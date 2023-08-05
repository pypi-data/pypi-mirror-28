from distutils.core import setup

setup(
    name='dform',
    version='0.0.4',
    description='SQL ORM API for pandas DataFrame #tag: list dict pandas dataframe dict-list list of dict record',
    author = 'HS Moon',
    author_email = 'mhs9089@gmail.com',
    py_modules = ['dform', 'orms'],
    install_requires=['pandas'],
    url='https://github.com/zwolf21/dform'
)