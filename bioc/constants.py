"""
Constants
"""
from enum import Enum

DOCUMENT = 1
PASSAGE = 2
SENTENCE = 3


class BioCFileType(Enum):
    BIOC_XML = 1
    BIOC_JSON = 2


class BioCVersion(Enum):
    V1 = 1
    V2 = 2