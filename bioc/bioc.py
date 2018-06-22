"""
Data structures and code to read/write BioC XML.
"""
import time
import sys


class BioCNode(object):
    """
    The annotations and/or other relations in the relation.
    """

    def __init__(self, refid, role):
        """
        Args:
            refid (str): the id of an annotated object or another relation
            role (str): the role of how the referenced annotation or other
                relation participates in the current relation
        """
        self.refid = refid
        self.role = role

    def __str__(self):
        return 'BioCNode[refid=%s,role=%s]' % (self.refid, self.role)

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


class BioCLocation(object):
    """
    The connection to the original text can be made through the offset and length fields.
    """

    def __init__(self, offset, length):
        """
        Args:
            offset (int): the offset of annotation
            length (int): the length of the annotated text
        """
        self.offset = offset
        self.length = length

    def __str__(self):
        return 'BioCLocation[offset=%s,length=%s]' % (self.offset, self.length)

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
            raise TypeError('%s is not an instance of BioCLocation' % type(location))
        return self.offset <= location.offset \
            and location.offset + location.length <= self.offset + self.length

    def __hash__(self):
        return hash((self.offset, self.length))

    @property
    def end(self):
        return self.offset + self.length


class BioCAnnotation(object):
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

        Args:
            location(BioCLocation): the location at the specified position in
                this annotation
        """
        self.locations.append(location)

    def __str__(self):
        s = 'BioCAnnotation['
        s += 'id=%s,' % self.id
        s += 'text=%s,' % _shorten_text(self.text)
        s += 'infons=[%s],' % ','.join('%s=%s' % (k, v) for (k, v) in self.infons.items())
        s += 'locations=[%s],' % ','.join(str(l) for l in self.locations)
        s += ']'
        return s

    def __repr__(self):
        s = 'BioCAnnotation['
        s += 'id=%s,' % self.id
        s += 'text=%s,' % self.text
        s += 'infons=[%s],' % ','.join('%s=%s' % (k, v) for (k, v) in self.infons.items())
        s += 'locations=[%s],' % ','.join(str(l) for l in self.locations)
        s += ']'
        return s

    @property
    def total_span(self):
        start = sys.maxsize
        end = 0
        for loc in self.locations:
            start = min(start, loc.offset)
            end = max(end, loc.offset + loc.length)
        return BioCLocation(start, end - start)

    def __contains__(self, annotation):
        if not isinstance(annotation, BioCAnnotation):
            raise TypeError('%s is not an instance of BioCAnnotation' % type(annotation))
        loc1 = self.total_span
        loc2 = annotation.total_span
        return loc2 in loc1


class BioCRelation(object):
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

    def __repr__(self):
        return str(self)

    def add_node(self, node):
        """
        Add the node to this relation

        Args:
            node (BioCNode): node to be added to this relation
        """
        self.nodes.append(node)

    def get_node(self, role, default=None):
        """
        Get the first node with role

        Args:
            role(str): role
            default: node returned instead of raising StopIteration

        Returns:
            BioCNode
        """
        return next((node for node in self.nodes if node.role == role), default)


class BioCSentence(object):
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
        s += 'text=%s,' % _shorten_text(self.text)
        s += 'infons=[%s],' % ','.join('%s=%s' % (k, v) for (k, v) in self.infons.items())
        s += 'annotations=[%s],' % ','.join(str(a) for a in self.annotations)
        s += 'relations=[%s],' % ','.join(str(r) for r in self.relations)
        s += ']'
        return s

    def __repr__(self):
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

        Args:
            annotation (BioCAnnotation): the annotation
        """
        self.annotations.append(annotation)

    def add_relation(self, relation):
        """
        Adds relation in this sentence.

        Args:
            relation(BioCRelation): a relation
        """
        self.relations.append(relation)


class BioCPassage(object):
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
            s += 'text=%s,' % _shorten_text(self.text)
        s += 'infons=[%s],' % ','.join('%s=%s' % (k, v) for (k, v) in self.infons.items())
        s += 'sentences=[%s],' % ','.join(str(s) for s in self.sentences)
        s += 'annotations=[%s],' % ','.join(str(a) for a in self.annotations)
        s += 'relations=[%s],' % ','.join(str(r) for r in self.relations)
        s += ']'
        return s

    def __repr__(self):
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

        Args:
            sentence(BioCSentence): a sentence
        """
        self.sentences.append(sentence)

    def add_annotation(self, annotation):
        """
        Adds annotation in this passage.

        Args:
            annotation (BioCAnnotation): the annotation
        """
        self.annotations.append(annotation)

    def add_relation(self, relation):
        """
        Adds relation in this passage.

        Args:
            relation(BioCRelation): a relation
        """
        self.relations.append(relation)


class BioCDocument(object):
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

    def __repr__(self):
        return str(self)

    def add_passage(self, passage):
        """
        Adds passage in this document.

        Args:
            passage(BioCPassage): a passage
        """
        self.passages.append(passage)

    def add_annotation(self, annotation):
        """
        Adds annotation in this document.

        Args:
            annotation (BioCAnnotation): the annotation
        """
        self.annotations.append(annotation)

    def add_relation(self, relation):
        """
        Adds relation in this document.

        Args:
            relation(BioCRelation): a relation
        """
        self.relations.append(relation)

    def get_passage(self, offset):
        """
        Gets passage

        Args:
            offset(int): passage offset

        Return:
            BioCPassage: the passage
        """
        for passage in self.passages:
            if passage.offset == offset:
                return passage
        return None


class BioCCollection(object):
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

        Args:
            document(BioCDocument): a document
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

    def __repr__(self):
        return str(self)


def _shorten_text(text):
    if len(text) <= 40:
        text = text
    else:
        text = text[:17] + ' ... ' + text[-17:]
    return repr(text)
