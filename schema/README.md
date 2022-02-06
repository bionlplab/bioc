## Validate XML schema

```shell
$ sudo apt install libxml2-utils
$ xmllint --noout --schema schema/bioc_v1.xsd tests/bioc/everything.xml
$ xmllint --noout --schema schema/bioc_v2.xsd tests/bioc/everything_v2.xml 
```

## Validate DTD
```shell
$ xmllint --noout --dtdvalid schema/bioc_v1.dtd tests/bioc/everything.xml
$ xmllint --noout --dtdvalid schema/bioc_v2.dtd tests/bioc/everything_v2.xml 
```

## Validate JSON schema
```shell
$ pip install jsonschema
$ jsonschema --instance ./tests/bioc/everything.json ./schema/bioc_schema.json
```