from setuptools import setup
#from distutils.core import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='xyz-helloworld-script-git',    # This is the name of your PyPI-package.
    version='1.2',                          # Update the version number for new releases
    #scripts=['test.py']                  # The name of your scipt, and also the command you'll be using for calling it
    author = '',
    author_email = '',
    url = 'https://github.com/xiaoyanzhuo/ETRI',
    #download_url = 'https://github.com/xiaoyanzhuo/ETRI/releases/tag/V1.0'
    packages=['test'],
    scripts=['bin/test-joke'],
    zip_safe=False
)
