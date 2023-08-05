import requests
import os
import json
import logging


from jabu.exceptions import BackupException
from jabu.notifications import backupnotification
from jabu.notifications.notification import BackupNotification


@backupnotification('telegram')
class Telegram(BackupNotification):
    def __init__(self, config):
        BackupNotification.__init__(self, config, 'telegram')
        self.api_token = config['api_token']
        self.chat_id = config['chat_id']

    def notify_success(self, source, hostname, filename, stats):
        filesize = stats.getSizeDescription()
        message = "Backup of '%s' (%s) on '%s' was successful [size: %s]." % (source.name, source.type, hostname,
                                                                              filesize)
        # call telegram api
        url = "https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}".format(self.api_token,
                                                                                     message, self.chat_id)
        response = requests.get(url)
        content = response.content.decode("utf8")

        logging.info("Send telegram message")
        # send message
        # writes logging
