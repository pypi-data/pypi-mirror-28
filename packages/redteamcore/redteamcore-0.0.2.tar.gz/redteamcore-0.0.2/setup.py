from distutils.core import setup
from distutils.core import Command
import os
import sys
import setuptools
import unittest

class CleanPycCommand(Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""
        pass

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""
        pass

    def run(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filenames = [os.path.join(d, x)
                     for d, _, files in os.walk(dir_path)
                     for x in files if os.path.splitext(x)[1] == '.pyc']
        for filename in filenames:
            os.remove(filename)

setup(name='redteamcore',
      packages=['redteamcore'],
      install_requires=['requests', 'python-dateutil'],
      version='0.0.2',
      description='Core Python modules for use in tooling.',
      author='Kenneth Evensen',
      author_email='kevensen@redhat.com',
      license='GPLv3',
      url='https://github.com/fedoraredteam/redteamcore',
      download_url='https://github.com/fedoraredteam/redteamcore/archive/0.0.2.tar.gz',
      keywords=['frt', 'redteam', 'linux'],
      classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 2.7',
      ],
      platforms=['Linux', 'OSX'],
      test_suite='tests',
      cmdclass={'tidy': CleanPycCommand})
