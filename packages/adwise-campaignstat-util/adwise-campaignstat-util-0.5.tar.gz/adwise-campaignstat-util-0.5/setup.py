from setuptools import setup
setup(
    name='adwise-campaignstat-util',    # This is the name of your PyPI-package.
    version='0.5',                          # Update the version number for new releases
    scripts=['campaignstat'],                  # The name of your scipt, and also the command you'll be using for calling it
    install_requires=[
           'requests',
      ] 
)
