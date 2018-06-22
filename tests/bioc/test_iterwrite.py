import tempfile

import os

from .utils import assert_everything
from ..context import bioc


def test_iterwrite():
    src = os.path.join(os.path.dirname(__file__), 'everything.xml')
    with open(src, encoding='utf8') as fp:
        collection = bioc.load(fp)

    tmp = tempfile.NamedTemporaryFile()
    with bioc.iterwrite(tmp.name, collection) as writer:
        for document in collection.documents:
            writer.writedocument(document)

    with open(tmp.name, encoding='utf8') as fp:
        collection = bioc.load(fp)

    assert_everything(collection)
