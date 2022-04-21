from distutils.core import setup
from setuptools import find_packages
import py2exe
import PySimpleGUI


setup(
    options={
        'py2exe': {
            'includes': ['PySimpleGUI'],
            'packages': find_packages(),
        }
    },
    windows=[{
        'script': 'UI.py',
    }],
)