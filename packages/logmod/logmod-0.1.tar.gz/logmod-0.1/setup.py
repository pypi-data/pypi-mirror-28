import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme_rst = f.read()

setup(
    name='logmod',
    url='https://github.com/digitalmensch/logmod',
    download_url='https://pypi.python.org/pypi/logmod',
    description='Log all calls to a module',
    long_description=readme_rst,
    keywords='logging, module, debugging',
    platforms='any',
    license="MIT",
    version='0.1',
    author='Tobias Ammann',
    py_modules=['logmod'],
    install_requires=['structlog'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'
    ],
)
