from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.txt'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cryptotranslator',
    version='0.1.1',
    description='Names translation for cryptocurrency pairs and tickets.',
    long_description=long_description,
    url='https://github.com/estebance/crypto_translator',
    author='Esteban Ceron',
    author_email='restebance@gmail.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['pyyaml'],
    package_data={'cryptotranslator': ['*.yaml']},
    include_package_data=True,
    keywords='standard',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)
