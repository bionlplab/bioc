from abc import ABC
from typing import Set, List, Tuple, Dict

from intervaltree import IntervalTree


class BratAnnotation(ABC):
    """
    Base class for all annotations with an ID.

    All annotations IDs consist of a single upper-case character identifying the annotation type and a number. The initial
    ID characters relate to annotation types as follows:

    * T: text-bound annotation
    * R: relation
    * E: event
    * A: attribute
    * M: modification (alias for attribute, for backward compatibility)
    * N: normalization
    * *: equiv relation
    * #: note

    :param id: annotation ID
    :type id: str, optional
    :param type: annotation type
    :type id: str, optional
    """
    def __init__(self):
        self.id = None  # type: str | None
        self.type = None # type: str | None


class BratAttribute(BratAnnotation):
    """
    Attribute annotations are binary or multi-valued "flags" that specify further aspects of other annotations.
    Attributes have a unique ID and are defined by reference to the ID of the annotation that the attribute marks and
    the attribute value.

    ::

        A1  Negation E1
        A2  Confidence E2 L1

    As for other annotations, the ID is separated by TAB and other fields by space.

    Binary attributes such as A1 in the above example need only specify the attribute name and the ID of the marked
    annotation: the value true is implied for the binary attribute. The absence of a binary attribute annotation is
    interpreted as the attribute having the value false.

    Multi-valued attributes specify also the attribute value, separated by SPACE. The values of multi-valued attributes
    are fully configurable.

    For backward compatibility with existing standoff formats, brat also recognizes the ID prefix "M" for attributes.

    Represented in standoff as

    ::

        ID [tab] TYPE REFID [FLAG1 FLAG2 ...]

    :param id: annotation ID staring with A or M
    :param type: annotation type
    :param refid: the ID of the annotation that the attribute marks.
    :param attributes: all "flags" that specify further aspects of referred annotations.
    """
    def __init__(self):
        super(BratAttribute, self).__init__()
        self.refid = None  # type: str | None
        self.attributes = set()  # type: Set[str]

    def add_attribute(self, attribute: str):
        self.attributes.add(attribute)

    def __eq__(self, other):
        if not isinstance(other, BratAttribute):
            return False
        else:
            return self.id == other.id \
                   and self.type == other.type \
                   and self.refid == other.refid \
                   and self.attributes == other.attributes

    def __str__(self):
        return 'BratAttribute[id=%s,type=%s,refid=%s,flags=%s]' % (
            self.id, self.type, self.refid, ';'.join(self.attributes))


class BratEntity(BratAnnotation):
    """
    Each entity annotation has a unique ID and is defined by type (e.g. Person or Organization) and the span of
    characters containing the entity mention (represented as a "start end" offset pair). For example,

    ::

        T1  Organization 0 4  Sony
        T3  Organization 33 41  Ericsson
        T3  Country 75 81 Sweden

    Each line contains one text-bound annotation identifying the entity mention in text

    Represented in standoff as "`ID [tab] TYPE START END [tab] TEXT`" where START and END are positive integer offsets
    identifying the span of the annotation in text and `TEXT` is the corresponding text. Discontinuous annotations can
    be represented as "`ID [tab] TYPE START END[;START END]* [tab] TEXT`" with multiple START END pairs separated by
    semicolons.
    """
    def __init__(self):
        super(BratEntity, self).__init__()
        self.text = None  # type: str | None
        self.range = IntervalTree()  # type: IntervalTree

    def shit(self, offset: int):
        ent = BratEntity()
        ent.id = self.id
        ent.type = self.type
        ent.text = self.text
        for interval in self.range:
            ent.range[interval.begin+offset: interval.end+offset] = interval.data
        return ent

    def add_span(self, start: int, end: int, data = None):
        self.range[start: end] = data

    @property
    def span(self):
        return self.range.begin(), self.range.end()


class BratRelation(BratAnnotation):
    """
    Relations have a unique ID and are defined by their type (e.g. Origin, Part-of) and their arguments.

    ::

        R1 Origin Arg1:T3 Arg2:T4


    The format is similar to that applied for events, with the exception that the annotation does not identify a
    specific piece of text expressing the relation ("trigger"): the ID is separated by a TAB character, and the
    relation type and arguments by SPACE.

    Relation arguments are commonly identified simply as Arg1 and Arg2, but the system can be configured to use any
    labels (e.g. Anaphor and Antecedent) in the standoff representation.

    Represented in standoff as

    ::

        ID [tab] TYPE [ROLE1:PART1 ROLE2:PART2 ...]

    :param arguments: ROLE:ID
        role: task-specific argument role
        id: the entity or event filling that role
    """
    def __init__(self):
        super(BratRelation, self).__init__()
        self.arguments = {}


