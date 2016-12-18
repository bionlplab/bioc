# -*- coding: utf-8 -*-

"""
Data structures and code to read/write BioC XML.
"""
import time, sys


class BioCNode:
    """
    The annotations and/or other relations in the relation.
    """

    def __init__(self, refid, role):
        """
        :param refid: the id of an annotated object or another relation
        :type refid: str
        :param role: the role of how the referenced annotation or other relation participates in the current relation
        :type role: str
        """
        self.refid = refid
        self.role = role

    def __str__(self):
        return 'BioCNode[refid=%s,role=%s]' % (self.refid, self.role)

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

    def __init__(self, offset, length):
        """
        :param offset: the offset of annotation
        :type offset: int
        :param length: the length of the annotated text
        :type length: int
        """
        self.offset = offset
        self.length = length

    def __str__(self):
        return 'BioCLocation[offset=%s,length=%s]' % (self.offset, self.length)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.offset == other.offset and self.length == other.length

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.offset, self.length))


class BioCAnnotation:
    """
    Stand off annotation.
    """

    def __init__(self):
        self.infons = dict()
        self.locations = list()
        self.id = ''
        self.text = ''

    def add_location(self, location):
        """
        Adds the location at the specified position in this annotation.

        :param location: The location at the specified position in this annotation
        :type location: BioCLocation
        """
        self.locations.append(location)

    def __str__(self):
        s = 'BioCAnnotation['
        s += 'id=%s,' % self.id
        s += 'text=%s,' % self.text
        s += 'infons=[%s],' % ','.join('%s=%s' % (k, v) for (k, v) in self.infons.items())
        s += 'locations=[%s],' % ','.join(str(l) for l in self.locations)
        s += ']'
        return s

    def get_total_location(self):
        start = sys.maxint
        end = 0
        for loc in self.locations:
            start = min(start, loc.offset)
            end = max(end, loc.offset + loc.length)
        return BioCLocation(start, end - start)

    def __contains__(self, annotation):
        loc1 = self.get_total_location()
        loc2 = annotation.get_total_location()
        return loc1.offset <= loc2.offset and loc2.offset + loc2.length <= loc1.offset + loc1.length


class BioCRelation:
    """
    Relationship between multiple BioCAnnotations and possibly other BioCRelations
    """

    def __init__(self):
        self.id = ''
        self.infons = dict()
        self.nodes = list()

    def __str__(self):
        s = 'BioCRelation['
        s += 'id=%s,' % self.id
        s += 'infons=[%s],' % ','.join('%s=%s' % (k, v) for (k, v) in self.infons.items())
        s += 'nodes=[%s],' % ','.join(str(n) for n in self.nodes)
        s += ']'
        return s

    def add_node(self, node):
        """
        Add the node to this relation

        :param node: node to be added to this relation
        :type node: BioCNode
        """
        self.nodes.append(node)


class BioCSentence:
    """
    One sentence in a {@link BioCPassage}.

    It may contain the original text of the sentence or it might be BioCAnnotations and possibly
    BioCRelations on the text of the passage.

    There is no code to keep those possibilities mutually exclusive. However the currently available
    DTDs only describe the listed possibilities.
    """

    def __init__(self):
        self.offset = -1
        self.text = ''
        self.infons = dict()
        self.annotations = list()
        self.relations = list()

    def __str__(self):
        s = 'BioCSentence['
        s += 'offset=%s,' % self.offset
        s += 'text=%s,' % self.text
        s += 'infons=[%s],' % ','.join('%s=%s' % (k, v) for (k, v) in self.infons.items())
        s += 'annotations=[%s],' % ','.join(str(a) for a in self.annotations)
        s += 'relations=[%s],' % ','.join(str(r) for r in self.relations)
        s += ']'
        return s

    def clear_infons(self):
        """
        Clears all information.
        """
        self.infons.clear()

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

    def add_annotation(self, annotation):
        """
        Adds annotation in this sentence.

        :param annotation: annotation
        :type annotation: BioCAnnotation
        """
        self.annotations.append(annotation)

    def add_relation(self, relation):
        """
        Adds relation in this sentence.

        :param relation: relation
        :type relation: BioCRelation
        """
        self.relations.append(relation)


