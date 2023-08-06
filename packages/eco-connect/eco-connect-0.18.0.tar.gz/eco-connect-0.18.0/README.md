# eco-connect @ Ecorithm
A wrapper for connecting to Ecorithm's API Platform through python

[![Build Status](https://travis-ci.org/ecorithm/eco-connect.svg?branch=master)](https://travis-ci.org/ecorithm/eco-connect)
[![Coverage Status](https://coveralls.io/repos/github/ecorithm/eco-connect/badge.svg?branch=master&t=RDCkPJ)](https://coveralls.io/github/ecorithm/eco-connect?branch=master)

## Requirements
- The package can be installed using pip.
  `pip3 install eco-connect --upgrade`
- This module requires authentication for the connectors to be use. Credentials are loaded through your environment variables. Create the following env variables with your provided ecorithm credentials:
`export ECO_CONNECT_USER=MyEcorithmUserName`
`export ECO_CONNECT_PASSWORD=MyEcorithmPASSWord`

- To test the your credentials open a python interpreter and run the following:
`from  eco_connect import validate_credentials`
`validate_credentials()`


## Usage
- Supported ecorithm connectors include:
* FactsService

- To use, import the connector i.e `from eco_connect import FactsService`

- For additional resources please refer to documentation at `https://django.prod.ecorithm.com/`
or contact support at `help@ecorithm.com`

## Deploying to pypi
- To deploy the latest distribution to pypi, run the following commands from the root project folder:
- `python3 setup.py sdist`
- `python3 setup.py bdist_wheel --universal`
- `twine upload dist/*`
- enter the username / password for the pypi account found on ecorithm's one-password.
- latest version to pip install can be found here: `https://pypi.python.org/pypi/eco-connect`
