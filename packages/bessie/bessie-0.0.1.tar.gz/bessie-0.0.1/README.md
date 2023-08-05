# Bessie - Base API Client

-----

**Table of Contents**

* [About](#about)
* [Building Clients](#building-clients)
* [Installation](#installation)
* [License](#license)

## About 

Bessie is a small base framework for building client APIs. 

## Building Clients

The `BaseClient` class is designed to be subclassed. Each method is also designed to be overriden to include custom logic for specific APIs (such as injecting an authorization header by overriding the `_prepare_request` method).

## Installation

Bessie is not yet avaialbe on PyPI, but should be soon. You can always install it from the repository though. 

## License

Bessie is distributed under the terms of the [MIT License](https://choosealicense.com/licenses/mit).

