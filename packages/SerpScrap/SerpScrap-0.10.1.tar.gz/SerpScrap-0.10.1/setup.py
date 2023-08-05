#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '0.10.1'


setup(
    name='SerpScrap',
    version=version,
    description='''
    A python scraper to extract and analyze data from
    search engine result pages and urls.
    Extract data, like url, title, snippet
    of results or ratings for given keywords.
    ''',
    long_description=open('README.rst').read(),
    author='Ronald Schmidt',
    author_email='ronald.schmidt@zu-web.de',
    doc_url='http://serpscrap.readthedocs.io/en/latest/',
    url='https://github.com/ecoron/SerpScrap',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'PySocks==1.6.7',
        'chardet==3.0.4',
        'beautifulsoup4==4.6.0',
        'html2text==2017.10.4',
        'lxml==3.8.0',
        'sqlalchemy==1.1.15',
        'selenium==3.8.1',
        'cssselect==1.0.1',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='seo scraper ad-detection scraping keywords',
)
