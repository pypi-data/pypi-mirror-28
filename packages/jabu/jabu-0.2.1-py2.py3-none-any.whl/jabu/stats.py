class BackupRunStatistics:
    def __init__(self):

        self.size = None

        self.dumptime = None

        self.uploadtime = None

        self.retained_copies = None

    def getSizeDescription(self):
        num = self.size

        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0

        return "NaN"
