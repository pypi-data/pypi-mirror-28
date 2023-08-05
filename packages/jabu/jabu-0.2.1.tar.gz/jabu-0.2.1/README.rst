# JABU - Just Another Backup Utility

This python script, given a backup configuration, will cycle through a list of backup 'sources'

### Instalation
- Install depencencies
```
$ sudo apt install python-setuptools
```
- Install JABU
```python
# python setup.py install
```
- Create a `jabu` user and add to sudoers
```bash
# useradd -m jabu
```
```
# cat > /etc/sudoers.d/99-jabu <<EOF
jabu ALL=(ALL) NOPASSWD: /bin/tar
EOF
```
- Create config file, example in the directory `config-sample.json`

```
# cp -rf jabu/jabu/config-sample.json /home/jabu/mynightlybackup.json
```
- Test your configuration by doing initial run of the jabu
```
# sudo -H -u backups /usr/local/bin/jabu -v /home/jabu/mynightlybackup.json
```

- Add yout job to cron.
```
# cat > /etc/cron.d/nightly-backups.conf <<EOF
0 2 * * * jabu /usr/local/bin/jabu /home/jabu/mynightlybackup.json
EOF
```
