from codecs import open
from os import path

from setuptools import find_packages, setup

BASE_PATH = path.abspath(path.dirname(__file__))


def read(filepath):
    with open(path.join(BASE_PATH, filepath), encoding='utf-8') as f:
        return f.read()


setup(
    name='randpy',
    version='0.1.0',
    description='Yiny set of utilities to generate random data',
    long_description=read('README.rst'),
    url='https://github.com/mattshaffer11/randpy',
    license='MIT',
    author='Matt Shaffer',
    author_email='mattshaffer11@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    keywords='testing data random',
    packages=find_packages(exclude=['tests']),
)
