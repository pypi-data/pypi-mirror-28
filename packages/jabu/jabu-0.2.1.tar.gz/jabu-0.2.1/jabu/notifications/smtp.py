import smtplib

try:
    from email.mime.text import MIMEText
except:
    from email.MIMEText import MIMEText

from jabu.exceptions import BackupException
from jabu.notifications import backupnotification
from jabu.notifications.notification import BackupNotification


@backupnotification('smtp')
class SMTP(BackupNotification):
    def __init__(self, config):
        BackupNotification.__init__(self, config, 'smtp')
        self.host = config['host']
        self.port = config['port']
        self.username = config['credentials']['username']
        self.password = config['credentials']['password']
        self.use_tls = bool(config['use_tls'])
        self.use_ssl = bool(config['use_ssl'])
        self.success_to = config['success_to']
        self.failure_to = config['failure_to']
        self.debug = bool(config['debug'])

    def notify_success(self, source, hostname, filename, stats):
        if 'success_to' not in dir(self) or not self.success_to:
            return
        filesize = stats.getSizeDescription()
        fromaddr = self.username
        toaddrs = self.success_to
        msg = MIMEText("Successfully backed up %s (%s) [size: %s]" % (source.name, source.type, filesize))
        msg['Subject'] = "Backup of %s (%s) on %s was successful" % (source.name,  source.type, hostname)
        msg['X-Backup-Id'] = source.id
        msg['X-Backup-Type'] = source.type
        msg['X-Backup-Hostname'] = hostname

        if self.use_ssl:
            server = smtplib.SMTP_SSL(self.host, self.port)
        else:
            server = smtplib.SMTP(self.host, self.port)

        if self.debug:
            server.set_debuglevel(1)

        if self.use_tls:
            server.starttls()
            server.ehlo()

        if 'username' in dir(self):
            server.login(self.username, self.password)

        server.sendmail(fromaddr, toaddrs, msg.as_string())
        server.quit()

    def notify_failure(self, source, hostname, e):
        import traceback; traceback.print_exc()
        if 'failure_to' not in dir(self) or not self.failure_to:
            return
        fromaddr = self.username
        toaddrs = self.failure_to
        msg = MIMEText("Error encountered while backing up %s (%s): \n\n%s" % (source.name, source.type, str(e)))
        msg['Subject']="ERROR: Backup of %s (%s) on %s failed" % (source.name, source.type, hostname)
        msg['X-Backup-Id'] = source.id
        msg['X-Backup-Type'] = source.type
        msg['X-Backup-Hostname'] = hostname
        if self.use_ssl:
            server = smtplib.SMTP_SSL(self.host, self.port)
        else:
            server = smtplib.SMTP(self.host, self.port)
        if self.debug:
            server.set_debuglevel(1)
        if self.use_tls:
            server.starttls()
            server.ehlo()
        if 'username' in dir(self):
            server.login(self.username, self.password)
        server.sendmail(fromaddr, toaddrs, msg.as_string())
        server.quit()
