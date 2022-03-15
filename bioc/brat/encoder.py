import io
from typing import TextIO

from bioc.brat.brat import BratAttribute, BratEntity, BratEquivRelation, BratEvent, BratNote, BratRelation, BratDocument


def dumps_brat_attribute(att: BratAttribute) -> str:
    """
    ID [tab] TYPE REFID [FLAG1 FLAG2 ...]
    """
    return '%s\t%s %s %s' % (att.id, att.type, att.refid, ' '.join(att.attributes))


def dumps_brat_entity(ent: BratEntity) -> str:
    """
    ID [tab] TYPE START END [tab] TEXT

    ID [tab] TYPE START END[;START END]* [tab] TEXT
    """
    return '%s\t%s %s\t%s' % (ent.id, ent.type,
                              ';'.join(['%s %s' % (i.begin, i.end) for i in sorted(ent.range)]),
                              ent.text)


def dumps_brat_equiv(rel: BratEquivRelation) -> str:
    """
    * [tab] TYPE ID1 ID2 [...]
    """
    return '%s\t%s %s' % (rel.id, rel.type, ' '.join(sorted(rel.argids)))


def dumps_brat_event(event: BratEvent) -> str:
    """
    ID [tab] TYPE:TRIGGER [ROLE1:PART1 ROLE2:PART2 ...]
    """
    return '%s\t%s:%s %s' % (event.id, event.type, event.trigger_id,
                             ' '.join(['%s:%s' % (k, v) for k, v in event.arguments.items()]))


def dumps_brat_relation(rel: BratRelation) -> str:
    """
    ID [tab] TYPE [ROLE1:PART1 ROLE2:PART2 ...]
    """
    return '%s\t%s %s' % (rel.id, rel.type, ' '.join(['%s:%s' % (k, v) for k, v in rel.arguments.items()]))


def dumps_brat_note(note: BratNote) -> str:
    """
    #ID [tab] TYPE REFID [tab] NOTE
    """
    return '%s\t%s %s\t%s' % (note.id, note.type, note.refid, note.text)


def dump(doc: BratDocument, fp: TextIO):
    for ent in doc.entities:
        fp.write('%s\n' % dumps_brat_entity(ent))
    for rel in doc.relations:
        fp.write('%s\n' % dumps_brat_relation(rel))
    for event in doc.events:
        fp.write('%s\n' % dumps_brat_event(event))
    for attr in doc.attributes:
        fp.write('%s\n' % dumps_brat_attribute(attr))
    for rel in doc.equiv_relations:
        fp.write('%s\n' % dumps_brat_equiv(rel))
    for note in doc.notes:
        fp.write('%s\n' % dumps_brat_note(note))


def dumps(doc: BratDocument):
    output = io.StringIO()
    dump(doc, output)
    return output.getvalue()
