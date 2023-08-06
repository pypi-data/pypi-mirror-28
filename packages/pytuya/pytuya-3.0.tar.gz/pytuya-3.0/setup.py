from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytuya',
    version='3.0',
    description='Control Tuya devices with python.',
    long_description='Control Tuya devices with python.',
    url='http://seandev.org',
    author='Sean Olson',
    author_email='seandolson654@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Home Automation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    keywords='home automation',
    packages=["pytuya"],
    install_requires=[
          'pyaes',
      ],
)
