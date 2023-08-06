#!/usr/bin/python3

from distutils.core import setup
import os
import stepic

if os.environ.get('RELEASE') != '0':
    version = stepic.__version__
else:
    version = stepic.__version__ + '~bzr'

setup(name='stepic',
      version=version,
      description='Python image steganography',
      author='Lenny Domnitser',
      author_email='lenny@domnit.org',
      maintainer="Scott Kitterman",
      maintainer_email="scott@kitterman.com",
      url='https://launchpad.net/stepic',
      license='GPL',
      py_modules=['stepic'],
      scripts=['stepic'],
      data_files=[('share/doc/stepic', ['COPYING', 'TODO']),
                  ('share/man/man1', ['stepic.1'])],
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
          'Environment :: Console',
          'Topic :: Multimedia :: Graphics',
          'Topic :: Utilities',
          'Development Status :: 6 - Mature',
          'Programming Language :: Python :: 3 :: Only'
          ]
      )
