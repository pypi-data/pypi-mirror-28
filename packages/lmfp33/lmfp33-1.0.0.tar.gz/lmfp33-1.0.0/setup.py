from __future__ import print_function  
from setuptools import setup, find_packages  
import sys  
  
setup(  
    name="lmfp33",
    version="1.0.0",
    author="lanmengfei",
    author_email="865377886@qq.com",
    description="兰孟飞写的好用的包",
    long_description=open("README.txt",encoding="utf-8").read(),
    license="MIT",
    url="https://user.qzone.qq.com/865377886",
    packages=['lmfp33'],
    install_requires=[
        #"pandas",
        #"sqlalchemy",
        #"pymssql",
        #"jieba",
        #"numpy",
        "xlsxwriter",
        "pymssql",
        "psycopg2"
        ],  
    classifiers=[  
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ]
)