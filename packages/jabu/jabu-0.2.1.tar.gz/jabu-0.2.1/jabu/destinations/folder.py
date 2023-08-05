import os
import fnmatch
import shutil
import datetime
import subprocess
import logging

from jabu.exceptions import BackupException
from jabu.destinations import backupdestination
from jabu.destinations.destination import BackupDestination


@backupdestination('folder')
class Folder(BackupDestination):
    def __init__(self, config):
        BackupDestination.__init__(self, config)
        self.path = config['path']

    def send(self, id, name, suffix, filename):
        logging.info("The path of filename is: '%s' " % filename)
        logging.info("Destination path is: '%s' " % self.path)

        directoryfile = "%s-%s.%s" % (
            id,
            datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
            suffix)

        destfile = os.path.join(self.path, directoryfile)
        # The best option is use shutil.copyfile
        shutil.copyfile(filename, destfile)

    def cleanup(self, id, name, stats):
        logging.info("Clean up the path: '%s'..." % self.path)
        pattern = '%s-*.jb' % id
        results = []
        for root, dirs, files in os.walk(self.path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    results.append(os.path.join(root, name))
                    logging.info("Found: %s" % os.path.join(root, name))

        sorted(results)
        numcopy = len(results)
        logging.info("There are '%s' copy/ies of this backup." % numcopy)
        if numcopy > self.retention_copies:
            logging.info("The number of retention copies('%s') is smaller than numcopy('%s')" % (self.retention_copies,
                                                                                                 numcopy))
            numdelete = numcopy - self.retention_copies
            files_delete = results[:numdelete]

            for item in files_delete:
                logging.info("Erase the backup copy: '%s' " % item)
                os.remove(item)
