# Introduction
This library can be useful for data engineers and other developers, who need to load a JSON-files into Spark DataFrame using pySpark.

Basically Spark can infer schema of the JSON-data. But it's passable a case, when there are not all necessary 
fields in JSON-file, because they are empty. In that case these fields will not be in the resulting 
DataFrame and in its schema, and it's very bad for further data processing and can cause various errors if our 
transformations expect these fields.
Therefore, for reading JSON-file it is recommended to use the scheme explicitly.

The goal of this library is to support input data integrity when loading json data into Apache Spark Dataframe. 
For this purpose the library:
- Parses the standard json-schema and builds a Spark DataFrame schema (pyspark.sql.types.StructType)

JSON-schema must meet the standard [json-schema.org](json-schema.org).

The generated schema can be used when loading json data into Spark.

# Quickstart
Example of usage - see [example.py](example.py)

You could use ```make``` in terminal:
- ```make init``` - to prepare the virtual environment and to install all requirements 
- ```make test``` - to run tests
- ```make run``` - to run an example ([example.py](example.py))
- ```make clean``` - to clean project directory

# JSON

The root of the JSON-schema is required to be:
- type 'object' and to have a field 'properties' having the contents of the schema
- or a field 'definitions' and '$ref'-field with reference to a main structure inside 'definitions'

In order to use such a reference in the schema the corresponding field name should be '$ref'.
The value is the address in the definitions, i.e. the path following the first occurrence of
'#/definitions/' will be applied on the definitions field. So a reference will look 
like: "$ref": "#/definitions/path/to/struct"

## License

This repository is released under version 2.0 of the 
[Apache License](https://www.apache.org/licenses/LICENSE-2.0).
