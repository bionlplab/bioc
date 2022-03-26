"""
BioC data structures and encoder/decoder for Python
"""
from .bioc import BioCAnnotation, BioCCollection, BioCDocument, BioCLocation, BioCNode, BioCPassage, \
    BioCRelation, BioCSentence, BioCDataModel
from .validator import validate
from .biocitertools import annotations, relations, sentences
from .utils import get_text, pretty_print
from .biocxml import loads, load, dump, dumps
from .constants import PASSAGE, DOCUMENT, SENTENCE, BioCVersion


__all__ = ['BioCAnnotation', 'BioCCollection', 'BioCDocument', 'BioCLocation', 'BioCNode',
           'BioCPassage', 'BioCRelation', 'BioCSentence', 'BioCVersion',
           'BioCDataModel',
           'validate', 'annotations', 'relations', 'sentences', 'get_text', 'pretty_print',
           'biocxml', 'biocjson',
           'load', 'loads', 'dump', 'dumps',
           'PASSAGE', 'DOCUMENT', 'SENTENCE']
