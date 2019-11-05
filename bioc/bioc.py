"""
Data structures and code to read/write BioC XML.
"""
import sys
import time

from .utils import shorten_text


class InfonsMaxin:
    def __init__(self):
        super(InfonsMaxin, self).__init__()
        self.infons = {}

    def clear_infons(self):
        """
        Clears all information.
        """
        self.infons.clear()

    def __str__infons__(self):
        return 'infons=[%s],' % ','.join(f'{k}={v}' for (k, v) in self.infons.items())


class BioCNode:
    """
    The annotations and/or other relations in the relation.
    """

    def __init__(self, refid: str, role: str):
        """
        Args:
            refid: the id of an annotated object or another relation
            role: the role of how the referenced annotation or other relation participates in
            the current relation
        """
        self.refid = refid
        self.role = role

    def __str__(self):
        return f'BioCNode[refid={self.refid},role={self.role}]'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.refid == other.refid and self.role == other.role

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.refid, self.role))


class BioCLocation:
    """
    The connection to the original text can be made through the offset and length fields.
    """

    def __init__(self, offset: int, length: int):
        """
        Args:
            offset: the offset of annotation
            length: the length of the annotated text
        """
        self.offset = offset
        self.length = length

    def __str__(self):
        return f'BioCLocation[offset={self.offset},length={self.length}]'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.offset == other.offset and self.length == other.length

    def __ne__(self, other):
        return not self.__eq__(other)

    def __contains__(self, location):
        if not isinstance(location, BioCLocation):
            raise TypeError(f'Object of type {location.__class__.__name__} is not BioCLocation')
        return self.offset <= location.offset \
               and location.offset + location.length <= self.offset + self.length

    def __hash__(self):
        return hash((self.offset, self.length))

    @property
    def end(self):
        """The end offset of annotation"""
        return self.offset + self.length


class BioCAnnotation(InfonsMaxin):
    """
    Stand off annotation.
    """

    def __init__(self):
        super(BioCAnnotation, self).__init__()
        self.locations = []
        self.id = ''
        self.text = ''

    def add_location(self, location: BioCLocation):
        """
        Adds the location at the specified position in this annotation.

        Args:
            location: the location at the specified position in this annotation
        """
        self.locations.append(location)

    def __str__(self):
        s = 'BioCAnnotation['
        s += f'id={self.id},'
        s += f'text={shorten_text(self.text)},'
        s += self.__str__infons__()
        s += 'locations=[%s],' % ','.join(str(l) for l in self.locations)
        s += ']'
        return s

    def __repr__(self):
        return str(self)

    @property
    def total_span(self) -> BioCLocation:
        """The total span of this annotation. Discontinued locations will be merged."""
        if not self.locations:
            raise ValueError(f'{self.id}: annotation must have at least one location')
        start = min(l.offset for l in self.locations)
        end = max(l.end for l in self.locations)
        return BioCLocation(start, end - start)

    def __contains__(self, annotation):
        if not isinstance(annotation, BioCAnnotation):
            raise TypeError(f'Object of type {annotation.__class__.__name__} is not BioCAnnotation')
        loc1 = self.total_span
        loc2 = annotation.total_span
        return loc2 in loc1


class BioCRelation(InfonsMaxin):
    """
    Relationship between multiple BioCAnnotations and possibly other BioCRelations
    """

    def __init__(self):
        super(BioCRelation, self).__init__()
        self.id = ''
        self.nodes = []

    def __str__(self):
        s = 'BioCRelation['
        s += 'id=%s,' % self.id
        s += self.__str__infons__()
        s += 'nodes=[%s],' % ','.join(str(n) for n in self.nodes)
        s += ']'
        return s

    def __repr__(self):
        return str(self)

    def add_node(self, node: BioCNode):
        """
        Add the node to this relation

        Args:
            node: node to be added to this relation
        """
        self.nodes.append(node)

    def get_node(self, role: str, default=None) -> BioCNode:
        """
        Get the first node with role

        Args:
            role: role
            default: node returned instead of raising StopIteration

        Returns:
            the first node with role
        """
        return next((node for node in self.nodes if node.role == role), default)


class AnnotationMixin:
    def __init__(self):
        super(AnnotationMixin, self).__init__()
        self.annotations = []
        self.relations = []

    def add_annotation(self, annotation: BioCAnnotation):
        """
        Adds annotation in this sentence.

        Args:
            annotation: the annotation
        """
        self.annotations.append(annotation)

    def clear_annotations(self):
        """
        Clears all annotations.
        """
        del self.annotations[:]

    def clear_relations(self):
        """
        Clears all relations.
        """
        del self.relations[:]

    def add_relation(self, relation: BioCRelation):
        """
        Adds relation in this sentence.

        Args:
            relation: a relation
        """
        self.relations.append(relation)

    def __str__anns__(self):
        s = 'annotations=[%s],' % ','.join(str(a) for a in self.annotations)
        s += 'relations=[%s],' % ','.join(str(r) for r in self.relations)
        return s


class BioCSentence(AnnotationMixin, InfonsMaxin):
    """
    One sentence in a {@link BioCPassage}.

    It may contain the original text of the sentence or it might be BioCAnnotations and possibly
    BioCRelations on the text of the passage.

    There is no code to keep those possibilities mutually exclusive. However the currently available
    DTDs only describe the listed possibilities.
    """

    def __init__(self):
        super(BioCSentence, self).__init__()
        self.offset = -1
        self.text = ''

    def __str__(self):
        s = 'BioCSentence['
        s += 'offset=%s,' % self.offset
        s += 'text=%s,' % shorten_text(self.text)
        s += self.__str__infons__()
        s += self.__str__anns__()
        s += ']'
        return s

    def __repr__(self):
        return str(self)


