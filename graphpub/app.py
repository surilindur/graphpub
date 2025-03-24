#!/bin/python

"""The application itself, for use from the command line."""

from typing import Dict
from logging import basicConfig
from logging import addLevelName
from logging import INFO
from logging import ERROR
from logging import WARNING
from logging import DEBUG
from pathlib import Path
from argparse import ArgumentParser
from argparse import BooleanOptionalAction
from argparse import Namespace

from rdflib.term import URIRef

from publish import publish_graph

LOG_LEVELS: Dict[str, int] = {
    "info": INFO,
    "error": ERROR,
    "warning": WARNING,
    "debug": DEBUG,
}


class CommandLineArgs(Namespace):
    """Extension of the arguments namespace to account for custom options."""

    query_endpoint: URIRef
    update_endpoint: URIRef | None
    log_level: str
    target_base: URIRef
    target_graph: URIRef
    source_path: Path
    purge: bool


def setup_logging(level: str) -> None:
    """Configure the logging with basic formatting and level names."""
    for level_name, level_value in LOG_LEVELS.items():
        addLevelName(level=level_value, levelName=level_name)
    basicConfig(
        level=LOG_LEVELS[level],
        format="[%(levelname)s] %(message)s",
    )


def parse_args() -> CommandLineArgs:
    """Parse the command line arguments provided by the user."""
    parser = ArgumentParser(
        description="Publish local files to a SPARQL endpoint as a graph",
    )
    parser.add_argument(
        "--query-endpoint",
        type=URIRef,
        help="The endpoint URI for accessing the data",
    )
    parser.add_argument(
        "--update-endpoint",
        type=URIRef,
        help="The endpoint URI for updating the data, defaults to query endpoint",
        required=False,
    )
    parser.add_argument(
        "--target-base",
        type=URIRef,
        help="The base URI, mapped to source path, for completing all relative URIs",
    )
    parser.add_argument(
        "--target-graph",
        type=URIRef,
        help="The URI of the graph to publish in",
    )
    parser.add_argument(
        "--source-path",
        type=lambda p: Path(p).resolve(),
        help="The path to the input data on local filesystem",
    )
    parser.add_argument(
        "--purge",
        action=BooleanOptionalAction,
        help="Whether the target graph should be purged before publishing",
    )
    parser.add_argument(
        "--log-level",
        choices=LOG_LEVELS.keys(),
        default="info",
        help="The log level to use",
    )
    return parser.parse_args(namespace=CommandLineArgs)


def main() -> None:
    """The main entrypoint."""
    args = parse_args()
    setup_logging(level=args.log_level)
    publish_graph(
        query_endpoint=args.query_endpoint,
        update_endpoint=args.update_endpoint,
        target_graph=args.target_graph,
        target_base=args.target_base,
        source_path=args.source_path,
        purge=args.purge,
    )


if __name__ == "__main__":
    main()
