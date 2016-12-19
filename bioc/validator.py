class BioCValidator(object):
    def __init__(self):
        pass

    def validate(self, collection):
        annotations = []
        for document in collection.documents:
            annotations.extend(document.annotations)
            annotations.extend(document.relations)
            for passage in document.passages:
                annotations.extend(passage.annotations)
                annotations.extend(passage.relations)
                for sentence in passage.sentences:
                    annotations.extend(sentence.annotations)
                    annotations.extend(sentence.relations)

        for document in collection.documents:
            text = self.__get_doc_text(document)
            self.__validate_ann(document.annotations, text, 0)
            for relation in document.relations:
                for node in relation.nodes:
                    assert self.__contains(annotations, node.refid), \
                        'Cannot find node %s in document %s' % (str(node), document.id)

            for passage in document.passages:
                text = self.__get_passage_text(passage)
                self.__validate_ann(passage.annotations, text, passage.offset)
                for relation in passage.relations:
                    for node in relation.nodes:
                        assert self.__contains(annotations, node.refid), \
                            'Cannot find node %s in document %s' % (str(node), document.id)

                for sentence in passage.sentences:
                    self.__validate_ann(sentence.annotations, sentence.text, sentence.offset)
                    for relation in sentence.relations:
                        for node in relation.nodes:
                            assert self.__contains(annotations, node.refid), \
                                'Cannot find node %s document %s' % (str(node), document.id)

    def __validate_ann(self, annotations, text, offset):
        for ann in annotations:
            location = ann.get_total_location()
            anntext = text[location.offset - offset: location.offset + location.length - offset]
            assert anntext == ann.text, \
                'Annotation text is incorrect.\n  Annotation: %s\n  Actual text: %s' \
                % (anntext, ann.text)

    @staticmethod
    def __contains(annotations, id):
        for ann in annotations:
            if ann.id == id:
                return True
        return False

    @staticmethod
    def __fill_newline(text, offset):
        dis = offset - len(text)
        if dis > 0:
            text += '\n' * dis
        return text

    def __get_passage_text(self, passage):
        if passage.text:
            return passage.text

        text = ''
        for sentence in passage.sentences:
            text = self.__fill_newline(text, sentence.offset)
            assert sentence.text, 'BioC sentence has no text: {}'.format(sentence.offset)
            text += sentence.text
        return text

    def __get_doc_text(self, document):
        text = ''
        for passage in document.passages:
            text = self.__fill_newline(text, passage.offset)
            text += self.__get_passage_text(passage)
        return text
