# Mookfist LimitlessLED Controller v0.1.2
[![Build Status](https://travis-ci.org/mookfist/mookfist-lled-controller.svg?branch=develop)](https://travis-ci.org/mookfist/mookfist-lled-controller)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/dfe89d6cf72045589e4f7ca6bb399ed7)](https://www.codacy.com/app/mookfist/mookfist-lled-controller?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mookfist/mookfist-lled-controller&amp;utm_campaign=Badge_Grade)

Intended as a simple wrapper around the LimitlessLED wifi protocol written in python.

Supports wifi bridge versions 4, 5, and 6.

Currently white temperature support is not implemented.

There are no plans to implement the "party mode" features of the Limitless LED protocol. But I am not against accepting a pull request for them.

For more information on the LimitlessLED protocol visit http://limitlessled.com/dev

## Installation

### From Source

Download the code: https://github.com/mookfist/mookfist-limitlessled-controller/archive/master.zip

```
$ unzip master.zip
$ python setup.py install
$ python lled.py --help
```

### From PyPI

```
$ pip install mookfist-lled-controller
$ lled.py --help
```

## Usage

You can view the documentation over at http://mookfist-lled-controller.readthedocs.io

You can view examples at https://github.com/mookfist-lled-controller/tree/examples
