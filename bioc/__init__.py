"""
BioC data structures and encoder/decoder for Python
"""
from .bioc import BioCCollection, BioCDocument, BioCPassage, BioCSentence, BioCAnnotation, \
    BioCRelation, BioCLocation, BioCNode
from .biocitertools import annotations, relations, sentences
from .biocxml import load, loads, BioCXMLDocumentReader, dumps, dump, BioCXMLDocumentWriter
from .constants import PASSAGE, SENTENCE, DOCUMENT
from .utils import get_text, pretty_print
from .validator import validate

__all__ = ['BioCAnnotation', 'BioCCollection', 'BioCDocument', 'BioCLocation', 'BioCNode',
           'BioCPassage', 'BioCRelation', 'BioCSentence', 'load', 'loads', 'dump', 'dumps',
           'validate', 'annotations', 'sentences', 'get_text', 'pretty_print',
           'BioCXMLDocumentWriter', 'BioCXMLDocumentReader', 'biocjson']
