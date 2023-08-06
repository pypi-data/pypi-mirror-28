# eco-connect @ Ecorithm
A wrapper for connecting to Ecorithm's API Platform through python

[![Build Status](https://travis-ci.org/ecorithm/eco-connect.svg?branch=master)](https://travis-ci.org/ecorithm/eco-connect)
[![Coverage Status](https://coveralls.io/repos/github/ecorithm/eco-connect/badge.svg?branch=master&t=RDCkPJ)](https://coveralls.io/github/ecorithm/eco-connect?branch=master)

## Documentation
- http://eco-connect.readthedocs.io/en/latest/index.html

## Deploying to pypi
- To deploy the latest distribution to pypi, run the following commands from the root project folder:
- rm -rf `dist/`
- `python3 setup.py sdist`
- `twine upload dist/*`
- enter the username / password for the pypi account found on ecorithm's one-password.
- latest version to pip install can be found here: `https://pypi.python.org/pypi/eco-connect`
