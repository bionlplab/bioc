"""
BioC data structures and encoder/decoder for Python
"""

from .bioc import BioCCollection, BioCDocument, BioCPassage, BioCSentence, BioCAnnotation, \
    BioCRelation, BioCLocation, BioCNode, BioCDataModel
from .biocitertools import annotations, relations, sentences
from .biocjson import BioCJsonIterWriter, toJSON, BioCJsonIterReader, fromJSON
from .biocjson import load as jsonload, loads as jsonloads, dump as jsondump, dumps as jsondumps
from .biocxml import load as xmlload, loads as xmlloads, dump as xmldump, dumps as xmldumps
from .constants import PASSAGE, SENTENCE, DOCUMENT, BioCFileType, BioCVersion
from .utils import get_text, pretty_print, shorten_text
from .validator import validate
from .biocio import load, loads, dump, dumps

# __all__ = ['BioCAnnotation', 'BioCCollection', 'BioCDocument', 'BioCLocation', 'BioCNode',
#            'BioCPassage', 'BioCRelation', 'BioCSentence', 'BioCFileType', 'BioCVersion',
#            'BioCDataModel',
#            'validate', 'annotations', 'sentences', 'get_text', 'pretty_print', 'shorten_text',
#            'biocxml', 'biocjson',
#            'BioCJsonIterWriter', 'toJSON', 'BioCJsonIterReader', 'fromJSON', 'biocjson',
#            'load', 'loads', 'dump', 'dumps',
#            'PASSAGE', 'SENTENCE', 'DOCUMENT',
#            'relations']


