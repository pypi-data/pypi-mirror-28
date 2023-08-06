from setuptools import setup
#from distutils.core import setup

setup(
    name='xyz-helloworld-script',    # This is the name of your PyPI-package.
    version='0.1',                          # Update the version number for new releases
    scripts=['helloworld']                  # The name of your scipt, and also the command you'll be using for calling it
)
