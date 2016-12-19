============================================

`BioC XML format <http://bioc.sourceforge.net/>`_ can be used to share
text documents and annotations.

``bioc`` exposes an API familiar to users of the standard library
``marshal`` and ``pickle`` modules.

Development of ``bioc`` happens on GitHub:
https://github.com/yfpeng/pengyifan-pybioc

Getting started
---------------

Installing ``bioc``

::

    $ pip install --pre bioc

Encoding the BioC collection object \`collection':

::

    import bioc
    # Serialize ``collection`` to a BioC formatted ``str``.
    bioc.dumps(collection)

    # Serialize ``collection`` as a BioC formatted stream to ``fp``.
    with open(filename, 'w') as fp
        bioc.dump(collection, fp)

Compact encoding:

::

    import bioc
    bioc.dumps(collection, pretty_print=False)

Decoding the BioC XML file:

::

    import json
    # Deserialize ``s`` to a BioC collection object.
    collection = json.loads(s)
    # Deserialize ``fp`` to a BioC collection object.
    with open(filename, 'r') as fp:
        bioc.load(fp)

Requirements
------------

`lxml <http://lxml.de/>`_

Developers
----------

-  Yifan Peng (yifan.peng@nih.gov)

Acknowledgment
--------------

-  `Hernani Marques <https://github.com/2mh/PyBioC/>`_

Webpage
-------

The official BioC webpage is available with all up-to-date instructions,
code, and corpora in the BioC format, and other research on, based on
and related to BioC.

-  http://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/BioC/
-  http://bioc.sourceforge.net/

Reference
---------

-  Comeau,D.C., Doğan,R.I., Ciccarese,P., Cohen,K.B., Krallinger,M.,
   Leitner,F., Lu,Z., Peng,Y., Rinaldi,F., Torii,M., Valencia,V.,
   Verspoor,K., Wiegers,T.C., Wu,C.H., Wilbur,W.J. (2013) BioC: A
   minimalist approach to interoperability for biomedical text
   processing. Database: The Journal of Biological Databases and
   Curation.
-  Peng,Y., Tudor,C., Torii,M., Wu,C.H., Vijay-Shanker,K. (2014) iSimp
   in BioC standard format: Enhancing the interoperability of a sentence
   simplification system. Database: The Journal of Biological Databases
   and Curation.
-  Marques,M., Rinaldi,F. (2012) PyBioC: a python implementation of the
   BioC core. In Proceedings of BioCreative IV workshop.
