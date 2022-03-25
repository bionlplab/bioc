# BioC Json

## Encoding the BioC object

Encoding the BioC collection object `collection`:

```python
import bioc

# Serialize ``collection`` to a BioC Json formatted ``str``.
bioc.dumps(collection, BioCFileType.BIOC_JSON, indent=2)

# Serialize ``collection`` as a BioC Json formatted stream to ``fp``.
with open(filename, 'w') as fp
    bioc.dump(collection, BioCFileType.BIOC_JSON, fp, indent=2)
```

Compact encoding:

```python
import bioc
bioc.dumps(collection, BioCFileType.BIOC_JSON)
```

## Decoding the BioC Json file

```python
import bioc

# Deserialize ``s`` to a BioC collection object.
collection = bioc.loads(s, BioCFileType.BIOC_JSON)

# Deserialize ``fp`` to a BioC collection object.
with open(filename, 'r') as fp:
    collection = bioc.load(fp, BioCFileType.BIOC_JSON)
```

## Json Lines

Incrementally encoding the BioC structure:

```python
from bioc import BioCJsonIterWriter
with open(filename, 'w', encoding='utf8') as fp:
    writer = BioCJsonIterWriter(fp, level=bioc.PASSAGE)
    for doc in collection.documents:
         for passage in doc.passages:
             writer.write(passage)
```

or

```python
from bioc import toJSON
import jsonlines
with jsonlines.open(filename, 'w') as writer:
    for doc in collection.documents:
         for passage in doc.passages:
             writer.write(toJSON(passage))
```

Incrementally decoding the BioC Json lines file:

```python
from bioc import BioCJsonIterReader
with open(filename, 'r', encoding='utf8') as fp:
    reader = BioCJsonIterReader(fp, level=bioc.PASSAGE)
    for passage in reader:
        # process passage
        ...
```

or

```python
from bioc import fromJSON
import jsonlines
with jsonlines.open(filename) as reader:
    for obj in reader:
        passage = fromJSON(obj, level=bioc.PASSAGE)
        ...
```

