"""
Loads str/file-obj to a list of Pubtator objects
"""
from typing import List


class PubTatorAnn:
    def __init__(self, pmid: str, start: int, end: int, text: str, type: str, id: str):
        self.pmid = pmid
        self.start = start
        self.end = end
        self.text = text
        self.type = type
        self.id = id

    def __str__(self):
        return '{self.pmid}\t{self.start}\t{self.end}\t{self.text}\t{self.type}\t{self.id}'.format(self=self)


class PubTatorRel:
    def __init__(self, pmid, type, id1, id2):
        self.pmid = pmid
        self.type = type
        self.id1 = id1
        self.id2 = id2

    def __str__(self):
        return '{self.pmid}\t{self.type}\t{self.id1}\t{self.id2}'.format(self=self)


class PubTator:
    def __init__(self, pmid: str = None, title: str = None, abstract: str = None):
        self.pmid = pmid  # type: str
        self.title = title  # type: str
        self.abstract = abstract  # type: str
        self.annotations = []  # type: List[PubTatorAnn]
        self.relations = []  # type: List[PubTatorRel]

    def add_annotation(self, ann: PubTatorAnn):
        self.annotations.append(ann)

    def add_relation(self, rel: PubTatorRel):
        self.relations.append(rel)

    def get_annotation(self, concept_id: str, multiple_ids: bool = True, default = None) -> PubTatorAnn:
        """
        :param multiple_ids: one entity may have multiple concept ids.
        """
        for ann in self.annotations:
            if multiple_ids and concept_id in ann.id:
                return ann
            elif ann.id == concept_id:
                return ann
        return default

    def __str__(self):
        text = self.pmid + '|t|' + self.title + '\n'
        if self.abstract:
            text += self.pmid + '|a|' + self.abstract + '\n'
        for ann in self.annotations:
            text += '{}\n'.format(ann)
        for rel in self.relations:
            text += '{}\n'.format(rel)
        return text

    @property
    def text(self) -> str:
        """
        str: text
        """
        text = self.title
        if self.abstract:
            text += '\n' + self.abstract
        return text
