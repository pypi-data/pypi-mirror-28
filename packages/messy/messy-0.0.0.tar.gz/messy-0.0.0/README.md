messy
===========

[![](https://travis-ci.org/not4drugs/messy.svg?branch=master)](https://travis-ci.org/not4drugs/messy "Travis CI")
[![](https://codecov.io/gh/not4drugs/messy/branch/master/graph/badge.svg)](https://codecov.io/gh/not4drugs/messy "Codecov")
[![](https://img.shields.io/github/license/not4drugs/messy.svg)](https://github.com/not4drugs/messy/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/messy.svg)](https://badge.fury.io/py/messy "PyPI")

In what follows `python3` is an alias for `python3.5` or any later
version (`python3.6` and so on).

Installation
------------

Install the latest `pip` & `setuptools` packages versions

```bash
python3 -m pip install --upgrade pip setuptools
```

### Release

Download and install the latest stable version from `PyPI` repository

```bash
python3 -m pip install --upgrade messy
```

### Developer

Download and install the latest version from `GitHub` repository

```bash
git clone https://github.com/not4drugs/messy.git
cd messy
python3 setup.py install
```

Bumping version
---------------

Install
[bumpversion](https://github.com/peritus/bumpversion#installation).

Choose which version number category to bump following [semver
specification](http://semver.org/).

Test bumping version

```bash
bumpversion --dry-run --verbose $VERSION
```

where `$VERSION` is the target version number category name, possible
values are `patch`/`minor`/`major`.

Bump version

```bash
bumpversion --verbose $VERSION
```

**Note**: to avoid inconsistency between branches and pull requests,
bumping version should be merged into `master` branch as separate pull
request.

Running tests
-------------

Plain

```bash
python3 setup.py test
```

Inside `Docker` container

```bash
docker-compose up
```

Inside `Docker` container with remote debugger

```bash
./set-dockerhost.sh docker-compose up
```

Bash script (e.g. can be used in `Git` hooks)

```bash
./run-tests.sh
```
