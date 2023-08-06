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
    name = "recur7down",
    version = "0.2.1.6",
    description = "recursive web scraper code for work related project",
    long_description = long_description,
    author = "Shichao(Richard) Ji",
    author_email = "jshichao@vt.edu",
    url = "https://github.com/shichaoji/recur7down",
    download_url = "https://github.com/shichaoji/recur7down/archive/0.1.tar.gz",
    keywords = ['data''requests','python','scrapy'],
    license = 'MIT', 
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        ],
    packages = find_packages(),
    install_requires=[
        'Pandas',
        'json2df'
      ],
    entry_points={
        'console_scripts': ['recur7down=recur7down:main'],
      },
)

