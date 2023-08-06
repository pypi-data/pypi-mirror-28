# coding: utf-8

from setuptools import setup

from pyofo import __version__

setup(
    name='pyofo',
    version=__version__.__version__,
    author=__version__.__author__,
    author_email=__version__.__author_email__,
    url='https://github.com/qxzzxq/pyofo',
    packages=['pyofo'],
    license='MIT',
    description='A Python library to interface with ofo bike API',
    keywords = ['ofo', 'bike'], 
    install_requires=[
        'requests',
    ],
)
