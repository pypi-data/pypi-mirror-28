# ilabs.client
[![Build Status](https://travis-ci.org/innodatalabs/ilabs.client.svg?branch=master)](https://travis-ci.org/innodatalabs/ilabs.client)
[![PyPI version](https://badge.fury.io/py/ilabs.client.svg)](https://badge.fury.io/py/ilabs.client)

Python client to access api.innodatalabs.com endpoints.

## Building

```
virtualenv .venv -p python3  # or python2, as appropriate
. .venv/bin/activate
pip install -r requirements.txt
pip install mock nose

nosetests ilabs/client/test
```

## Usage

Quick start examples: https://github.com/innodatalabs/ilabs.client/tree/master/examples

User guide and API reference: https://innodatalabs.github.io/ilabs.client

## Command-Line Bulk Prediction Tool

This package also provides a CLI tool to run file-to-file prediction in bulk:
```
ilabs_bulk_predict -h

usage: ilabs_bulk_predict [-h] --domain DOMAIN [--user_key USER_KEY]

                          [--num_workers NUM_WORKERS]
                          input_dir output_dir

Sends all files from the input directory to prediction service and places
result in the output directory

positional arguments:
  input_dir             Directory where input files are located
  output_dir            Directory where output will be saved

optional arguments:
  -h, --help            show this help message and exit
  --domain DOMAIN, -d DOMAIN
                        Prediction domain
  --user_key USER_KEY, -u USER_KEY
                        Secret user key
  --num_workers NUM_WORKERS, -n NUM_WORKERS
                        Number of concurrent workers
```
