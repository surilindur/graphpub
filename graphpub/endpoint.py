"""Functionality related to SPARQL endpoints."""

from os import getenv
from typing import Tuple
from logging import warning

from rdflib.term import URIRef
from rdflib.graph import Graph
from rdflib.graph import Dataset
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore

from constants import HTTP_USER_AGENT


def get_auth() -> Tuple[str, str] | None:
    """
    Generate an auth tuple for use in RDFLib's stores,
    if the environment variables are defined.
    When not defined, returns None.
    """
    username = getenv("SPARQL_USERNAME")
    password = getenv("SPARQL_PASSWORD")
    return (username, password) if username and password else None


def get_graph(
    query_endpoint: URIRef,
    update_endpoint: URIRef | None,
    identifier: URIRef,
    purge: bool,
) -> Graph:
    """
    Access a read-write graph from the given endpoint, identified by the identifier.
    When the update endpoint URI is not defined, the query endpoint is used for both.
    Optionally, remove an existing graph and create a fresh one.
    """
    store = SPARQLUpdateStore(
        query_endpoint=query_endpoint,
        update_endpoint=update_endpoint,
        method="POST_FORM",
        headers={"User-Agent": HTTP_USER_AGENT},
        auth=get_auth(),
    )
    dataset = Dataset(store=store)
    if purge:
        warning(f"Removing graph {identifier}")
        dataset.remove_graph(g=identifier)
    return dataset.add_graph(g=identifier)
