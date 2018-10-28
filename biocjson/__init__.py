from bioc import DOCUMENT
from biocjson.jsondecoder import parse_doc, parse_passage, parse_sentence, load, loads, BioCJsonDecoderIter
from biocjson.jsonencoder import BioCJSONEncoder, BioCJsonWriter
from biocjson.jsonencoder import dumps, dump

__all__ = ['iterparse', 'iterwrite', 'dumps', 'dump', 'load', 'loads']


def iterparse(file, level=DOCUMENT):
    reader = BioCJsonDecoderIter(file, level)
    return reader


def iterwrite(file, level=DOCUMENT):
    writer = BioCJsonWriter(file, level)
    return writer
