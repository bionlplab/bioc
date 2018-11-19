"""
Validate BioC data structure
"""
from typing import Callable, List

from bioc.bioc import BioCDocument, BioCCollection


# pylint: disable=unused-argument
def _default_error(msg, traceback):
    """Default error handler that accepts two parameters: error message and traceback."""
    raise ValueError(msg)


class BioCValidator:
    """
    Validate BioC data structure
    """

    def __init__(self, onerror: Callable[[str, List], None] = None):
        if onerror is None:
            self.onerror = _default_error
        else:
            self.onerror = onerror
        self.current_docid = None
        self.traceback = []

    def validate_doc(self, document: BioCDocument):
        """Validate a single document."""
        annotations = []
        annotations.extend(document.annotations)
        annotations.extend(document.relations)
        for passage in document.passages:
            annotations.extend(passage.annotations)
            annotations.extend(passage.relations)
            for sentence in passage.sentences:
                annotations.extend(sentence.annotations)
                annotations.extend(sentence.relations)

        self.current_docid = document.id
        self.traceback.append(document)

        text = self.__get_doc_text(document)
        self.__validate_ann(document.annotations, text, 0)
        self.__validate_rel(annotations, document.relations, f'document {document.id}')

        for passage in document.passages:
            self.traceback.append(passage)

            text = self.__get_passage_text(passage)
            self.__validate_ann(passage.annotations, text, passage.offset)
            self.__validate_rel(annotations, passage.relations,
                                f'document {document.id} --> passage {passage.offset}')

            for sentence in passage.sentences:
                self.traceback.append(sentence)
                self.__validate_ann(sentence.annotations, sentence.text, sentence.offset)
                self.__validate_rel(annotations, sentence.relations,
                                    f'document {document.id} --> sentence {sentence.offset}')
                self.traceback.pop()
            self.traceback.pop()
        self.traceback.pop()

    def validate(self, collection: BioCCollection):
        """Validate a single collection."""
        for document in collection.documents:
            self.validate_doc(document)

    def __validate_rel(self, annotations, relations, path):
        for relation in relations:
            for node in relation.nodes:
                if not self.__contains(annotations, node.refid):
                    self.onerror(f'Cannot find node {node} in {path}', self.traceback)

    def __validate_ann(self, annotations, text, offset):
        for ann in annotations:
            self.traceback.append(ann)
            location = ann.total_span
            anntext = text[location.offset - offset: location.offset + location.length - offset]
            if anntext != ann.text:
                self.onerror(
                    '%s: Annotation text is incorrect at %d.\n'
                    '  Annotation: %s\n'
                    '  Actual text: %s' %
                    (self.current_docid, location.offset, anntext, ann.text),
                    self.traceback)
            self.traceback.pop()

    @classmethod
    def __contains(cls, annotations, ann_id):
        for ann in annotations:
            if ann.id == ann_id:
                return True
        return False

    def __fill_newline(self, text, offset):
        dis = offset - len(text)
        if dis < 0:
            self.onerror('%s: Overlap with previous text: len[%d] vs next offset[%d]\n%s'
                         % (self.current_docid, len(text), offset, text),
                         self.traceback)
        if dis > 0:
            text += '\n' * dis
        return text

    def __get_passage_text(self, passage):
        if passage.text:
            return passage.text

        text = ''
        for sentence in passage.sentences:
            self.traceback.append(sentence)
            text = self.__fill_newline(text, sentence.offset)
            if sentence.text:
                text += sentence.text
            else:
                self.onerror(
                    f'{self.current_docid}: BioC sentence has no text: {sentence.offset}',
                    self.traceback)
            self.traceback.pop()
        return text

    def __get_doc_text(self, document):
        text = ''
        for passage in document.passages:
            text = self.__fill_newline(text, passage.offset)
            text += self.__get_passage_text(passage)
        return text


def validate(collection, onerror: Callable[[str, List], None] = None):
    """Validate BioC data structure."""
    BioCValidator(onerror).validate(collection)
