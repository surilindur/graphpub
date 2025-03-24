<p align="center">
    <img alt="logo" src="./.github/assets/logo.svg" width="64">
</p>

<p align="center">
    <a href="https://github.com/surilindur/graphport/actions/workflows/ci.yml"><img alt="CI" src=https://github.com/surilindur/graphport/actions/workflows/ci.yml/badge.svg?branch=main"></a>
    <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/%3C%2F%3E-Python-%233776ab.svg"></a>
    <a href="https://opensource.org/licenses/MIT"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-%23750014.svg"></a>
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/Code%20Style-black-000000.svg"></a>
</p>

Experimental simple prototype tool to publish [RDF](https://www.w3.org/RDF/) graphs
from local documents to a [SPARQL endpoint](https://www.w3.org/TR/sparql11-protocol/)
using [RDFLib](https://github.com/RDFLib/rdflib) and SPARQL update queries.
The tool exists to faciliate the following use-cases:

* Storing RDF graphs as documents on local filesystem. This makes it easier to do version control over them.
* Using relative URIs inside documents. When published, these URIs are mapped to a full URI under the specified base URI, following their relative path under the published root directory.

The tool does no mapping beyond filling in the relative URIs, and all input data is expected to be in RDF already.
The tool has been designed for smaller datasets, and other bulk loading mechanisms should be preferred for larger ones when available.
Export functionality is beyond the scope of the tool.
Authentication using a username and password is supported via environment variables.

## Dependencies

* Python
* RDFLib

## Compatibility

The queries are sent using `POST` with a `User-Agent` header following the [common conventions](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent),
and should thus work with reverse proxies that do agent validation or block the use of query strings.

The tool has been tested against the following SPARQL endpoints:

* Apache Jena Fuseki

## Usage

Authentication via username and password is facilitated through the environment variables `SPARQL_USERNAME` and `SPARQL_PASSWORD`,
which are used in the auth tuples of RDFLib's SPARQL store.

To publish a local directory from `./data` to the graph `http://localhost:8080/`,
by mapping all relative resource URIs under the graph URI,
and also purging the previous graph if it exists:

```bash
python graphpub/app.py \
    --query-endpoint http://localhost:3030/test/sparql \
    --update-endpoint http://localhost:3030/test/update \
    --target-base http://localhost:8080/ \
    --target-graph http://localhost:3030/test \
    --source-path ./data \
    --purge
```

## Issues

Please feel free to report any issues on the GitHub issue tracker.

## License

This code is copyrighted and released under the [MIT license](http://opensource.org/licenses/MIT).
