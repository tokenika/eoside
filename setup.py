from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='eoside',
      version='0.1',
      description='Python library for EOSIde',
      long_description=readme(),
      classifiers=[
        'Development Status :: 0.1 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Testing',
      ],
      keywords='EOSIO, smart contract development unit testing',
      url='https://github.com/tokenika/eoside',
      author='Tokenika',
      author_email='contact@tokenika.io',
      license='MIT',
      packages=['eoside'],
      install_requires=[
          'termcolor',
          'eosfactory'
      ],
      zip_safe=False)