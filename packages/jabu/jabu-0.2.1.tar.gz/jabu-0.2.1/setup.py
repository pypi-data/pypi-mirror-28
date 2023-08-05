from setuptools import setup


setup(
    name='jabu',
    version='0.2.1',
    description='Just Another Backup Utility',
    url='https://gitlab.com/carbans/jabu',
    author='Carlos Latorre',
    author_email='me@carloslatorre.net',
    license='GPL3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Archiving :: Backup',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='backup jabu system sysadmin',
    packages=['jabu', 'jabu.sources', 'jabu.destinations', 'jabu.notifications'],
    install_requires=['fnmatch', 'os', 'shutil', 'datetime', 'subprocess'],
    entry_points={
          'console_scripts': [
              'jabu = jabu.main:main'
          ]
    }
)
