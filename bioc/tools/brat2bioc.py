from typing import List

import tqdm

from bioc import BioCDocument, BioCCollection, BioCPassage, BioCAnnotation, BioCLocation, BioCRelation, BioCNode
from bioc.brat.brat import BratDocument, BratEntity, BratRelation, BratEvent, BratEquivRelation


def brat2bioc_entity(bratentity: BratEntity) -> BioCAnnotation:
    ann = BioCAnnotation()
    ann.id = bratentity.id
    ann.text = bratentity.text
    ann.infons['type'] = bratentity.type
    for span in bratentity.range:
        ann.add_location(BioCLocation(span.begin, span.end - span.begin))
    return ann


def brat2bioc_relation(bratrelation: BratRelation) -> BioCRelation:
    rel = BioCRelation()
    rel.id = bratrelation.id
    rel.infons['type'] = bratrelation.type
    for role, refid in bratrelation.arguments.items():
        rel.add_node(BioCNode(refid, role))
    return rel


def brat2bioc_equiv(brat_equiv: BratEquivRelation) -> BioCRelation:
    rel = BioCRelation()
    rel.id = brat_equiv.id
    rel.infons['type'] = brat_equiv.type
    for argid in brat_equiv.argids:
        rel.add_node(BioCNode(argid, 'Arg'))
    return rel


def brat2bioc_event(bratevent: BratEvent) -> BioCRelation:
    rel = BioCRelation()
    rel.id = bratevent.id
    rel.infons['type'] = bratevent.type
    rel.infons['trigger_id'] = bratevent.trigger_id
    rel.add_node(BioCNode(bratevent.trigger_id, bratevent.type))
    for role, refid in bratevent.arguments.items():
        rel.add_node(BioCNode(refid, role))
    return rel


def brat2bioc_doc(bratdoc: BratDocument) -> BioCDocument:
    passage = BioCPassage()
    passage.offset = 0
    passage.text = bratdoc.text
    # entity
    for bratentity in bratdoc.entities:
        passage.add_annotation(brat2bioc_entity(bratentity))
    # relation
    for bratrelation in bratdoc.relations:
        passage.add_relation(brat2bioc_relation(bratrelation))
    # event
    for bratevent in bratdoc.events:
        passage.add_relation(brat2bioc_event(bratevent))
    # equiv
    for i, brat_equiv in enumerate(bratdoc.equiv_relations):
        brat_equiv.id = '%s%s' % (brat_equiv.id, i)
        passage.add_relation(brat2bioc_equiv(brat_equiv))
    # attribute
    for bratatt in bratdoc.attributes:
        ann = passage.get(bratatt.refid)
        ann.infons['note_id'] = bratatt.id
        ann.infons['attributes'] = ' '.join(sorted(bratatt.attributes))
    # note
    for bratnote in bratdoc.notes:
        ann = passage.get(bratnote.refid)
        ann.infons['note_id'] = bratnote.id
        ann.infons['type'] = bratnote.type
        ann.infons['note'] = bratnote.text

    biocdoc = BioCDocument.of_passages(passage)
    biocdoc.id = bratdoc.id
    return biocdoc


def brat2bioc(bratdocs: List[BratDocument]) -> BioCCollection:
    collection = BioCCollection()
    for bratdoc in tqdm.tqdm(bratdocs):
        biocdoc = brat2bioc_doc(bratdoc)
        collection.add_document(biocdoc)
    return collection