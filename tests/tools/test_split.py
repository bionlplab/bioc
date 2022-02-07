import math
import string
import tempfile

import bioc
from bioc.tools import split
import random


def get_random_str():
    return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=random.randint(10, 500)))


def get_collection(total_doc):
    c = bioc.BioCCollection()
    c.source = 'source'
    for i in range(total_doc):
        text = get_random_str()
        doc = bioc.BioCDocument.of_text(text)
        c.add_document(doc)
    return c


def test_itersplit():
    total_doc = 230
    n = 7
    c = get_collection(total_doc)
    cs = list(split.itersplit(c, n))
    for i in range(int(total_doc / n)):
        subc = cs[i]
        assert len(subc.documents) == n

    last_n = int(math.ceil(total_doc / n)) - 1
    if last_n > int(total_doc / n):
        subc = cs[last_n]
        assert len(subc.documents) == total_doc % n


def test_split_file():
    total_doc = 230
    n = 7
    c = get_collection(total_doc)

    top_dir = tempfile.mkdtemp()
    _, source = tempfile.mkstemp(suffix='.xml', dir=top_dir)
    with open(source, 'w') as fp:
        bioc.dump(c, fp)

    split.split_file(source, prefix=top_dir, num_doc=n)
    for i in range(int(total_doc/n)):
        source = top_dir + '{:02x}.xml'.format(i)
        with open(source) as fp:
            subc = bioc.load(fp)
            assert len(subc.documents) == n

    last_n = int(math.ceil(total_doc/n)) - 1
    if last_n > int(total_doc/n):
        source = top_dir + '{:02x}.xml'.format(last_n)
        with open(source) as fp:
            subc = bioc.load(fp)
            assert len(subc.documents) == total_doc % n
