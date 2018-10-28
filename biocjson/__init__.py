from biocjson.jsonencoder import dumps, dump

from bioc import DOCUMENT, PASSAGE, SENTENCE, BioCDocument, BioCPassage, BioCSentence

from biocjson.jsondecoder import parse_doc, parse_passage, parse_sentence
from biocjson.jsonencoder import BioCJSONEncoder, BioCJsonWriter
import jsonlines
from contextlib import contextmanager


def iterparse(file, level=DOCUMENT):
    assert level in (DOCUMENT, PASSAGE, SENTENCE), 'Unrecognized level: %s' % level
    with jsonlines.open(file) as reader:
        for obj in reader:
            if level == DOCUMENT:
                yield parse_doc(obj)
            elif level == PASSAGE:
                yield parse_passage(obj)
            elif level == SENTENCE:
                yield parse_sentence(obj)



@contextmanager
def iterwrite(file, level=DOCUMENT):
    assert level in (DOCUMENT, PASSAGE, SENTENCE), 'Unrecognized level: %s' % level
    writer = BioCJsonWriter(file, level)
    yield writer
    writer.close()




