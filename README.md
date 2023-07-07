# Parble Python SDK

This repo contains the source code of the official python SDK for [Parble](https://parble.com/home) intelligent document processing API.

To access the API you will need a Parble account. Sign up for free at [signup](https://parble.com/signup).

## Documentation

Our documentation is continuously updated, you can find it here: [parblelabs.github.io/parble-python](https://parblelabs.github.io/parble-python/).


## Development of the library

### Setup local environment

1. `pip install hatch`
2. `pip install .`
3. `hatch run +py='3.10' test:cov`

### Documentation generation

Run: `hatch run docs:build-html`
