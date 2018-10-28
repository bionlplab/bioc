import os
import tempfile
from pathlib import Path

import pytest

import bioc
from tests.utils import assert_everything

file = Path(__file__).parent / 'everything.xml'


def test_load():
    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp)
    assert_everything(collection)


def test_loads():
    with open(file, encoding='utf8') as fp:
        s = fp.read()
    collection = bioc.loads(s)
    assert_everything(collection)


def test_dump():
    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp)
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'w', encoding='utf8') as fp:
        bioc.dump(collection, fp)
    with open(tmp.name, encoding='utf8') as fp:
        collection = bioc.load(fp)
    assert_everything(collection)


def test_dumps():
    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp)
    s = bioc.dumps(collection)
    collection = bioc.loads(s)
    assert_everything(collection)


def test_validate():
    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp)
    bioc.validate(collection)


def test_BioCLocation():
    base = bioc.BioCLocation(1, 10)
    assert base != 'foo'
    assert base.end == 11

    loc = bioc.BioCLocation(1, 10)
    assert base == loc

    loc = bioc.BioCLocation(2, 9)
    assert base != loc
    assert loc in base
    assert base not in loc

    locs = {base, loc}
    assert base in locs
    assert loc in locs

    with pytest.raises(TypeError):
        assert 'foo' in base


def test_BioCNode():
    base = bioc.BioCNode('refid', 'role')
    assert base != 'foo'

    node = bioc.BioCNode('refid', 'role')
    assert base == node

    node = bioc.BioCNode('refid', 'role2')
    assert base != node

    nodes = {base, node}
    assert base in nodes
    assert node in nodes


def test_BioCAnnotation():
    base = bioc.BioCAnnotation()
    base.add_location(bioc.BioCLocation(1, 10))

    ann = bioc.BioCAnnotation()
    ann.add_location(bioc.BioCLocation(2, 9))

    assert ann in base
    assert base not in ann

    with pytest.raises(TypeError):
        assert 'foo' in base
