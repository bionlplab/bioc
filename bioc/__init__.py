"""
BioC data structures and encoder/decoder for Python
"""
from typing import TextIO

from .bioc import BioCCollection, BioCDocument, BioCPassage, BioCSentence, BioCAnnotation, \
    BioCRelation, BioCLocation, BioCNode
from .biocitertools import annotations, relations, sentences
from .biocjson import decoder as biocjsondecoder, encoder as biocjsonencoder, BioCJsonIterWriter, toJSON, \
    BioCJsonIterReader, fromJSON
from .biocxml import decoder as biocxmldecoder, encoder as biocxmlencoder, BioCXMLDocumentReader, BioCXMLDocumentWriter
from .constants import PASSAGE, SENTENCE, DOCUMENT, BioCFileType
from .utils import get_text, pretty_print
from .validator import validate

__all__ = ['BioCAnnotation', 'BioCCollection', 'BioCDocument', 'BioCLocation', 'BioCNode',
           'BioCPassage', 'BioCRelation', 'BioCSentence', 'BioCFileType',
           'validate', 'annotations', 'sentences', 'get_text', 'pretty_print',
           'BioCXMLDocumentWriter', 'BioCXMLDocumentReader', 'biocxml',
           'BioCJsonIterWriter', 'toJSON', 'BioCJsonIterReader', 'fromJSON', 'biocjson']


def load(fp: TextIO, filetype: BioCFileType = BioCFileType.BIOC_XML, **kwargs) -> BioCCollection:
    """
    Deserialize ``fp`` (a ``.read()``-supporting file-like object containing a BioC collection)
    to a BioC collection object.
    """
    if filetype == BioCFileType.BIOC_XML:
        return biocxmldecoder.load(fp)
    elif filetype == BioCFileType.BIOC_JSON:
        return biocjsondecoder.load(fp, **kwargs)
    else:
        raise ValueError


def loads(s: str, filetype: BioCFileType = BioCFileType.BIOC_XML, **kwargs) -> BioCCollection:
    """
    Deserialize ``s`` (a ``str`` instance containing a BioC collection) to a BioC collection object.
    """
    if filetype == BioCFileType.BIOC_XML:
        return biocxmldecoder.loads(s)
    elif filetype == BioCFileType.BIOC_JSON:
        return biocjsondecoder.loads(s, **kwargs)
    else:
        raise ValueError


def dump(collection: BioCCollection, fp: TextIO, filetype: BioCFileType = BioCFileType.BIOC_XML, **kwargs):
    """
    Serialize ``collection`` as a BioC formatted stream to ``fp``.
    """
    if filetype == BioCFileType.BIOC_XML:
        return biocxmlencoder.dump(collection, fp, **kwargs)
    elif filetype == BioCFileType.BIOC_JSON:
        return biocjsonencoder.dump(collection, fp, **kwargs)
    else:
        raise ValueError


def dumps(collection: BioCCollection, filetype: BioCFileType = BioCFileType.BIOC_XML, **kwargs) -> str:
    """
    Serialize ``collection`` to a BioC formatted ``str``.
    """
    if filetype == BioCFileType.BIOC_XML:
        return biocxmlencoder.dumps(collection, **kwargs)
    elif filetype == BioCFileType.BIOC_JSON:
        return biocjsonencoder.dumps(collection, **kwargs)
    else:
        raise ValueError
