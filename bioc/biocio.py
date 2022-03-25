# from typing import TextIO
#
# from bioc.bioc.constants import BioCFileType, BioCVersion
# from bioc.bioc.bioc import BioCCollection
# from bioc.bioc.biocjson import loads as jsonloads, dump as jsondump, load as jsonload, dumps as jsondumps
# from bioc.bioc.biocxml import loads as xmlloads, dump as xmldump, load as xmlload, dumps as xmldumps
#
#
# def loads(s: str, filetype: BioCFileType = BioCFileType.BIOC_XML, version: BioCVersion = BioCVersion.V1,
#           **kwargs) -> BioCCollection:
#     """
#     Deserialize ``s`` (a ``str`` instance containing a BioC collection) to a BioC collection object.
#     """
#     if filetype == BioCFileType.BIOC_XML:
#         return xmlloads(s, version)
#     elif filetype == BioCFileType.BIOC_JSON:
#         return jsonloads(s, **kwargs)
#     else:
#         raise ValueError
#
#
# def dump(collection: BioCCollection, fp: TextIO, filetype: BioCFileType = BioCFileType.BIOC_XML,
#          version: BioCVersion = BioCVersion.V1, **kwargs):
#     """
#     Serialize ``collection`` as a BioC formatted stream to ``fp``.
#     """
#     if filetype == BioCFileType.BIOC_XML:
#         return xmldump(collection, fp, version, **kwargs)
#     elif filetype == BioCFileType.BIOC_JSON:
#         return jsondump(collection, fp, **kwargs)
#     else:
#         raise ValueError
#
#
# def load(fp: TextIO, filetype: BioCFileType = BioCFileType.BIOC_XML, version: BioCVersion = BioCVersion.V1,
#          **kwargs) -> BioCCollection:
#     """
#     Deserialize ``fp`` (a ``.read()``-supporting file-like object containing a BioC collection)
#     to a BioC collection object.
#     """
#     if filetype == BioCFileType.BIOC_XML:
#         return xmlload(fp, version)
#     elif filetype == BioCFileType.BIOC_JSON:
#         return jsonload(fp, **kwargs)
#     else:
#         raise ValueError
#
#
# def dumps(collection: BioCCollection, filetype: BioCFileType = BioCFileType.BIOC_XML,
#           version: BioCVersion = BioCVersion.V1, **kwargs) -> str:
#     """
#     Serialize ``collection`` to a BioC formatted ``str``.
#     """
#     if filetype == BioCFileType.BIOC_XML:
#         return xmldumps(collection, version, **kwargs)
#     elif filetype == BioCFileType.BIOC_JSON:
#         return jsondumps(collection, **kwargs)
#     else:
#         raise ValueError