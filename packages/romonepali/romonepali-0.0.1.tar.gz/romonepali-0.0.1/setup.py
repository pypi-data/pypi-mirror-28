from setuptools import setup, find_packages

setup(
    name='romonepali',
    packages=find_packages(),
    version='0.0.1',
    license='MIT',
    description='A simple program to install apks from a directory to android phone via adbSmall python program to install all apks on a directory(including apks in sub-directory of it) in your pc to android phones.',
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
