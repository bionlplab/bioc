"""
BioC XML encoder and decoder
"""
from bioc.biocxml.encoder import dump, dumps, BioCXMLDocumentWriter
from bioc.biocxml.decoder import load, loads, BioCXMLDocumentReader

__all__ = ['BioCXMLDocumentReader', 'BioCXMLDocumentWriter',
           'dumps', 'dump', 'load', 'loads']
