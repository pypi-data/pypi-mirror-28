# Makaron

[![build status](https://gitlab.com/makaron/makaron/badges/master/build.svg)](https://gitlab.com/makaron/makaron/commits/master)
[![coverage](https://gitlab.com/makaron/makaron/badges/master/coverage.svg?job=coverage)](https://makaron.gitlab.io/makaron/coverage)
[![PyPI version](https://badge.fury.io/py/makaron.svg)](https://badge.fury.io/py/makaron)

A simple way to handle your version number.

Need more info, look at the homepage documentation. [makaron.gitlab.io](http://makaron.gitlab.io/)

## Install

```
pip install makaron
```

## Config

Makaron expect a `.makaron.yml` file in the current working directory.
This file list the files where Makaron has to update the version number.

You have to give Makaron two information. First the file where is supposed to search.
Second a regex that will let him find the line where is the version number.

You can update version number with this format `major.minor.patch` with the following `.makaron.yml` file.

```
setup.py: "__version__ = '[version]'"
```

You can also add several files to update using different method, like so:

```
setup.py: "__version__ = '[version]'"
lib/version.py: "__version__ = '[version]'"
```

You can also update different versions in the same file, doing this:

```
setup.py:
  - "__version__ = '[version]'"
  - "@version: [version]"
```

## Update version

Just type the name of the number you want to increase:

```bash
$ makaron major
```
or

```bash
$ makaron minor
```

or

```bash
$ makaron patch
```

## Print the current version

Just type `makaron` in your prompt.
