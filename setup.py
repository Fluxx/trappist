import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

tests_require = [
    'mock==1.0.1',
    'nose==1.3.0'
]

requires = [
    'Flask==1.0',
    'django>=1.4',
]

setup(
    name="trappist",
    version="0.2.0",
    author="Jeff Pollard",
    author_email="jeff.pollard@gmail.com",
    description=("Mount your Flask or WSGI app in your Django app."),
    license="MIT",
    keywords="django flask http mount",
    url="https://github.com/Fluxx/trappist",
    py_modules=['trappist'],
    install_requires=requires,
    tests_require=tests_require,
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP :: WSGI"
    ],
)
