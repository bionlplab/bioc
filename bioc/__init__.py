__author__ = 'Yifan Peng'

__version__ = '1.0.0-SNAPSHOT'

from bioc import BioCCollection, BioCDocument, BioCPassage, BioCSentence, BioCAnnotation, \
    BioCRelation, BioCLocation, BioCNode, parse
from iterparse import iterparse

__all__ = ['BioCAnnotation', 'BioCCollection', 'BioCDocument', 'BioCLocation', 'BioCNode',
           'BioCPassage', 'BioCRelation', 'BioCSentence', 'parse', 'iterparse']
