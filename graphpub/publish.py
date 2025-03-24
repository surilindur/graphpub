"""Functionality for publishing a graph from local files on the filesystem."""

from os.path import splitext
from time import perf_counter
from typing import List
from pathlib import Path
from logging import info
from logging import debug
from logging import exception
from logging import warning

from rdflib.term import URIRef

from constants import RDF_FILE_EXTENSIONS
from endpoint import get_graph


def publish_graph(
    query_endpoint: URIRef,
    update_endpoint: URIRef | None,
    target_graph: URIRef,
    target_base: URIRef,
    source_path: Path,
    purge: bool,
) -> None:
    """
    Publish a graph from local files on the filesystem,
    by mapping the source path to the base URI,
    and all nested relative paths to relative URIs below this base.
    """
    assert source_path.exists(), f"Source path does not exist: {source_path}"

    info(f"Publishing graph from {source_path}")
    info(f"Publishing to {update_endpoint or query_endpoint}")

    graph = get_graph(
        query_endpoint=query_endpoint,
        update_endpoint=update_endpoint,
        identifier=target_graph,
        purge=purge,
    )

    # Keep the paths to process in a list to avoid recursion
    path_queue: List[Path] = [source_path]

    start_time = perf_counter()

    while path_queue:
        path = path_queue.pop(0)  # pop the first element, not the last
        if path.is_file():
            relative_path, file_ext = splitext(path.relative_to(source_path).as_posix())
            if file_ext in RDF_FILE_EXTENSIONS:
                try:
                    info(f"Parse {path}")
                    path_uri = URIRef(value=relative_path, base=target_base)
                    debug(f"Path URI mapped to {path_uri}")
                    graph.parse(source=path, publicID=path_uri)
                except Exception as ex:
                    exception(ex)
            else:
                warning(f"Skipping {path} due to unsupported extension")
        elif path.is_dir():
            path_queue.extend(path.iterdir())
        else:
            warning(f"Skipping {path}")

    duration_seconds = perf_counter() - start_time

    info(f"Published in {duration_seconds:.3f} seconds")
