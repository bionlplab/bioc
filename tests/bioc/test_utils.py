from pathlib import Path

import pytest

import bioc


def test_get_text():
    file = Path(__file__).parent / 'everything.xml'
    with open(file, encoding='utf8') as fp:
        collection = bioc.load(fp)

    assert (0, 'abcdefghijklmnopqrstuvwxyz') == bioc.get_text(collection.documents[0])
    assert (27, 'abcdefg测试Non-ASCII') == bioc.get_text(collection.documents[1].passages[0])
    assert (0, '\n' * 27 + 'abcdefg测试Non-ASCII') == bioc.get_text(collection.documents[1])

    with pytest.raises(ValueError):
        next(bioc.get_text('Foo'))
