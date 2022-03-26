import bioc
from bioc.pubtator.pubtator import PubTatorAnn, PubTator, PubTatorRel


def pubtator2bioc_ann(ann: PubTatorAnn) -> bioc.BioCAnnotation:
    biocann = bioc.BioCAnnotation()
    biocann.id = 'T{}'.format(ann.start)
    biocann.infons['type'] = ann.type
    biocann.infons['concept_id'] = ann.id
    biocann.add_location(bioc.BioCLocation(ann.start, ann.end - ann.start))
    biocann.text = ann.text
    return biocann


def pubtator2bioc_rel(rel: PubTatorRel) -> bioc.BioCRelation:
    biocrel = bioc.BioCRelation()
    biocrel.infons['type'] = rel.type
    biocrel.add_node(bioc.BioCNode(rel.id1, 'Chemical'))
    biocrel.add_node(bioc.BioCNode(rel.id2, 'Disease'))
    return biocrel


def pubtator2bioc(pubdoc: PubTator):
    doc = bioc.BioCDocument()
    doc.id = pubdoc.pmid
    doc.text = '%s\n%s' % (pubdoc.title, pubdoc.abstract)
    for ann in pubdoc.annotations:
        biocann = pubtator2bioc_ann(ann)
        doc.add_annotation(biocann)
    for i, rel in enumerate(pubdoc.relations):
        biocrel = pubtator2bioc_rel(rel)
        biocrel.id = 'R%s' % i
        doc.add_relation(biocrel)
    return doc
