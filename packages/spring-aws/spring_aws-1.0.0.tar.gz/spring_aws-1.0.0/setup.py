# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='spring_aws',
    version='1.0.0',
    description='Generic AWS Utilities',
    long_description=readme,
    author='Jiwan Rai',
    author_email='jiwan@sheriemuijs.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

