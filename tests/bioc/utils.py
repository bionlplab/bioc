def assert_everything(collection):
    assert 'source' == collection.source
    assert 'date' == collection.date, collection.date
    assert 'key' == collection.key
    assert 'collection-infon-value' == collection.infons['collection-infon-key']
    document = collection.documents[0]
    assert '1' == document.id
    assert 'document-infon-value' == document.infons['document-infon-key']
    passage = document.passages[0]
    assert 0 == passage.offset
    assert 'passage-infon-value' == passage.infons['passage-infon-key']
    assert 'abcdefghijklmnopqrstuvwxyz' == passage.text
    annotation = passage.annotations[0]
    assert '1' == annotation.id
    assert 'annotation-infon-value' == annotation.infons['annotation-infon-key']
    assert 'bc' == annotation.text
    assert 1 == annotation.total_span.offset
    assert 2 == annotation.total_span.length
    annotation = passage.annotations[1]
    assert '2' == annotation.id
    assert 'annotation-infon-value' == annotation.infons['annotation-infon-key']
    assert 'fg' == annotation.text
    assert 5 == annotation.total_span.offset
    assert 2 == annotation.total_span.length
    relation = passage.relations[0]
    assert 'R1' == relation.id
    assert 'relation-infon-value' == relation.infons['relation-infon-key']
    assert '1' == relation.nodes[0].refid
    assert 'role1' == relation.nodes[0].role
    assert '2' == relation.nodes[1].refid
    assert 'role2' == relation.nodes[1].role
    relation = document.relations[0]
    assert 'R2' == relation.id
    assert 'relation-infon-value' == relation.infons['relation-infon-key']
    assert '1' == relation.nodes[0].refid
    assert 'role1' == relation.nodes[0].role
    assert '2' == relation.nodes[1].refid
    assert 'role2' == relation.nodes[1].role

    document = collection.documents[1]
    passage = document.passages[0]
    assert 27 == passage.offset
    sentence = passage.sentences[0]
    assert 27 == sentence.offset
    assert 'sentence-infon-value' == sentence.infons['sentence-infon-key']
    assert 'abcdefg' == sentence.text
    sentence = passage.sentences[1]
    assert 34 == sentence.offset
    assert 'sentence-infon-value' == sentence.infons['sentence-infon-key']
    assert 'hijklm' == sentence.text
    annotation = passage.sentences[0].annotations[0]
    assert '3' == annotation.id
    assert 'annotation-infon-value' == annotation.infons['annotation-infon-key']
    assert 'bc' == annotation.text
    assert 28 == annotation.total_span.offset
    assert 2 == annotation.total_span.length
    annotation = passage.sentences[1].annotations[0]
    assert '4' == annotation.id
    assert 'annotation-infon-value' == annotation.infons['annotation-infon-key']
    assert 'hi' == annotation.text
    assert 34 == annotation.total_span.offset
    assert 2 == annotation.total_span.length
    relation = passage.sentences[0].relations[0]
    assert 'R3' == relation.id
    assert 'relation-infon-value' == relation.infons['relation-infon-key']
    assert '3' == relation.nodes[0].refid
    assert 'role1' == relation.nodes[0].role