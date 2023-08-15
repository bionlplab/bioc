
from typing import Generator

import tqdm
import bioc


def itersplit(collection: bioc.BioCCollection, num_doc: int) -> Generator[bioc.BioCCollection, None, None]:
    subc = bioc.BioCCollection()
    subc = subc.copy_infon(collection)

    for doc in collection.documents:
        subc.add_document(doc)
        if len(subc.documents) == num_doc:
            yield subc
            subc = bioc.BioCCollection()
            subc = subc.copy_infon(collection)
    if subc.documents:
        yield subc


def split_file(source, *,
               prefix: str,
               num_doc: int,
               additional_suffix: str = '.xml',
               suffix_length: int = 2):
    path_format = prefix + '{:0' + str(suffix_length) + 'x}' \
                  + additional_suffix

    with open(source, encoding='utf8') as fp:
        collection = bioc.load(fp)

    for i, subc in tqdm.tqdm(enumerate(itersplit(collection, num_doc))):
        dst = path_format.format(i)
        with open(dst, 'w', encoding='utf8') as fp:
            bioc.dump(subc, fp)
