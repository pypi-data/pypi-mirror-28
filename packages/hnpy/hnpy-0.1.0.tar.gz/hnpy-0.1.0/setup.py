from setuptools import setup

from hnpy import __version__

setup(name='hnpy',
      author='jarhill0',
      author_email='',
      description='Yet another object-based Hacker News API wrapper for Python.',
      install_requires=['requests >= 2.18.4'],
      keywords='hacker news api wrapper python3',
      license='MIT',
      long_description='This package is for Python 3 only.\n\nClick here for README: '
                       'https://github.com/jarhill0/hnpy#hnpy',
      packages=['hnpy'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest',
                     'betamax >= 0.8.0',
                     'betamax_serializers >= 0.2.0'],
      test_suite='tests',
      url='https://github.com/jarhill0/hnpy',
      version=__version__)
