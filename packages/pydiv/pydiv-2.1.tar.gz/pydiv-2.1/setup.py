from setuptools import setup

with open('README.md') as f:
    readme=f.read()

with open('LICENSE.txt') as f:
    license=f.read()

setup(
    name = 'pydiv',
    packages = ['pydiv'],
    version = '2.1',
    description = 'Gives the division forms for decimal numbers',
    author = 'Ankan Das',
    author_email = 'ankandas2222@gmail.com',
    url = 'https://github.com/AnkanDas22/pydiv',
    download_url = 'https://github.com/AnkanDas22/pydiv/archive/2.0.tar.gz',
    long_description=readme)
