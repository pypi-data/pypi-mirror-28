# eth-validation

[![Join the chat at https://gitter.im/ethereum/eth-validation](https://badges.gitter.im/ethereum/eth-validation.svg)](https://gitter.im/ethereum/eth-validation?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Build Status](https://travis-ci.org/ethereum/eth-validation.png)](https://travis-ci.org/ethereum/eth-validation)
   

Python tools for validating Ethereum-related objects

* Python 3.5+ support

Read more in the [documentation on ReadTheDocs](http://eth-validation.readthedocs.io/). [View the change log on Github](docs/releases.rst).

## Quickstart

```sh
pip install eth-validation
```

## Developer setup

If you would like to hack on eth-validation, set up your dev environment with:

```sh

git clone git@github.com:ethereum/eth-validation.git
cd eth-validation
virtualenv -p python3 venv
. venv/bin/activate
pip install -e .[dev]
```

### Testing Setup

During development, you might like to have tests run on every file save.

Show flake8 errors on file change:

```sh
# Test flake8
when-changed -v -s -r -1 eth_validation/ tests/ -c "clear; flake8 eth_validation tests && echo 'flake8 success' || echo 'error'"
```

Run multi-process tests in one command, but without color:

```sh
# in the project root:
pytest --numprocesses=4 --looponfail --maxfail=1
# the same thing, succinctly:
pytest -n 4 -f --maxfail=1
```

Run in one thread, with color and desktop notifications:

```sh
cd venv
ptw --onfail "notify-send -t 5000 'Test failure ⚠⚠⚠⚠⚠' 'python 3 test on eth-validation failed'" ../tests ../eth_validation
```

### Release setup

For Debian-like systems:
```
apt install pandoc
```

To release a new version:

```sh
make release bump=$$VERSION_PART_TO_BUMP$$
```

#### How to bumpversion

The version format for this repo is `{major}.{minor}.{patch}` for stable, and
`{major}.{minor}.{patch}-{stage}.{devnum}` for unstable (`stage` can be alpha or beta).

To issue the next version in line, specify which part to bump,
like `make release bump=minor` or `make release bump=devnum`.

If you are in a beta version, `make release bump=stage` will switch to a stable.

To issue an unstable version when the current version is stable, specify the
new version explicitly, like `make release bump="--new-version 4.0.0-alpha.1 devnum"`
