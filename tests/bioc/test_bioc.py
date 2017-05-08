import tempfile

import os
from .utils import assert_everything
from ..context import bioc

src = os.path.join(os.path.dirname(__file__), 'everything.xml')


def test_load():
    with open(src) as fp:
        collection = bioc.load(fp)
    assert_everything(collection)


def test_loads():
    with open(src) as fp:
        s = fp.read()
    collection = bioc.loads(s)
    assert_everything(collection)


def test_dump():
    with open(src) as fp:
        collection = bioc.load(fp)
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'w') as fp:
        bioc.dump(collection, fp)
    with open(tmp.name) as fp:
        collection = bioc.load(fp)
    assert_everything(collection)


def test_dumps():
    with open(src) as fp:
        collection = bioc.load(fp)
    s = bioc.dumps(collection)
    collection = bioc.loads(s)
    assert_everything(collection)


def test_validate():
    with open(src) as fp:
        collection = bioc.load(fp)
    bioc.validate(collection)
