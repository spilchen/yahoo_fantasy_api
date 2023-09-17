#!/usr/bin/env python

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='yahoo_fantasy_api',
      version='2.8.0',
      description='Python bindings to access the Yahoo! Fantasy APIs',
      long_description=readme(),
      url='http://github.com/spilchen/yahoo_fantasy_api',
      author='Matt Spilchen',
      author_email='matt.spilchen@gmail.com',
      license='MIT',
      packages=['yahoo_fantasy_api'],
      setup_requires=["pytest-runner"],
      tests_require=["pytest"],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
      ],
      install_requires=['objectpath', 'pytz', 'yahoo_oauth',
                        'docopt'],
      python_requires='>=3',
      zip_safe=False,
      scripts=['yahoo_fantasy_api/scripts/yfa_draft_results',
               'yahoo_fantasy_api/scripts/yfa_init_oauth_env',
               'yahoo_fantasy_api/scripts/yfa_league',
               'yahoo_fantasy_api/scripts/yfa_team']
      )
