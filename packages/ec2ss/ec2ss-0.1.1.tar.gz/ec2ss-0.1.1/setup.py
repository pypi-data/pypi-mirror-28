
from setuptools import setup, find_packages

setup(
    name = 'ec2ss',
    version = '0.1.1',
    description = 'Simple CLI for start/stop EC2 instances',
    url = 'https://github.com/blurblah/ec2_start_stop',
    author = 'blurblah',
    author_email = 'blurblah@blurblah.net',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords = 'ec2 start stop',
    packages = find_packages(exclude=['tests']),
    install_requires = ['boto3'],
    python_requires = '>=3',
)