`bioc` - BioC data structures and encoder/decoder for Python
=============================================================

.. .. image:: https://img.shields.io/travis/yfpeng/bioc.svg
..    :alt: Build status
..    :target: https://travis-ci.org/yfpeng/bioc

.. image:: https://github.com/yfpeng/bioc/workflows/bioc/badge.svg
   :alt: Build status
   :target: https://github.com/yfpeng/bioc/

.. image:: https://img.shields.io/pypi/v/bioc.svg
   :target: https://pypi.python.org/pypi/bioc
   :alt: Latest version on PyPI

.. image:: https://img.shields.io/pypi/dm/bioc.svg
   :alt: Downloads
   :target: https://pypi.python.org/pypi/bioc
   
..  .. image:: https://coveralls.io/repos/github/yfpeng/bioc/badge.svg?branch=master
..    :alt: Coverage
..    :target: https://pypi.python.org/pypi/bioc
   
.. image:: https://codecov.io/gh/yfpeng/bioc/branch/master/graph/badge.svg
   :alt: Coverage
   :target: https://codecov.io/gh/yfpeng/bioc
   
.. image:: https://requires.io/github/yfpeng/bioc/requirements.svg?branch=master
   :target: https://requires.io/github/yfpeng/bioc/requirements/?branch=master
   :alt: Requirements Status

.. image:: https://img.shields.io/pypi/l/bioc.svg
   :alt: License
   :target: https://opensource.org/licenses/BSD-3-Clause
   
.. image:: https://hits.dwyl.com/yfpeng/bioc.svg
   :alt: Hits
   :target: https://hits.dwyl.com/yfpeng/bioc




`BioC XML / JSON format <http://bioc.sourceforge.net/>`_ can be used to share
text documents and annotations.

``bioc`` exposes an API familiar to users of the standard library
``marshal`` and ``pickle`` modules.

Development of ``bioc`` happens on GitHub:
https://github.com/yfpeng/bioc

Getting started
---------------

Installing ``bioc``

.. code:: bash

    $ pip install bioc

XML
~~~

Encoding the BioC collection object ``collection``:

.. code:: python

    import bioc
    # Serialize ``collection`` to a BioC formatted ``str``.
    bioc.dumps(collection)

    # Serialize ``collection`` as a BioC formatted stream to ``fp``.
    with open(filename, 'w') as fp
        bioc.dump(collection, fp)

Compact encoding:

.. code:: python

    import bioc
    bioc.dumps(collection, pretty_print=False)

Incremental BioC serialisation:

.. code:: python

    import bioc
    with bioc.BioCXMLDocumentWriter(filename) as writer:
        writer.write_collection_info(collection)
        for document in collection.documents:
            writer.write_document(document)

Decoding the BioC XML file:

.. code:: python

    import bioc
    # Deserialize ``s`` to a BioC collection object.
    collection = bioc.loads(s)

    # Deserialize ``fp`` to a BioC collection object.
    with open(filename, 'r') as fp:
        collection = bioc.load(fp)

Incrementally decoding the BioC XML file:

.. code:: python

    import bioc
    with bioc.BioCXMLDocumentReader(filename) as reader:
        collection_info = reader.get_collection_info()
        for document in reader:
            # process document
            ...

``get_collection_info`` can be called after the construction of the ``BioCXMLDocumentReader`` anytime.

Together with Python coroutines, this can be used to generate BioC XML in an asynchronous, non-blocking fashion.

.. code:: python

    import bioc
    with bioc.BioCXMLDocumentReader(source) as reader, \
         bioc.BioCXMLDocumentWriter(dest) as writer:
        collection_info = reader.get_collection_info()
        writer.write_collection_info(collection_info)
        for document in reader:
            # modify the document
            ...
            writer.write_document(document)

Json
~~~~

Encoding the BioC collection object ``collection``:

.. code:: python

    import biocjson
    # Serialize ``collection`` to a BioC Json formatted ``str``.
    biocjson.dumps(collection, indent=2)

    # Serialize ``collection`` as a BioC Json formatted stream to ``fp``.
    with open(filename, 'w') as fp
        biocjson.dump(collection, fp, indent=2)

Compact encoding:

.. code:: python

    import biocjson
    biocjson.dumps(collection)

Decoding the BioC Json file:

.. code:: python

    import biocjson
    # Deserialize ``s`` to a BioC collection object.
    collection = biocjson.loads(s)

    # Deserialize ``fp`` to a BioC collection object.
    with open(filename, 'r') as fp:
        collection = biocjson.load(fp)

Json Lines
~~~~~~~~~~

Incrementally encoding the BioC structure:

.. code:: python

    from bioc.biocjson import BioCJsonIterWriter
    with BioCJsonIterWriter(filename, level=bioc.PASSAGE) as writer:
        for doc in collection.documents:
             for passage in doc.passages:
                 writer.write(passage)

or

.. code:: python

    from bioc.biocjson import toJSON
    import jsonlines
    with jsonlines.open(filename, 'w') as writer:
        for doc in collection.documents:
             for passage in doc.passages:
                 writer.write(toJSON(passage))

Incrementally decoding the BioC Json lines file:

.. code:: python

    from bioc.biocjson import BioCJsonIterReader
    with BioCJsonIterReader(filename, level=bioc.PASSAGE) as reader:
        for passage in reader:
            # process passage
            ...

or

.. code:: python

    from bioc.biocjson import fromJSON
    import jsonlines
    with jsonlines.open(filename) as reader:
        for obj in reader:
            passage = fromJSON(obj, level=bioc.PASSAGE)
            ...

Developers
----------

-  Yifan Peng (yifan.peng@nih.gov)

Acknowledgment
--------------

-  Hernani Marques (https://github.com/2mh/PyBioC)

Webpage
-------

The official BioC webpage is available with all up-to-date instructions,
code, and corpora in the BioC format, and other research on, based on
and related to BioC.

-  http://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/BioC/
-  http://bioc.sourceforge.net/


Reference
---------

If you use bioc in your research, please cite the following paper:

-  Peng,Y., Tudor,C., Torii,M., Wu,C.H., Vijay-Shanker,K. (2014) iSimp
   in BioC standard format: Enhancing the interoperability of a sentence
   simplification system. Database: The Journal of Biological Databases
   and Curation.

