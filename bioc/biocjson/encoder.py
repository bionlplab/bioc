import json

import jsonlines

from bioc.bioc import BioCPassage, BioCNode, BioCAnnotation, BioCLocation, BioCRelation, \
    BioCSentence, BioCCollection, BioCDocument
from bioc.constants import DOCUMENT, PASSAGE, SENTENCE


def dumps(obj, **kwargs) -> str:
    """
    Serialize a BioC ``obj`` to a JSON formatted ``str``.
    """
    return json.dumps(obj, cls=BioCJSONEncoder, **kwargs)


def dump(obj, fp, **kwargs):
    """
    Serialize obj as a JSON formatted stream to fp (a .write()-supporting file-like object)
    """
    return json.dump(obj, fp, cls=BioCJSONEncoder, **kwargs)


class BioCJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BioCLocation):
            return {
                'offset': obj.offset,
                'length': obj.length,
            }
        elif isinstance(obj, BioCAnnotation):
            return {
                'id': obj.id,
                'infons': obj.infons,
                'text': obj.text,
                'locations': [self.default(l) for l in obj.locations],
            }
        elif isinstance(obj, BioCNode):
            return {
                'refid': obj.refid,
                'role': obj.role,
            }
        elif isinstance(obj, BioCRelation):
            return {
                'id': obj.id,
                'infons': obj.infons,
                'nodes': [self.default(n) for n in obj.nodes]
            }
        elif isinstance(obj, BioCSentence):
            return {
                'offset': obj.offset,
                'infons': obj.infons,
                'text': obj.text,
                'annotations': [self.default(a) for a in obj.annotations],
                'relations': [self.default(r) for r in obj.relations],
            }
        elif isinstance(obj, BioCPassage):
            return {
                'offset': obj.offset,
                'infons': obj.infons,
                'text': obj.text,
                'sentences': [self.default(s) for s in obj.sentences],
                'annotations': [self.default(a) for a in obj.annotations],
                'relations': [self.default(r) for r in obj.relations],
            }
        elif isinstance(obj, BioCDocument):
            return {
                'id': obj.id,
                'infons': obj.infons,
                'passages': [self.default(p) for p in obj.passages],
                'annotations': [self.default(a) for a in obj.annotations],
                'relations': [self.default(r) for r in obj.relations],
            }
        elif isinstance(obj, BioCCollection):
            return {
                'source': obj.source,
                'date': obj.date,
                'key': obj.key,
                'infons': obj.infons,
                'documents': [self.default(d) for d in obj.documents],
            }
        return json.JSONEncoder.default(self, obj)


class BioCJsonIterWriter(object):
    def __init__(self, file, level):
        if level not in {DOCUMENT, PASSAGE, SENTENCE}:
            raise ValueError(f'Unrecognized level: {level}')

        self.writer = jsonlines.open(file, 'w')
        self.level = level

    def write(self, obj):
        if self.level == DOCUMENT and not isinstance(obj, BioCDocument):
            raise ValueError
        if self.level == PASSAGE and not isinstance(obj, BioCPassage):
            raise ValueError
        if self.level == SENTENCE and not isinstance(obj, BioCSentence):
            raise ValueError
        self.writer.write(BioCJSONEncoder().default(obj))

    def close(self):
        self.writer.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
