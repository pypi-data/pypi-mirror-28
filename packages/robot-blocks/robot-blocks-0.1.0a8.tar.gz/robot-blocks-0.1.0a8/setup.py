import os
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='robot-blocks',
    version='0.1.0a8',
    packages=find_packages(),
    include_package_data=True,
    license='Apache Software License',
    description='Building blocks for raspberry pi robot software',
    long_description=read('README.md'),
    author='Christopher Davies',
    author_email='christopherdavies553@gmail.com',
    url='https://chris104957.github.io/robot-blocks/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Robot Framework',
        'Framework :: Robot Framework :: Library',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['coverage==4.4.2', 'blinker==1.4', 'coveralls==1.2.0']
)

