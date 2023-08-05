from setuptools import setup, find_packages

setup(
    name='rss',
    version='0.0.0',
    packages=find_packages(),
    install_requires=[
        'redis==2.10.6',
    ],
    author='Aji Liu',
    author_email='amigcamel@gmail.com',
    description='A Python API for controlling redis master and slave via sentinel.',
)
