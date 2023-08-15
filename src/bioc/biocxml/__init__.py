"""
BioC XML encoder and decoder
"""
from typing import TextIO, Union, BinaryIO
from contextlib import contextmanager

from .decoder import BioCXMLDocumentReader
from .decoder import load, loads
from .encoder import BioCXMLDocumentWriter
from .encoder import dump, dumps

__all__ = ['load', 'loads', 'dump', 'dumps', 'iterparse']


@contextmanager
def iterparse(source: Union[str, BinaryIO]):
    reader = BioCXMLDocumentReader(source)
    yield reader


@contextmanager
def iterwrite(file, encoding='utf8', standalone=True):
    writer = BioCXMLDocumentWriter(file, encoding, standalone)
    yield writer
    writer.close()
