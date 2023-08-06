from setuptools import setup
#from distutils.core import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='etri-performance-optimize',    # This is the name of your PyPI-package.
    version='0.5',                          # Update the version number for new releases
    #scripts=['test.py']                  # The name of your scipt, and also the command you'll be using for calling it
    author = 'xzhuo',
    author_email = '',
    url = 'https://github.com/xiaoyanzhuo/ETRI',
    #download_url = 'https://github.com/xiaoyanzhuo/ETRI/releases/tag/V1.0'
    packages=['profiling'],
    scripts=['bin/profiling-analysis'],
    include_package_data=True,
    zip_safe=False
)
