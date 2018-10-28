import tempfile
from pathlib import Path

from bioc import biocjson
from tests.utils import assert_everything

file = Path(__file__).parent / 'everything.json'


def test_load():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)
    assert_everything(collection)


def test_loads():
    with open(file, encoding='utf8') as fp:
        s = fp.read()
    collection = biocjson.loads(s)
    assert_everything(collection)


def test_dump():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)
    tmp = tempfile.mktemp()
    with open(tmp, 'w', encoding='utf8') as fp:
        biocjson.dump(collection, fp)
    with open(tmp, encoding='utf8') as fp:
        collection = biocjson.load(fp)
    assert_everything(collection)


def test_dumps():
    with open(file, encoding='utf8') as fp:
        collection = biocjson.load(fp)
    s = biocjson.dumps(collection)
    collection = biocjson.loads(s)
    assert_everything(collection)
