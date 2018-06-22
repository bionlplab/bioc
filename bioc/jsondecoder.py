import json

import bioc


def parse_collection(obj):
    collection = bioc.BioCCollection()
    collection.source = obj['source']
    collection.date = obj['date']
    collection.key = obj['key']
    collection.infons = obj['infons']
    for doc in obj['documents']:
        collection.add_document(parse_doc(doc))
    return collection


def parse_annotation(obj):
    ann = bioc.BioCAnnotation()
    ann.id = obj['id']
    ann.infons = obj['infons']
    ann.text = obj['text']
    for loc in obj['locations']:
        ann.add_location(bioc.BioCLocation(loc['offset'], loc['length']))
    return ann


def parse_relation(obj):
    rel = bioc.BioCRelation()
    rel.id = obj['id']
    rel.infons = obj['infons']
    for node in obj['nodes']:
        rel.add_node(bioc.BioCNode(node['refid'], node['role']))
    return rel


def parse_sentence(obj):
    sentence = bioc.BioCSentence()
    sentence.offset = obj['offset']
    sentence.infons = obj['infons']
    sentence.text = obj['text']
    for annotation in obj['annotations']:
        sentence.add_annotation(parse_annotation(annotation))
    for relation in obj['relations']:
        sentence.add_relation(parse_relation(relation))
    return sentence


def parse_passage(obj):
    passage = bioc.BioCPassage()
    passage.offset = obj['offset']
    passage.infons = obj['infons']
    if 'text' in obj:
        passage.text = obj['text']
    for sentence in obj['sentences']:
        passage.add_sentence(parse_sentence(sentence))
    for annotation in obj['annotations']:
        passage.add_annotation(parse_annotation(annotation))
    for relation in obj['relations']:
        passage.add_relation(parse_relation(relation))
    return passage


def parse_doc(obj):
    doc = bioc.BioCDocument()
    doc.id = obj['id']
    doc.infons = obj['infons']
    for passage in obj['passages']:
        doc.add_passage(parse_passage(passage))
    for annotation in obj['annotations']:
        doc.add_annotation(parse_annotation(annotation))
    for relation in obj['relations']:
        doc.add_relation(parse_relation(relation))
    return doc


def load(fp, **kwargs):
    """
    Deserialize fp (a .read()-supporting text file or binary file containing a JSON document) to a BioCCollection object

    Args:
        fp: a file containing a JSON document
        **kwargs:

    Returns:
        BioCCollection: a collection
    """
    obj = json.load(fp, **kwargs)
    return parse_collection(obj)


def loads(s, **kwargs):
    """
    Deserialize s (a str, bytes or bytearray instance containing a JSON document) to a BioCCollection object.

    Args:
        s(str):
        **kwargs:

    Returns:
        BioCCollection: a collection
    """
    obj = json.loads(s, **kwargs)
    return parse_collection(obj)