class BratEquivRelation(BratAnnotation):
    """
    Equivalence ie are symmetric and transitive ie that define sets of annotations to be equivalent in some sense (e.g.
    referring to the same real-world entity). Such ie can be represented in a compact way as a SPACE-separated list of
    the IDs of the equivalent annotations. For example

    ::

        T1  Organization 0 43 International Business Machines Corporation
        T2  Organization 45 48  IBM
        T3  Organization 52 60  Big Blue
        *   Equiv T1 T2 T3

    For backward compatibility with existing standoff formats, brat supports also the special "empty" ID value "*" for
    equivalence relation annotations.

    Represented in standoff as "`* \t TYPE ID1 ID2 [...]`", where "*" is the literal asterisk character.

    :param argids: equivalent annotations
    """
    def __init__(self):
        super(BratEquivRelation, self).__init__()
        self.id = '*'
        self.type = 'Equiv'
        self.argids = set()

    def __eq__(self, other):
        if not isinstance(other, BratEquivRelation):
            return False
        else:
            return self.id == other.id \
                   and self.type == other.type \
                   and self.argids == other.argids


class BratEvent(BratAnnotation):
    """
    Events are typed annotations that are associated with a specific text expression stating the event (TRIGGER,
    identifying a TextBoundAnnotation) and have an arbitrary number of arguments, each of which is represented as a
    ROLE:PARTID pair, where ROLE is a string identifying the role (e.g. "Theme", "Cause") and PARTID the ID of another
    annotation participating in the event.

    ::

        T2  MERGE-ORG 14 27 joint venture
        E1  MERGE-ORG:T2 Org1:T1 Org2:T3

    The event triggers, annotations marking the word or words stating each event, are text-bound annotations and their
    format is identical to that for entities. (The IDs of triggers occupy the same space as the IDs of entities,
    and these must not overlap.)
    
    As for all annotations, the event ID occurs first, separated by a TAB
    character. The event trigger is specified as TYPE:ID and identifies the
    event type and its trigger through the ID. By convention, the event type is
    specified both in the trigger annotation and the event annotation. The event
    trigger is separated from the event arguments by SPACE. The event arguments
    are a SPACE-separated set of ROLE:ID pairs, where ROLE is one of the event-
    and task-specific argument roles (e.g. Theme, Cause, Site) and the ID
    identifies the entity or event filling that role. Note that several events
    can share the same trigger and that while the event trigger should be
    specified first, the event arguments can appear in any order.

    Represented in standoff as "`ID [tab] TYPE:TRIGGER [ROLE1:PART1 ROLE2:PART2 ...]`"

    :param trigger_id: the event trigger, annotations marking the word or words stating each event
    :param arguments: ROLE:ID
        role: task-specific argument role
        id: the entity or event filling that role
    """
    def __init__(self):
        super(BratEvent, self).__init__()
        self.arguments = {}  # type: Dict[str, str]
        self.trigger_id = None  # type: str | None

    def __eq__(self, other):
        if not isinstance(other, BratEvent):
            return False
        else:
            return self.id == other.id \
                   and self.type == other.type \
                   and self.trigger_id == other.trigger_id \
                   and self.arguments == other.arguments


class BratNote(BratAnnotation):
    """
    Note annotations provide a way to associate free-form text with either the
    document or a specific annotation.
    
    ::
    
        #1 AnnotatorNotes T1 this annotation is suspect
    
    Notes with an "ID" starting with # followed by a TAB character attach to
    specific annotations. For these notes, the second TAB-separated field
    contains a note type and the ID of the annotation that the note is attached
    to, and the third TAB-separated field contains the text of the note.
    
    The note type can be freely assigned and any number of notes can be attached
    to a single annotation. (However, currently only a single note of type
    AnnotatorNotes can be edited from the brat UI.)
    
    Represented in standoff as "`#ID [tab] TYPE REFID [tab] NOTE`"

    :param refid: the ID of the annotation that the note is attached to.
    :param text: the text of the note
    """
    def __init__(self):
        super(BratNote, self).__init__()
        self.refid = None  # type: str | None
        self.text = None  # type: str | None
        

class BratDocument:
    """
    :param text: text of the original documents input
    :param id: document id. Usually document name
    """
    def __init__(self):
        self.id = None
        self.text = None
        self.annotations = []  # type: List[BratAnnotation]

    def get_types(self, type):
        return [ann for ann in self.annotations if isinstance(ann, type)]

    @property
    def entities(self):
        return self.get_types(BratEntity)

    @property
    def events(self):
        return self.get_types(BratEvent)

    @property
    def relations(self):
        return self.get_types(BratRelation)

    @property
    def equiv_relations(self):
        return self.get_types(BratEquivRelation)

    @property
    def attributes(self):
        return self.get_types(BratAttribute)

    @property
    def notes(self):
        return self.get_types(BratNote)