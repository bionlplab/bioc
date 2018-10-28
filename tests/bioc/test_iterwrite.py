import tempfile
from pathlib import Path

import bioc
from tests.utils import assert_everything


def test_iterwrite():
    file = Path(__file__).parent / 'everything.xml'
    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp)

    tmp = tempfile.NamedTemporaryFile()
    with bioc.iterwrite(tmp.name, collection) as writer:
        for document in collection.documents:
            writer.writedocument(document)

    with open(tmp.name, encoding='utf8') as fp:
        collection = bioc.load(fp)

    assert_everything(collection)
