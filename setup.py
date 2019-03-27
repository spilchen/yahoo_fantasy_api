from setuptools import setup

setup(name='yahoo_fantasy_api',
      version='0.0.1',
      description='APIs to access the set of Yahoo! Fantasy APIs',
      url='http://github.com/spilchen/yahoo_fantasy_api',
      author='Matt Spilchen',
      author_email='matt.spilchen@gmail.com',
      license='MIT',
      packages=['yahoo_fantasy_api'],
      setup_requires=["pytest-runner"],
      tests_require=["pytest"],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
      ],
      python_requires='>=3',
      zip_safe=False)
