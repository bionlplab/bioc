from typing import TextIO

from bioc.brat.brat import BratDocument, BratEntity, BratEvent, BratRelation, BratNote, BratAttribute, BratEquivRelation


def loads_brat_attribute(s: str) -> BratAttribute:
    """
    ID [tab] TYPE REFID [FLAG1 FLAG2 ...]
    """
    toks = s.split('\t')
    assert len(toks) == 2, 'Illegal format: %s' % s

    att = BratAttribute()
    att.id = toks[0]

    toks = toks[1].split(' ')
    assert len(toks) >= 2, 'Illegal format: %s' % s

    att.type = toks[0]
    att.refid = toks[1]
    for tok in toks[2:]:
        att.add_attribute(tok)
    return att


def loads_brat_entity(s: str) -> BratEntity:
    """
    ID [tab] TYPE START END [tab] TEXT

    ID [tab] TYPE START END[;START END]* [tab] TEXT
    """
    toks = s.split('\t')
    assert len(toks) == 3, 'Illegal format: %s' % s

    entity = BratEntity()
    entity.id = toks[0]
    entity.text = toks[2]

    i = toks[1].find(' ')
    assert i != -1, 'Illegal format: %s' % s
    entity.type = toks[1][:i]

    for loc in toks[1][i+1:].split(';'):
        i = loc.find(' ')
        assert i != -1, 'Illegal format: %s' % s
        entity.add_span(int(loc[:i]), int(loc[i+1:]))

    return entity


def loads_brat_equiv(s: str) -> BratEquivRelation:
    """
    * [tab] TYPE ID1 ID2 [...]
    """
    toks = s.split('\t')
    assert len(toks) == 2, 'Illegal format: %s' % s

    rel = BratEquivRelation()
    rel.id = toks[0]

    toks = toks[1].split(' ')
    rel.type = toks[0]
    for tok in toks[1:]:
        rel.argids.add(tok)
    return rel


def loads_brat_event(s: str) -> BratEvent:
    """
    ID [tab] TYPE:TRIGGER [ROLE1:PART1 ROLE2:PART2 ...]
    """
    toks = s.split('\t')
    assert len(toks) == 2, 'Illegal format: %s' % s

    event = BratEvent()
    event.id = toks[0]

    toks = toks[1].split(" ")
    i = toks[0].find(':')
    assert i != -1, 'Illegal format: %s' % s
    event.type = toks[0][:i]
    event.trigger_id = toks[0][i+1:]

    for tok in toks[1:]:
        i = tok.find(':')
        assert i != -1, 'Illegal format: %s' % s
        event.arguments[tok[:i]] = tok[i+1:]

    return event


def loads_brat_relation(s: str) -> BratRelation:
    """
    ID [tab] TYPE [ROLE1:PART1 ROLE2:PART2 ...]
    """
    toks = s.split('\t')
    assert len(toks) == 2, 'Illegal format: %s' % s

    rel = BratRelation()
    rel.id = toks[0]

    toks = toks[1].split(" ")
    rel.type = toks[0]

    for tok in toks[1:]:
        i = tok.find(':')
        assert i != -1, 'Illegal format: %s' % s
        rel.arguments[tok[:i]] = tok[i + 1:]

    return rel


def loads_brat_note(s: str) -> BratNote:
    """
    #ID [tab] TYPE REFID [tab] NOTE
    """
    toks = s.split('\t')
    assert len(toks) == 3, 'Illegal format: %s' % s

    note = BratNote()
    note.id = toks[0]
    note.text = toks[2]

    i = toks[1].find(' ')
    assert i != -1, 'Illegal format: %s' % s
    note.type = toks[1][:i]
    note.refid = toks[1][i+1:]

    return note


def load(fp: TextIO):
    doc = BratDocument()
    for i, line in enumerate(fp):
        if line[0] == 'T':
            doc.add_annotation(loads_brat_entity(line))
        if line[0] == 'E':
            doc.add_annotation(loads_brat_event(line))
        if line[0] == 'R':
            doc.add_annotation(loads_brat_relation(line))
        if line[0] == '#':
            doc.add_annotation(loads_brat_note(line))
        if line[0] == 'A' or line[0] == 'M':
            doc.add_annotation(loads_brat_attribute(line))
        if line[0] == '*':
            doc.add_annotation(loads_brat_equiv(line))
    return doc