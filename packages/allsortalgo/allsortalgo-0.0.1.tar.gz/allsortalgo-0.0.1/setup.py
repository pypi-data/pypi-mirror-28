from setuptools import setup, find_packages

CLASSIFIERS = [
    'Development Status :: 1',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Scientific/Engineering']

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='allsortalgo',
    version='0.0.1',
    description='Python package containing implementation of all sorting algorithms',
    long_description=readme,
    author='Sanny Kumar',
    author_email='sanny.iitkgp@gmail.com',
    url='https://github.com/sannykr/allsortalgo',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=CLASSIFIERS
)

