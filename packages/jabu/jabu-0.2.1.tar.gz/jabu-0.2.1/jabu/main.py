#!/usr/bin/env python

import os
import time
import sys
import argparse
import getpass
import logging
import json

import jabu.stats
import jabu.sources
import jabu.destinations
import jabu.notifications

from jabu.exceptions import BackupException

default_modules = [
    'jabu.sources.folder',
    'jabu.destinations.samba',
    'jabu.notifications.smtp',
]


class BackupRunInstance:
    def __init__(self):
        import platform
        self.hostname = platform.node()
        self.source_modules = []
        self.sources = []
        self.destination_modules = []
        self.destinations = []
        self.notification_modules = []
        self.notifications = []

        self.stats = jabu.stats.BackupRunStatistics()

    def run(self):
        for source in self.sources:
            # Avisar todas las notificaciones configuradas que empezamos
            for notification in self.notifications:
                notification.notify_start(source, self.hostname)

            try:

                starttime = time.time()
                dumpfiles = source.dump_and_compress()
                if not isinstance(dumpfiles, list):
                    dumpfiles = [dumpfiles, ]

                endtime = time.time()

                self.stats.dumptime = endtime - starttime

                # Add up backup file sizes
                totalsize = 0
                for dumpfile in dumpfiles:
                    totalsize = totalsize + os.path.getsize(dumpfile)

                self.stats.size = totalsize

                # Send each dump file to each listed destination
                starttime = time.time()
                for dumpfile in dumpfiles:
                    for destination in self.destinations:
                        destination.send(source.id, source.name, "jb", dumpfile)
                        destination.cleanup(source.id, source.name, self.stats)
                endtime = time.time()
                self.stats.uploadtime = endtime - starttime

                # Trigger success notifications as required
                for notification in self.notifications:
                    notification.notify_success(source, self.hostname, dumpfile, self.stats)

            except Exception as e:
                import traceback
                traceback.print_exc()

                for notification in self.notifications:
                    notification.notify_failure(source, self.hostname, e)
            finally:
                # Done with dump file now
                if 'dumpfile' in locals() and os.path.isfile(dumpfile):
                    os.unlink(dumpfile)

        logging.debug('Complete.')


def main():

    try:
        os.umask(0o77)

        # Read cmmand line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('configfile', metavar='configfile', nargs=1,
                            help='name of configuration file to use for this run')
        parser.add_argument('-v', help='With this flag activate the verbose', dest='verbose', action='store_true')
        parser.add_argument('-d', help='With this flag activate the debug', dest='debug', action='store_true')
        args = parser.parse_args()

        configfile = args.configfile[0]

        # Enable logging if verbosity requested
        if args.debug:
            logging.basicConfig(level=logging.DEBUG)
        elif args.verbose:
            logging.basicConfig(level=logging.INFO)

        # Read our JSON configuration file
        with open(configfile) as json_conf:
            config = json.load(json_conf)

        # Import main and additional handler library modules
        backup_modules = config['modules']
        if backup_modules is None:
            backup_modules = default_modules
        for modulename in backup_modules:
            logging.debug("Importing module '%s'" % modulename)
            try:
                module = __import__(modulename)
            except ImportError as e:
                logging.error("Error importing module: %s" % e.__str__())

        # Instantiate handlers for any listed destinations
        destinations = []
        for dest_id, dest_class in jabu.destinations.handlers.items():
            logging.debug("Dest(%s) - %s" % (dest_id, dest_class))
            for dest_config in config['destinations']:
                if dest_config['type'] == dest_id:
                    destination = dest_class(dest_config)
                    destinations.append(destination)

        # Instantiate handlers for any listed notifications
        notifications = []
        for notify_id, notify_class in jabu.notifications.handlers.items():
            logging.debug("Notify(%s) - %s" % (notify_id, notify_class))
            for notify_config in config['notifications']:
                if notify_config['type'] == notify_id:
                    notification = notify_class(notify_config)
                    notifications.append(notification)

        # Loop through sections, process those we have sources for
        sources = []
        for source_id, source_class in jabu.sources.handlers.items():
            logging.debug("Source(%s) - %s" % (source_id, source_class))
            for source_config in config['sources']:
                if source_config['type'] == source_id:
                    source = source_class(source_config)
                    sources.append(source)

        if len(sources) < 1:
            raise BackupException("No sources listed in configuration file.")

        instance = BackupRunInstance()
        instance.notifications = notifications
        instance.sources = sources
        instance.destinations = destinations
        instance.run()

    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()
