from bioc.brat.brat import BratNote
from bioc.brat.decoder import loads_brat_note
from bioc.brat.encoder import dumps_brat_note


def get_note(id, type, refid, text):
    n = BratNote()
    n.id = id
    n.type = type
    n.refid = refid
    n.text = text
    return n


def test_note():
    base = get_note('#1', 'type', 'E1', 'text')
    actual = get_note('#1', 'type', 'E1', 'text')
    assert base == actual

    diff = get_note('#2', 'type', 'E1', 'text')
    assert base != diff

    diff = get_note('#1', 'type2', 'E1', 'text')
    assert base != diff

    diff = get_note('#1', 'type', 'E2', 'text')
    assert base != diff

    diff = get_note('#1', 'type', 'E1', 'text2')
    assert base != diff

    line = '#1\ttype E1\ttext'
    actual = loads_brat_note(line)
    assert base == actual

    assert line == dumps_brat_note(base)
