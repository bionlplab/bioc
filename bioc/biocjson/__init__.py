"""
BioC JSON and JSON lines encoder and decoder
"""
from .encoder import dumps, dump, BioCJsonIterWriter, toJSON
from .decoder import loads, load, BioCJsonIterReader, fromJSON

__all__ = ['BioCJsonIterReader', 'BioCJsonIterWriter',
           'dumps', 'dump', 'load', 'loads', 'toJSON', 'fromJSON']
