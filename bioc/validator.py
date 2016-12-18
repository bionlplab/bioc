class BioCValidator(object):
    def __init__(self):
        pass

    def validate(self, collection):
        for document in collection.documents:
            text = self.__get_doc_text(document)
            self.__validate_ann(document.annotations, text, 0)
            for relation in document.relations:
                for node in relation.nodes:
                    assert self.__contains(document.annotations, document.relations, node.refid), \
                        'Cannot find node %s in document %s' % (str(node), document.id)

            for passage in document.passages:
                text = self.__get_passage_text(passage)
                self.__validate_ann(passage.annotations, text, passage.offset)
                for relation in passage.relations:
                    for node in relation.nodes:
                        assert self.__contains(passage.annotations, passage.relations, node.refid), \
                            'Cannot find node %s in document %s' % (str(node), document.id)

                for sentence in passage.sentences:
                    self.__validate_ann(sentence.annotations, sentence.text, sentence.offset)
                    for relation in sentence.relations:
                        for node in relation.nodes:
                            assert self.__contains(sentence.annotations, sentence.relations,
                                                   node.refid), \
                                'Cannot find node %s document %s' % (str(node), document.id)

    def __validate_ann(self, annotations, text, offset):
        for ann in annotations:
            anntext = ''
            sorted(ann.locations, key=lambda l: l.offset)
            for location in ann.locations:
                anntext += ' ' \
                           + text[
                             location.offset - offset: location.offset + location.length - offset]
            anntext = anntext.lstrip()
            assert anntext == ann.text, 'Annotation text is incorrect.\n  Annotation: %s\n  Acutal text: %s' \
                                        % (anntext, ann.text)

    def __contains(self, annotations, relations, id):
        for ann in annotations:
            if ann.id == id:
                return True
        for rel in relations:
            if rel.id == id:
                return True
        return False

    def __filltext(self, text, offset):
        while len(text) < offset:
            text += '\n'
        return text

    def __get_passage_text(self, passage):
        if passage.text:
            return passage.text

        text = ''
        for sentence in passage.sentences:
            text = self.__filltext(text, sentence.offset)
            assert sentence.text, 'BioC sentence has no text'
            text += sentence.text
        return text

    def __get_doc_text(self, document):
        text = ''
        for passage in document.passages:
            text = self.__filltext(text, passage.offset)
            text += self.__get_passage_text(passage)
        return text
