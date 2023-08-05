'''
File: setup.py
Created Date: Monday January 15th 2018
Author: Sujan Poudel
Github: https://github.com/psuzn
Last Modified:Monday, January 15th 2018, 9:50:55 am
Copyright (c) 2018 https://github.com/psuzn
'''

from setuptools import setup, find_packages

setup(
    name='romonepali',
    packages=find_packages(),
    version='0.0.3',
    license='MIT',
    description='Romonised nepali input method for LInux.',
    author='Sujan Poudel',
    author_email="spoudel347@gmail.com",
    url='https://github.com/psuzn/romoNepali',
    download_url='https://github.com/psuzn/romoNepali',
    keywords=['unicode', 'Nepali', 'Romonised', 'Nepal'],  # arbitrary keywords
    install_requires=[
        "requests",
        "pynput"
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'],
    entry_points={
        'console_scripts': [
            'romonepali = romonepali.uni:init'
        ]},
)
