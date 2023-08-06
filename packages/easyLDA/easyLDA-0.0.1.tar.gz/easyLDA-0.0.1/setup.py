from setuptools import setup, find_packages

import os

_HERE = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

#try:
#    import pypandoc
#    long_description = pypandoc.convert('README.md', 'rst')
    
#except(IOError, ImportError):
#    long_description = open('README.md').read()



with open(os.path.join(_HERE, 'README.rst'),'r+') as fh:
    long_description = fh.read()

setup(
    name = "easyLDA",
    version = "0.0.1",
    description = "easily bult LDA Topic Models with just a list of docs (e.g. a list of twitter posts in CSV/TXT",
    long_description = long_description,
    author = "Shichao(Richard) Ji",
    author_email = "jshichao@vt.edu",
    url = "https://github.com/shichaoji/easyLDA",
    download_url = "https://github.com/shichaoji/easyLDA/archive/0.1.tar.gz",
    keywords = ['topic model','LDA','easy','text mining','natual language processing'],
    license = 'MIT', 
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        ],
    packages = find_packages(),
    install_requires=[
        'nltk',
        'gensim'
      ],
    entry_points={
        'console_scripts': ['easyLDA=easyLDA:main'],
      },
)

