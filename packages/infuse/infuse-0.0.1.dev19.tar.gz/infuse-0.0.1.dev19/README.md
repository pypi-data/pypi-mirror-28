# Infuse

[![Build Status](https://travis-ci.org/bregman-arie/infuse.svg?branch=master)](https://travis-ci.org/bregman-arie/infuse)

Infuse is nothing at this point. We'll update you once it becomes something

* [Requirements](#requirements)
* [Installation](#installation)

## Requirements

* Python >= 2.7

## Installation

    pip install .

## Initialize the database

    infuse-db

## Run the flask server

    infuse-server

## Configuration

Infuse loads configuration in this order:

    Default config.py - built-in. Part of Infuse code base.
    Environment varliabes - any of the environment vairables specified in the table below that the user export (e.g. `export INFUSE_SERVER_PORT=80`)
    Configurtion file - the default configuration file (/etc/infuse/infuse.com) or the file you mentioned with parser/environment variable.
    Parser - arguments you pass with infuse command-line invocation.
    
| Name | Description |
| ---- | ----------- |
| `INFUSE_CONFIG_FILE` | The configuration file from where to load additional configuration
| `INFUSE_DEBUG` | Turn on DEBUG
| `INFUSE_SERVER_PORT` | The port to use when running Infuse server
| `INFUSE_DATABASE_URL` | The database URL where we can connect to, defaults to sqlite local db file: infuse.db

# Contributions

To contribute use github pull requests.
