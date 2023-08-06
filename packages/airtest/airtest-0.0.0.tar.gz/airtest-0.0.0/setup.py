from setuptools import setup, find_packages
from pip.req import parse_requirements


setup(
    name='airtest',
    version='0.0.0',
    author='Netease Games',
    author_email='gzliuxin@corp.netease.com',
    description='Automated test framework for android/iOS/Windows',
    long_description='Automated test framework for android/iOS/Windows, present by NetEase Games',
    url='https://github.com/AirtestProject/Airtest',
    license='Apache License 2.0',
    keywords=['automation', 'test', 'android', 'opencv'],
    packages=find_packages(exclude=['cover', 'examples', 'tests', 'dist', 'new_test']),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
)
