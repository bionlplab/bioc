"""
BioC data structures and encoder/decoder for Python
"""
from enum import Enum
from typing import TextIO

from .bioc import BioCCollection, BioCDocument, BioCPassage, BioCSentence, BioCAnnotation, \
    BioCRelation, BioCLocation, BioCNode
from .biocitertools import annotations, relations, sentences
from .biocjson import BioCJsonIterWriter, toJSON, BioCJsonIterReader, fromJSON
from .biocjson import load as jsonload, loads as jsonloads, dump as jsondump, dumps as jsondumps
from .biocxml import load as xmlload, loads as xmlloads, dump as xmldump, dumps as xmldumps
from .utils import get_text, pretty_print
from .validator import validate

DOCUMENT = 1
PASSAGE = 2
SENTENCE = 3


class BioCFileType(Enum):
    BIOC_XML = 1
    BIOC_JSON = 2


class BioCVersion(Enum):
    V1 = 1
    V2 = 2


__all__ = ['BioCAnnotation', 'BioCCollection', 'BioCDocument', 'BioCLocation', 'BioCNode',
           'BioCPassage', 'BioCRelation', 'BioCSentence', 'validate', 'annotations', 'sentences', 'get_text', 'pretty_print',
           'biocxml', 'biocjson',
           'BioCJsonIterWriter', 'toJSON', 'BioCJsonIterReader', 'fromJSON', 'biocjson']


def load(fp: TextIO, filetype: BioCFileType = BioCFileType.BIOC_XML, version: BioCVersion = BioCVersion.V1,
         **kwargs) -> BioCCollection:
    """
    Deserialize ``fp`` (a ``.read()``-supporting file-like object containing a BioC collection)
    to a BioC collection object.
    """
    if filetype == BioCFileType.BIOC_XML:
        return xmlload(fp, version)
    elif filetype == BioCFileType.BIOC_JSON:
        return jsonload(fp, **kwargs)
    else:
        raise ValueError


def loads(s: str, filetype: BioCFileType = BioCFileType.BIOC_XML, version: BioCVersion = BioCVersion.V1,
          **kwargs) -> BioCCollection:
    """
    Deserialize ``s`` (a ``str`` instance containing a BioC collection) to a BioC collection object.
    """
    if filetype == BioCFileType.BIOC_XML:
        return xmlloads(s, version)
    elif filetype == BioCFileType.BIOC_JSON:
        return jsonloads(s, **kwargs)
    else:
        raise ValueError


def dump(collection: BioCCollection, fp: TextIO, filetype: BioCFileType = BioCFileType.BIOC_XML,
         version: BioCVersion = BioCVersion.V1, **kwargs):
    """
    Serialize ``collection`` as a BioC formatted stream to ``fp``.
    """
    if filetype == BioCFileType.BIOC_XML:
        return xmldump(collection, fp, version, **kwargs)
    elif filetype == BioCFileType.BIOC_JSON:
        return jsondump(collection, fp, **kwargs)
    else:
        raise ValueError


def dumps(collection: BioCCollection, filetype: BioCFileType = BioCFileType.BIOC_XML,
          version: BioCVersion = BioCVersion.V1, **kwargs) -> str:
    """
    Serialize ``collection`` to a BioC formatted ``str``.
    """
    if filetype == BioCFileType.BIOC_XML:
        return xmldumps(collection, version, **kwargs)
    elif filetype == BioCFileType.BIOC_JSON:
        return jsondumps(collection, **kwargs)
    else:
        raise ValueError


