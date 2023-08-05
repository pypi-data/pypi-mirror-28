from distutils.core import setup

from setuptools import find_packages

setup(
    name='autogit-client',
    packages=find_packages(),
    scripts=['autogit_daemon/autogit_client.py', 'autogit_daemon/daemon.py', 'autogit_daemon/utils.py'],
    version='0.1.1',
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },
    description='A Daemon for Autogit Client',
    author='Vimlabs',
    author_email='neiell@vimlabs.com',
    url='https://gitlab.vimlabs.com/vimlabs/autogit.io-daemon',
    download_url='https://gitlab.vimlabs.com/vimlabs/autogit.io-daemon/repository/master/archive.tar.gz',
    keywords=['autogit', 'autogit-daemon', 'autogit-client', 'vimlabs', 'auto-deploy', 'deploy automation'],  # arbitrary keywords
    classifiers=[],
    entry_points={
        'console_scripts': [
            'autogit-client=autogit_daemon.autogit_client:main'
        ],
    }
)
