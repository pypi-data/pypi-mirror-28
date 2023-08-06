from distutils.core import setup

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sacrina'))

long_description="""
Python library for Sacrina API
  """

setup(
  name='sacrina',
  version= '0.1',
  author='S.S.Hussain',
  author_email='contact@sacrina.com',
  packages=['sacrina'],
  scripts=[],
  url='https://github.com/sacrina/sacrina-python/',
  download_url='https://github.com/sacrina/sacrina-python/archive/master.zip',
  license='Sacrina Lisence',
  long_description=long_description,
  install_requires=['requests>=2.18.4'],
  classifiers=[
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ],
  keywords=['sacrina', 'rest', 'sdk', 'sacrina-api']
)
