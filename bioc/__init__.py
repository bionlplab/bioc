from bioc.bioc import BioCCollection, BioCDocument, BioCPassage, BioCSentence, BioCAnnotation, BioCRelation, \
    BioCLocation, BioCNode
from bioc.biocitertools import annotations, relations, sentences
from bioc.utils import get_text, pretty_print
from bioc.validator import validate
from bioc.biocxml.decoder import load, loads, BioCXMLDocumentReader, read_xml
from bioc.biocxml.encoder import dumps, dump, BioCXMLDocumentWriter, to_xml
from bioc.constants import PASSAGE, SENTENCE, DOCUMENT
import bioc.biocjson as biocjson


__all__ = ['BioCAnnotation', 'BioCCollection', 'BioCDocument', 'BioCLocation', 'BioCNode',
           'BioCPassage', 'BioCRelation', 'BioCSentence', 'load', 'loads', 'dump', 'dumps',
           'merge', 'validate', 'annotations', 'sentences', 'get_text', 'pretty_print',
           'BioCXMLDocumentWriter', 'BioCXMLDocumentReader', 'biocjson']


def merge(output: str, *input: str):
    """
    Merge multiple BioC files into one.

    Args:
        output: output BioC file name
        input: input BioC file names
    """
    collection = None
    for src in input:
        with open(src) as fp:
            tmp = load(fp)
        if collection is None:
            collection = tmp
        else:
            for document in tmp.documents:
                collection.add_document(document)
    with open(output, 'w') as fp:
        dump(collection, fp)

