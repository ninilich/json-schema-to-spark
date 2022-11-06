# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
from JsonToSparkSchema.converter import SchemaConverter
from pyspark.sql import SparkSession

schema_file = 'tests/test_data/schema_simple1.json'
data_file = 'tests/test_data/data_simple1.json'

# read file with json schema
with open(schema_file) as file:
    json_schema = json.load(file)

# use JsonToSparkSchemaConverter
converter = SchemaConverter(json_schema)
schema_for_spark = converter.schema_for_spark

spark = SparkSession \
    .builder \
    .appName("Converter_Example") \
    .getOrCreate()

# read json-file with Spark using converted schema:
df = spark.read \
    .option("multiline", "false") \
    .schema(schema_for_spark)\
    .json(data_file)

# just to check
df.printSchema()
df.show()


