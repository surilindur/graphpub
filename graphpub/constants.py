"""Various constants used within the application."""

from typing import Set
from platform import python_version
from platform import system
from platform import machine
from platform import python_implementation

from rdflib import __version__ as rdflib_version

RDF_FILE_EXTENSIONS: Set[str] = set(
    (
        ".jsonld",
        ".n3",
        ".nq",
        ".nt",
        ".hext",
        ".xml",
        ".trig",
        ".trix",
        ".ttl",
    )
)

HTTP_USER_AGENT: str = " ".join(
    (
        f"Graphpub/0.1 ({system()} {machine()})",
        f"RDFLib/{rdflib_version}",
        f"{python_implementation()}/{python_version()}",
    )
)