class BioCPassage:
    """
    One passage in a BioCDocument.

    This might be the text in the passage and possibly BioCAnnotations over that text. It could be
    the BioCSentences in the passage. In either case it might include BioCRelations over annotations
    on the passage.
    """

    def __init__(self):
        self.offset = -1
        self.text = ''
        self.infons = dict()
        self.sentences = list()
        self.annotations = list()
        self.relations = list()

    def __str__(self):
        s = 'BioCPassage['
        s += 'offset=%s,' % self.offset
        if self.text is not None:
            s += 'text=%s,' % self.text
        s += 'infons=[%s],' % ','.join('%s=%s' % (k, v) for (k, v) in self.infons.items())
        s += 'sentences=[%s],' % ','.join(str(s) for s in self.sentences)
        s += 'annotations=[%s],' % ','.join(str(a) for a in self.annotations)
        s += 'relations=[%s],' % ','.join(str(r) for r in self.relations)
        s += ']'
        return s

    def add_sentence(self, sentence):
        """
        Adds sentence in this passage.

        :param sentence: sentence
        :type sentence: BioCSentence
        """
        self.sentences.append(sentence)

    def add_annotation(self, annotation):
        """
        Adds annotation in this passage.

        :param annotation: annotation
        :type annotation: BioCAnnotation
        """
        self.annotations.append(annotation)

    def add_relation(self, relation):
        """
        Adds relation in this passage.

        :param relation: relation
        :type relation: BioCRelation
        """
        self.relations.append(relation)


class BioCDocument:
    """
    One document in the BioCCollection.

    An id, typically from the original corpus, identifies the particular document. It includes
    BioCPassages in the document and possibly BioCRelations over annotations on the document.
    """

    def __init__(self):
        self.id = ''
        self.infons = dict()
        self.passages = list()
        self.annotations = list()
        self.relations = list()

    def __str__(self):
        s = 'BioCDocument['
        s += 'id=%s,' % self.id
        s += 'infons=[%s],' % ','.join('%s=%s' % (k, v) for (k, v) in self.infons.items())
        s += 'passages=[%s],' % ','.join(str(p) for p in self.passages)
        s += 'annotations=[%s],' % ','.join(str(a) for a in self.annotations)
        s += 'relations=[%s],' % ','.join(str(r) for r in self.relations)
        s += ']'
        return s

    def add_passage(self, passage):
        """
        Adds passage in this document.

        :param passage: passage
        :type passage: BioCPassage
        """
        self.passages.append(passage)

    def add_annotation(self, annotation):
        """
        Adds annotation in this document.

        :param annotation: annotation
        :type annotation: BioCAnnotation
        """
        self.annotations.append(annotation)

    def add_relation(self, relation):
        """
        Adds relation in this document.

        :param relation: relation
        :type relation: BioCRelation
        """
        self.relations.append(relation)


class BioCCollection:
    """
    Collection of documents.

    Collection of documents for a project. They may be an entire corpus or some portion of a corpus.
    Fields are provided to describe the collection.

    Documents may appear empty if doing document at a time IO.
    """

    def __init__(self):
        self.encoding = 'utf-8'
        self.version = '1.0'
        self.standalone = True

        self.source = ''
        self.date = time.strftime("%Y-%m-%d")
        self.key = ''

        self.infons = dict()
        self.documents = list()

    def add_document(self, document):
        """
        Adds document in this collection.

        :param document: document
        :type document: BioCDocument
        """
        self.documents.append(document)

    def clear_infons(self):
        """
        Clears all information.
        """
        self.infons.clear()

    def __str__(self):
        s = 'BioCCollection['
        s += 'source=%s,' % self.source
        s += 'date=%s,' % self.date
        s += 'key=%s,' % self.key
        s += 'infons=[%s],' % ','.join('%s=%s' % (k, v) for (k, v) in self.infons.items())
        s += 'documents=[%s],' % ','.join(str(d) for d in self.documents)
        s += ']'
        return s



