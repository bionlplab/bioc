"""
BioC JSON and JSON lines encoder and decoder
"""
from bioc.biocjson.decoder import loads, load, BioCJsonIterReader
from bioc.biocjson.encoder import dumps, dump, BioCJsonIterWriter

__all__ = ['BioCJsonIterReader', 'BioCJsonIterWriter', 'dumps', 'dump', 'load', 'loads']
