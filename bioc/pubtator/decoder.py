import logging
import re
from typing import List, Generator, TextIO, Iterator, Union

from bioc.pubtator.pubtator import PubTator, PubTatorAnn, PubTatorRel

ABSTRACT_PATTERN = re.compile(r'(.*?)\|a\|(.*)')
TITLE_PATTERN = re.compile(r'(.*?)\|t\|(.*)')


def loads(s: str) -> List[PubTator]:
    """
    Parse s (a str) to a list of Pubtator documents

    Returns:
        list: a list of PubTator documents
    """
    return list(iterparse_s(s.splitlines()))


def load(fp: TextIO) -> List[PubTator]:
    """
    Parse file-like object to a list of Pubtator documents

    Args:
        fp: file-like object

    Returns:
        list: a list of PubTator documents
    """
    return loads(fp.read())


def iterparse_s(line_iterator: Iterator[str]) -> Generator[PubTator, None, None]:
    """
    Iterative parse each line
    """
    logger = logging.getLogger(__name__)
    doc = PubTator()
    i = 0
    for i, line in enumerate(line_iterator, 1):
        if i % 100000 == 0:
            logger.debug('Read %d lines', i)
        line = line.strip()
        if not line:
            if doc.pmid and (doc.title or doc.abstract):
                yield doc
            doc = PubTator()
            continue
        matcher = TITLE_PATTERN.match(line)
        if matcher:
            doc.pmid = matcher.group(1)
            doc.title = matcher.group(2)
            continue
        matcher = ABSTRACT_PATTERN.match(line)
        if matcher:
            doc.pmid = matcher.group(1)
            doc.abstract = matcher.group(2)
            continue
        toks = line.split('\t')
        if len(toks) >= 6:
            annotation = loads_ann(toks)
            doc.add_annotation(annotation)
        if len(toks) == 4:
            relation = PubTatorRel(toks[0], toks[1], toks[2], toks[3])
            doc.add_relation(relation)

    if doc.pmid and (doc.title or doc.abstract):
        yield doc
    logger.debug('Read %d lines', i)


def iterparse(fp: TextIO) -> Generator[PubTator, None, None]:
    """
    Iteratively parse fp (file-like object) in pubtator format
    """
    return iterparse_s(fp)


def loads_ann(s: Union[str, List[str]]) -> PubTatorAnn:
    """
    Parse s (a str) in the Pubtator annotation format
    """
    if isinstance(s, str):
        toks = s.split('\t')
    else:
        toks = s

    if len(toks) == 6:
        return PubTatorAnn(pmid=toks[0], start=int(toks[1]), end=int(toks[2]), text=toks[3], type=toks[4], id=toks[5])

    if len(toks) == 7 and '|' in toks[5] and '|' in toks[6]:
        ids = toks[5].split('|')
        texts = toks[6].split('|')
        if len(ids) != len(texts):
            raise ValueError('Cannot parse entity. %s concept but %s text. %s' % (len(ids), len(texts), s))
        return PubTatorAnn(pmid=toks[0], start=int(toks[1]), end=int(toks[2]), text=toks[3], type=toks[4], id=toks[5])

    raise ValueError('Cannot parse: %s' % s)
