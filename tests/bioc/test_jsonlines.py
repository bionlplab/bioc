import tempfile
from copy import deepcopy
from pathlib import Path

import jsonlines

import bioc
from bioc.jsondecoder import parse_doc
from bioc.jsonencoder import BioCJSONEncoder
from tests.bioc.utils import assert_everything

src = Path(__file__).parent / 'everything.json'


def test_jsonlines():
    with open(src, encoding='utf8') as fp:
        collection = bioc.jsonload(fp)

    tmp = tempfile.NamedTemporaryFile()
    with jsonlines.open(tmp.name, mode='w') as writer:
        for doc in collection.documents:
            writer.write(BioCJSONEncoder().default(doc))

    collection2 = deepcopy(collection)
    del collection2.documents[:]
    with jsonlines.open(tmp.name) as reader:
        for obj in reader:
            doc = parse_doc(obj)
            collection2.add_document(doc)
    assert_everything(collection2)
