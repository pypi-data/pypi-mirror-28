from setuptools import setup, find_packages

setup(
    name='blupointclient',  # This is the name of your PyPI-package.
    version='0.1.4',  # Update the version number for new releases
    description='BluPoint Client',
    py_modules=['blupointclient'],
    #scripts=['demo']  # The name of your scipt, and also the command you'll be using for calling it
    #packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    entry_points={  # Optional
        'console_scripts': [
            'blupointclient=blupointclient:main',
        ],
    },
)
