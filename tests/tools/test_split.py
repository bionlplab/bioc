import math
import string
import tempfile

import bioc
from bioc.tools import split
import random


def get_random_str():
    return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=random.randint(10, 500)))


def test_split():
    total_doc = 230
    n = 7
    c = bioc.BioCCollection()
    c.source = 'source'
    for i in range(total_doc):
        text = get_random_str()
        print(text)
        doc = bioc.BioCDocument.of_text(text)
        c.add_document(doc)

    top_dir = tempfile.mkdtemp()
    _, source = tempfile.mkstemp(suffix='.xml', dir=top_dir)
    with open(source, 'w') as fp:
        bioc.dump(c, fp)

    split.split(source, prefix=top_dir, num_doc=n)
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

