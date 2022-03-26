"""
BioC JSON encoder
"""
import io
import json
from contextlib import contextmanager
from typing import Dict, Union, TextIO

from bioc.bioc import BioCPassage, BioCNode, BioCAnnotation, BioCLocation, BioCRelation, \
    BioCSentence, BioCCollection, BioCDocument


BIOC_OBJ = Union[BioCCollection, BioCDocument, BioCPassage, BioCSentence]


def dumps(obj: BIOC_OBJ, **kwargs) -> str:
    """
    Serialize a BioC ``obj`` to a JSON formatted ``str``. kwargs are passed to json.
    """
    return json.dumps(obj, cls=BioCJSONEncoder, **kwargs)


def dump(obj: BIOC_OBJ, fp: TextIO, **kwargs):
    """
    Serialize ``obj`` as a JSON formatted stream to ``fp``
    (a ``.write()``-supporting file-like object). kwargs are passed to json.
    """
    return json.dump(obj, fp, cls=BioCJSONEncoder, **kwargs)


class BioCJSONEncoder(json.JSONEncoder):
    """
    Extensible BioC JSON encoder for BioC data structures.
    """

    def default(self, o):
        if isinstance(o, BioCLocation):
            return {
                'offset': o.offset,
                'length': o.length,
            }
        if isinstance(o, BioCAnnotation):
            return {
                'id': o.id,
                'infons': o.infons,
                'text': o.text,
                'locations': [self.default(l) for l in o.locations],
            }
        if isinstance(o, BioCNode):
            return {
                'refid': o.refid,
                'role': o.role,
            }
        if isinstance(o, BioCRelation):
            return {
                'id': o.id,
                'infons': o.infons,
                'nodes': [self.default(n) for n in o.nodes]
            }
        if isinstance(o, BioCSentence):
            return {
                'bioctype': 'BioCSentence',
                'offset': o.offset,
                'infons': o.infons,
                'text': o.text,
                'annotations': [self.default(a) for a in o.annotations],
                'relations': [self.default(r) for r in o.relations],
            }
        if isinstance(o, BioCPassage):
            return {
                'bioctype': 'BioCPassage',
                'offset': o.offset,
                'infons': o.infons,
                'text': o.text,
                'sentences': [self.default(s) for s in o.sentences],
                'annotations': [self.default(a) for a in o.annotations],
                'relations': [self.default(r) for r in o.relations],
            }
        if isinstance(o, BioCDocument):
            return {
                'bioctype': 'BioCDocument',
                'id': o.id,
                'infons': o.infons,
                'passages': [self.default(p) for p in o.passages],
                'annotations': [self.default(a) for a in o.annotations],
                'relations': [self.default(r) for r in o.relations],
            }
        if isinstance(o, BioCCollection):
            return {
                'bioctype': 'BioCCollection',
                'source': o.source,
                'date': o.date,
                'key': o.key,
                'version': o.version,
                'infons': o.infons,
                'documents': [self.default(d) for d in o.documents],
            }
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o)


class BioCJsonIterWriter:
    """
    Writer for the json lines format.
    """

    def __init__(self, fp: TextIO):
        self.fp = fp

    def write(self, obj: Union[BioCDocument, BioCPassage, BioCSentence]):
        """
        Encode and write a BioC obj (an instance of BioCDocument, BioCPassage, or BioCSentence).
        """
        self.fp.write(json.dumps(BioCJSONEncoder().default(obj)) + '\n')


@contextmanager
def iterwriter(file: Union[str, TextIO]) -> BioCJsonIterWriter:
    """
    Write a bioc object to a file incrementally.
    """
    if isinstance(file, io.TextIOBase):
        writer = BioCJsonIterWriter(file)
        yield writer
    else:
        with open(file, 'w') as fp:
            writer = BioCJsonIterWriter(fp)
            yield writer


def toJSON(o) -> Dict:
    """
    Convert a BioC obj (an instance of BioCDocument, BioCPassage, or BioCSentence)
    to a Python `dict`
    """
    return BioCJSONEncoder().default(o)
