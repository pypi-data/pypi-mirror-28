from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sudoku-cli',
    version='0.4',
    description='A CLI for solving Sudoku',
    long_description=long_description,
    url='https://github.com/lukegrecki/sudoku-cli',
    author='Luke Grecki',
    author_email='lukegrecki@gmail.com',
    keywords='sudoku',
    packages=find_packages(exclude=['tests*', 'benchmarks*']),
    install_requires=[
        'Click',
    ],
    python_requires='>=3',
    extras_require={
        'test': ['coverage', 'flake8'],
    },
    entry_points='''
        [console_scripts]
        sudoku=sudoku.cli:sudoku
    '''
)