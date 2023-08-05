import subprocess
import logging

from jabu.exceptions import BackupException


def encrypt(filename, passphrase):
    logging.info("Encrypting '%s' ..." % filename)
    encfilename = '%s.gpg' % filename
    encerrsname = '%s.err' % filename
    encfile = open(encfilename, 'wb')
    encerrs = open(encerrsname, 'wb')
    encargs = ['gpg', '--batch', '--yes', '-q', '--passphrase-fd', '0', '-c', filename]
    encproc1 = subprocess.Popen(encargs, stdin=subprocess.PIPE, stdout=encfile, stderr=encerrs)
    encproc1.communicate(passphrase)
    encproc1.wait()
    encfile.close()
    encerrs.close()
    exitcode = encproc1.returncode

    if exitcode != 0:
        errmsg = open(encerrsname, 'rb').read()
        raise BackupException("Error while encrypting: %s" % errmsg)
    return encfilename