class BioCPassage(AnnotationMixin, InfonsMaxin):
    """
    One passage in a BioCDocument.

    This might be the text in the passage and possibly BioCAnnotations over that text. It could be
    the BioCSentences in the passage. In either case it might include BioCRelations over annotations
    on the passage.
    """

    def __init__(self):
        super(BioCPassage, self).__init__()
        self.offset = -1
        self.text = ''
        self.sentences = list()

    def __str__(self):
        s = 'BioCPassage['
        s += 'offset=%d,' % self.offset
        if self.text is not None:
            s += 'text=%s,' % shorten_text(self.text)
        s += self.__str__infons__()
        s += 'sentences=[%s],' % ','.join(str(s) for s in self.sentences)
        s += self.__str__anns__()
        s += ']'
        return s

    def __repr__(self):
        return str(self)

    def add_sentence(self, sentence: BioCSentence):
        """
        Adds sentence in this passage.

        Args:
            sentence: a sentence
        """
        self.sentences.append(sentence)

    def get_sentence(self, offset: int) -> BioCSentence or None:
        """
        Gets sentence with specified offset

        Args:
            offset: sentence offset

        Return:
            the sentence with specified offset
        """
        for sentence in self.sentences:
            if sentence.offset == offset:
                return sentence
        return None

    @classmethod
    def of_sentences(cls, *sentences: BioCSentence) -> 'BioCPassage':
        """
        Returns a passage containing the sentences
        """
        if len(sentences) <= 0:
            raise ValueError("There has to be at least one sentence.")
        p = BioCPassage()
        p.offset = sys.maxsize
        for sentence in sentences:
            if sentence is None:
                raise ValueError('Passage is None')
            p.add_sentence(sentence)
            p.offset = min(p.offset, sentence.offset)
        return p


class BioCDocument(AnnotationMixin, InfonsMaxin):
    """
    One document in the BioCCollection.

    An id, typically from the original corpus, identifies the particular document. It includes
    BioCPassages in the document and possibly BioCRelations over annotations on the document.
    """

    def __init__(self):
        super(BioCDocument, self).__init__()
        self.id = ''
        self.passages = list()

    def __str__(self):
        s = 'BioCDocument['
        s += 'id=%s,' % self.id
        s += self.__str__infons__()
        s += 'passages=[%s],' % ','.join(str(p) for p in self.passages)
        s += self.__str__anns__()
        s += ']'
        return s

    def __repr__(self):
        return str(self)

    def add_passage(self, passage: BioCPassage):
        """
        Adds passage in this document.

        Args:
            passage: a passage
        """
        self.passages.append(passage)

    def get_passage(self, offset: int) -> BioCPassage or None:
        """
        Gets passage

        Args:
            offset: passage offset

        Return:
            the passage with specified offset
        """
        for passage in self.passages:
            if passage.offset == offset:
                return passage
        return None

    @classmethod
    def of_passages(cls, *passages: BioCPassage) -> 'BioCDocument':
        """
        Returns a document containing the passages
        """
        if len(passages) <= 0:
            raise ValueError("There has to be at least one passage.")
        document = BioCDocument()
        for passage in passages:
            if passage is None:
                raise ValueError('Passage is None')
            document.add_passage(passage)
        return document

    @classmethod
    def of_text(cls, text: str) -> 'BioCDocument':
        """
        Returns a document containing one passage with the text
        """
        passage = BioCPassage()
        passage.text = text
        passage.offset = 0
        return cls.of_passages(passage)


class BioCCollection(InfonsMaxin):
    """
    Collection of documents.

    Collection of documents for a project. They may be an entire corpus or some portion of a corpus.
    Fields are provided to describe the collection.

    Documents may appear empty if doing document at a time IO.
    """

    def __init__(self):
        super(BioCCollection, self).__init__()
        self.encoding = 'utf-8'
        self.version = '1.0'
        self.standalone = True

        self.source = ''
        self.date = time.strftime("%Y-%m-%d")
        self.key = ''

        self.documents = list()

    def add_document(self, document: BioCDocument):
        """
        Adds document in this collection.

        Args:
            document: a document
        """
        self.documents.append(document)

    def __str__(self):
        s = 'BioCCollection['
        s += 'source=%s,' % self.source
        s += 'date=%s,' % self.date
        s += 'key=%s,' % self.key
        s += self.__str__infons__()
        s += 'documents=[%s],' % ','.join(str(d) for d in self.documents)
        s += ']'
        return s

    def __repr__(self):
        return str(self)

    @classmethod
    def of_documents(cls, *documents: BioCDocument) -> 'BioCCollection':
        """
        Returns a collection containing the documents
        """
        if len(documents) <= 0:
            raise ValueError("There has to be at least one document.")
        c = BioCCollection()
        for document in documents:
            if document is None:
                raise ValueError('Document is None')
            c.add_document(document)
        return c


# def _shorten_text(text: str):
#     if len(text) <= 40:
#         text = text
#     else:
#         text = text[:17] + ' ... ' + text[-17:]
#     return repr(text)
