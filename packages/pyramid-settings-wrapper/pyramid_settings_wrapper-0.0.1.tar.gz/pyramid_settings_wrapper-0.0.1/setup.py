import sys
from setuptools import setup, find_packages
sys.path.append("pyramid_settings_wrapper")
from version import get_version

requires = [
    'pyramid',
    ]

setup(
  name = 'pyramid_settings_wrapper',
  packages = find_packages(),
  install_requires=requires,
  version=get_version(),
  description = 'Transforms Pyramid config into a flexible class for easy access to config values.',
  author = 'Matthew Richardson',
  author_email = 'm.richardson@ed.ac.uk',
  license = 'GNU Affero General Public License v3 or later (AGPLv3+)',
  url = 'https://github.com/mrichar1/pyramid_settings_wrapper',
  keywords = ['pyramid', 'config'],
  classifiers = [
      'Development Status :: 5 - Production/Stable',
      'Framework :: Pyramid',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Topic :: Internet :: WWW/HTTP',
      'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      'Topic :: Software Development :: Libraries :: Application Frameworks',
      'Topic :: Software Development :: Libraries :: Python Modules',
  ],
  test_suite="tests",
  )
