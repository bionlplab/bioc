"""
Deprecated. Please use `bioc.biocxml.encoder`
"""

import warnings

import bioc.biocxml.encoder


def encode_document(obj):
    """Encode a single document."""
    warnings.warn("deprecated. Please use bioc.biocxml.encoder.encode_document", DeprecationWarning)
    return bioc.biocxml.encoder.encode_document(obj)


def encode_passage(obj):
    """Encode a single passage."""
    warnings.warn("deprecated. Please use bioc.biocxml.encoder.encode_passage", DeprecationWarning)
    return bioc.biocxml.encoder.encode_passage(obj)


def encode_sentence(obj):
    """Encode a single sentence."""
    warnings.warn("deprecated. Please use bioc.biocxml.encoder.encode_sentence", DeprecationWarning)
    return bioc.biocxml.encoder.encode_sentence(obj)


def encode_annotation(obj):
    """Encode a single annotation."""
    warnings.warn("deprecated. Please use bioc.biocxml.encoder.encode_annotation",
                  DeprecationWarning)
    return bioc.biocxml.encoder.encode_annotation(obj)


def encode_relation(obj):
    """Encode a single relation."""
    warnings.warn("deprecated. Please use bioc.biocxml.encoder.encode_relation", DeprecationWarning)
    return bioc.biocxml.encoder.encode_relation(obj)


def encode_infon(k, v):
    warnings.warn("deprecated. Please use bioc.biocxml.encoder.encode_infon", DeprecationWarning)
    return bioc.biocxml.encoder.encode_infon(k, v)
