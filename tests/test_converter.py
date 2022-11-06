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
import pytest as pt
from JsonToSparkSchema.converter import SchemaConverter

test_data = [('tests/test_data/schema_simple1.json', 'tests/test_data/output_schema_simple1.json'),
             ('tests/test_data/schema_simple2.json', 'tests/test_data/output_schema_simple2.json'),
             ('tests/test_data/schema_complicated1.json', 'tests/test_data/output_schema_complicated1.json'),
             ('tests/test_data/schema_complicated2.json', 'tests/test_data/output_schema_complicated2.json')
]


@pt.mark.parametrize('test_data', test_data)
def test_schema_converter(test_data):
    in_data, out_data = test_data
    with open(in_data, 'r') as file:
        schema = json.load(file)
    with open(out_data, 'r') as file:
        output = file.read()
    converter = SchemaConverter(schema)
    output_schema = converter.schema_for_spark.json()
    assert output == output_schema

