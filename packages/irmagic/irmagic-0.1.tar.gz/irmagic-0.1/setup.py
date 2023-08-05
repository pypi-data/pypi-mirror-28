from setuptools import setup, find_packages
 
setup(
    name='irmagic',    # This is the name of your PyPI-package.
    version='0.1',                          # Update the version number for new releases
    packages=find_packages(exclude=['contrib', 'docs', 'tests'])                  # The name of your scipt, and also the command you'll be using for calling it
)