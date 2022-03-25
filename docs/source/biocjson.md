# BioC Json

## Encoding the BioC object

Encoding the BioC collection object `collection`:

```python
from bioc import biocjson

# Serialize ``collection`` to a BioC Json formatted ``str``.
biocjson.dumps(collection, indent=2)

# Serialize ``collection`` as a BioC Json formatted stream to ``fp``.
with open(filename, 'w') as fp
    biocjson.dump(collection, fp, indent=2)
```

Compact encoding:

```python
from bioc import biocjson
biocjson.dumps(collection)
```

## Decoding the BioC Json file

```python
from bioc import biocjson

# Deserialize ``s`` to a BioC collection object.
collection = biocjson.loads(s)

# Deserialize ``fp`` to a BioC collection object.
with open(filename, 'r') as fp:
    collection = biocjson.load(fp)
```

## Json Lines

Incrementally encoding the BioC structure:

```python
import bioc
from bioc.biocjson import BioCJsonIterWriter

with open(filename, 'w', encoding='utf8') as fp:
    writer = BioCJsonIterWriter(fp, level=bioc.PASSAGE)
    for doc in collection.documents:
         for passage in doc.passages:
             writer.write(passage)
```

or

```python
from bioc import biocjson
import jsonlines
with jsonlines.open(filename, 'w') as writer:
    for doc in collection.documents:
         for passage in doc.passages:
             writer.write(biocjson.toJSON(passage))
```

Incrementally decoding the BioC Json lines file:

```python
import bioc
from bioc.biocjson import BioCJsonIterReader
with open(filename, 'r', encoding='utf8') as fp:
    reader = BioCJsonIterReader(fp, level=bioc.PASSAGE)
    for passage in reader:
        # process passage
        ...
```

or

```python
import bioc
from bioc import biocjson
import jsonlines
with jsonlines.open(filename) as reader:
    for obj in reader:
        passage = biocjson.fromJSON(obj, level=bioc.PASSAGE)
        ...
```

