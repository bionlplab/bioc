"""
BioC data structures and encoder/decoder for Python
"""
from .bioc import *

__all__ = ['BioCAnnotation', 'BioCCollection', 'BioCDocument', 'BioCLocation', 'BioCNode',
           'BioCPassage', 'BioCRelation', 'BioCSentence', 'BioCFileType', 'BioCVersion',
           'BioCDataModel',
           'validate', 'annotations', 'sentences', 'get_text', 'pretty_print',
           'biocxml', 'biocjson',
           'BioCJsonIterWriter', 'toJSON', 'BioCJsonIterReader', 'fromJSON', 'biocjson',
           'load', 'loads', 'load']
