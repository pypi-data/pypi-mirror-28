'''one line comment'''
from setuptools import setup, find_packages

setup(
    name='ll-command',
    scripts=['p'],
    version='0.1.2',
    keywords='command line cli',
    description='a simple command to replace ll ',
    license='MIT License',
    url='https://github.com/hjlarry/ll-command',
    author='hjlarry',
    author_email='hjlarry@163.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'terminaltables',
        'colorclass'
    ],
)