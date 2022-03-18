# XML

bioc's interfaces for processing BioC XML are grouped in the `biocxml` package.

## Encoding the BioC object

Encoding the BioC collection object `collection`:

```python
import bioc
# Serialize ``collection`` to a BioC formatted ``str``.
bioc.dumps(collection)
# Serialize ``collection`` as a BioC formatted stream to ``fp``.
with open(filename, 'w') as fp:
    bioc.dump(collection, fp)
```

Compact encoding:

```python
import bioc
bioc.dumps(collection, pretty_print=False)
```

Incremental BioC serialisation:

```python
from bioc import biocxml
with biocxml.iterwrite(filename) as writer:
    writer.write_collection_info(collection)
    for document in collection.documents:
        writer.write_document(document)
```

## Decoding the BioC XML file

Decoding the BioC XML file:

```python
import bioc
# Deserialize ``s`` to a BioC collection object.
collection = bioc.loads(s)
# Deserialize ``fp`` to a BioC collection object.
with open(filename, 'r') as fp:
    collection = bioc.load(fp)
```

Incrementally decoding the BioC XML file:

```python
from bioc import biocxml
# read from a file
with biocxml.iterparse(filename) as reader:
    collection_info = reader.get_collection_info()
    for document in reader:
        # process document
        ...
# read from a ByteIO
with biocxml.iterparse(open(filename, 'rb')) as reader:
    collection_info = reader.get_collection_info()
    for document in reader:
        # process document
        ...
```

`get_collection_info` can be called after the `with` statement.

Together with Python coroutines, this can be used to generate BioC XML
in an asynchronous, non-blocking fashion.

```python
from bioc import biocxml

with biocxml.iterparse(source) as reader, biocxml.iterwrite(dest) as writer:
    collection_info = reader.get_collection_info()
    writer.write_collection_info(collection_info)
    for document in reader:
        # modify the document
        ...
        writer.write_document(document)
```