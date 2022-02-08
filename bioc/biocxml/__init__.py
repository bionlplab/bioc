"""
BioC XML encoder and decoder
"""
from typing import TextIO, Union, BinaryIO
from contextlib import contextmanager

from ..bioc import BioCCollection
from ..constants import BioCVersion
from .decoder import BioCXMLDocumentReader
from .decoder import load as load1, loads as loads1
from .decoder2 import BioCXMLDocumentReader as BioCXMLDocumentReader2
from .decoder2 import load as load2, loads as loads2
from .encoder import BioCXMLDocumentWriter
from .encoder import dump as dump1, dumps as dumps1
from .encoder2 import BioCXMLDocumentWriter as BioCXMLDocumentWriter2
from .encoder2 import dump as dump2, dumps as dumps2

__all__ = ['load', 'loads', 'dump', 'dumps', 'iterparse']


def load(fp: TextIO, version: BioCVersion = BioCVersion.V1) -> BioCCollection:
    """
    Deserialize ``fp`` (a ``.read()``-supporting file-like object containing a BioC collection)
    to a BioC collection object.
    """
    if version == BioCVersion.V1:
        return load1(fp)
    elif version == BioCVersion.V2:
        return load2(fp)
    else:
        raise ValueError


def loads(s: str, version: BioCVersion = BioCVersion.V1) -> BioCCollection:
    """
    Deserialize ``s`` (a ``str`` instance containing a BioC collection) to a BioC collection object.
    """
    if version == BioCVersion.V1:
        return loads1(s)
    elif version == BioCVersion.V2:
        return loads2(s)
    else:
        raise ValueError


def dump(collection: BioCCollection, fp: TextIO, version: BioCVersion = BioCVersion.V1, **kwargs):
    """
    Serialize ``collection`` as a BioC formatted stream to ``fp``.
    """
    if version == BioCVersion.V1:
        return dump1(collection, fp, **kwargs)
    elif version == BioCVersion.V2:
        return dump2(collection, fp, **kwargs)
    else:
        raise ValueError


def dumps(collection: BioCCollection, version: BioCVersion = BioCVersion.V1, **kwargs) -> str:
    """
    Serialize ``collection`` to a BioC formatted ``str``.
    """
    if version == BioCVersion.V1:
        return dumps1(collection, **kwargs)
    elif version == BioCVersion.V2:
        return dumps2(collection, **kwargs)
    else:
        raise ValueError


@contextmanager
def iterparse(source: Union[str, BinaryIO], version: BioCVersion = BioCVersion.V1):
    if version == BioCVersion.V1:
        reader = BioCXMLDocumentReader(source)
    elif version == BioCVersion.V2:
        reader = BioCXMLDocumentReader2(source)
    else:
        raise ValueError
    yield reader


@contextmanager
def iterwrite(file, encoding='utf8', standalone=True, version: BioCVersion = BioCVersion.V1):
    if version == BioCVersion.V1:
        writer = BioCXMLDocumentWriter(file, encoding, standalone)
    elif version == BioCVersion.V2:
        writer = BioCXMLDocumentWriter2(file, encoding, standalone)
    else:
        raise ValueError
    yield writer
    writer.close()
