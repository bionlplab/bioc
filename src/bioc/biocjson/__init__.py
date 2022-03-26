"""
BioC JSON and JSON lines encoder and decoder
"""
from .encoder import dumps, dump, toJSON, iterwriter
from .decoder import loads, load, fromJSON, iterreader


__all__ = ['iterwriter', 'iterreader',
           'dumps', 'dump', 'load', 'loads', 'toJSON', 'fromJSON']
