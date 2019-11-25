"""
BioC JSON encoder
"""

import json
from typing import Dict, Union, TextIO

from bioc.bioc import BioCPassage, BioCNode, BioCAnnotation, BioCLocation, BioCRelation, \
    BioCSentence, BioCCollection, BioCDocument
from bioc.constants import DOCUMENT, PASSAGE, SENTENCE


BIOC_OBJ = Union[BioCCollection, BioCDocument, BioCPassage, BioCSentence]


def dumps(obj: BIOC_OBJ, **kwargs) -> str:
    """
    Serialize a BioC ``obj`` to a JSON formatted ``str``.
    """
    return json.dumps(obj, cls=BioCJSONEncoder, **kwargs)


def dump(obj: BIOC_OBJ, fp: TextIO, **kwargs):
    """
    Serialize obj as a JSON formatted stream to ``fp`` (a ``.write()``-supporting file-like object)
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
                'offset': o.offset,
                'infons': o.infons,
                'text': o.text,
                'annotations': [self.default(a) for a in o.annotations],
                'relations': [self.default(r) for r in o.relations],
            }
        if isinstance(o, BioCPassage):
            return {
                'offset': o.offset,
                'infons': o.infons,
                'text': o.text,
                'sentences': [self.default(s) for s in o.sentences],
                'annotations': [self.default(a) for a in o.annotations],
                'relations': [self.default(r) for r in o.relations],
            }
        if isinstance(o, BioCDocument):
            return {
                'id': o.id,
                'infons': o.infons,
                'passages': [self.default(p) for p in o.passages],
                'annotations': [self.default(a) for a in o.annotations],
                'relations': [self.default(r) for r in o.relations],
            }
        if isinstance(o, BioCCollection):
            return {
                'source': o.source,
                'date': o.date,
                'key': o.key,
                'infons': o.infons,
                'documents': [self.default(d) for d in o.documents],
            }
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o)


class BioCJsonIterWriter:
    """
    Writer for the json lines format.
    """

    def __init__(self, fp: TextIO, level: int):
        if level not in {DOCUMENT, PASSAGE, SENTENCE}:
            raise ValueError(f'Unrecognized level {level}')

        self.fp = fp
        self.level = level

    def write(self, obj: Union[BioCDocument, BioCPassage, BioCSentence]):
        """
        Encode and write a single object.

        Args:
            obj: an instance of BioCDocument, BioCPassage, or BioCSentence

        Returns:

        """
        if self.level == DOCUMENT and not isinstance(obj, BioCDocument):
            raise ValueError(f'{self.fp}: can only write BioCDocument '
                             f'because of the level {self.level}')
        if self.level == PASSAGE and not isinstance(obj, BioCPassage):
            raise ValueError(f'{self.fp}: can only write BioCPassage '
                             f'because of the level {self.level}')
        if self.level == SENTENCE and not isinstance(obj, BioCSentence):
            raise ValueError(f'{self.fp}: can only write BioCSentence '
                             f'because of the level {self.level}')
        self.fp.write(json.dumps(BioCJSONEncoder().default(obj)) + '\n')


def toJSON(o) -> Dict:
    return BioCJSONEncoder().default(o)