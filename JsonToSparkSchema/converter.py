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

# Schema Converter to convert schema from json format into Spark StructType


from pyspark.sql.types import *


class SchemaConverter:
    """
    Class to convert standard JSON-schema (json-schema.org) to pyspark.sql.types.StructType.

    Supported types are: "string", "number" (double), "float", "integer" (long), "boolean", "object" and "array".
    The root of the JSON-schema is required to be:
     - type 'object' and to have a field 'properties' having the contents of the schema
     - or a field 'definitions' and '$ref'-field with reference to a main structure inside 'definitions'
    In order to use such a reference in the schema the corresponding field name should be '$ref'.
    The value is the address in the definitions, i.e. the path following the first occurrence of '#/definitions/'
    will be applied on the definitions field. So a reference will look like: "$ref": "#/definitions/path/to/struct"

    There isn't validation of input JSON-schema.
    """

    # Supported simple types
    SimpleTypeMap = {
        "string": StringType(),
        "number": DoubleType(),
        "float": FloatType(),
        "integer": LongType(),
        "boolean": BooleanType()
    }

    def __init__(self, js: dict):
        # Original standard JSON-schema (json-schema.org)
        self.json_schema = js
        # Main element to build schema
        if "$ref" in self.json_schema:
            self._main_element = self._get_ref_object(self.json_schema.get("$ref"))
        elif "properties" in self.json_schema:
            self._main_element = self.json_schema
        else:
            raise Exception("Format of JSON-Schema is not recognized by JsonToSparkSchemaConverter")
        # Converting schema
        self._build_schema_from_json()

    def _get_ref_object(self, ref: str) -> dict:
        """
        Get object via $ref
        :param ref: internal reference to element, f.e. '#/definitions/path_to_element'
        :return: element via reference
        """
        path = ref.split('/')
        result = self.json_schema
        for i in range(1, len(path)):
            result = result.get(path[i])
        return result

    def _get_simple_field(self, _type: str) -> StructType():
        """
        Returns StructType() for simple type
        """
        return self.SimpleTypeMap.get(_type)

    def _get_oneof_field(self, oneof_list: list) -> StructType():
        """
        Returns StructType() for 'oneOf' constructions.
        F.e. {"oneOf":[{"type":"null"},{"type":"integer"}]}
        """
        for item in oneof_list:
            if "type" in item.keys():
                if item.get("type") in self.SimpleTypeMap:
                    return self._get_simple_field(item.get("type"))
                elif item.get("type") == "array":
                    return self._get_array(item.get("items"))
                elif item.get("type") == "object":
                    return self._get_object(item.get("properties"))
            elif "$ref" in item.keys():
                obj = self._get_ref_object(item.get("$ref"))
                return self._get_object(obj.get("properties"))
        raise Exception('oneOf field is incorrect')

    def _get_array(self, _items: dict) -> StructType():
        """
        Returns StructType() for 'array'.
        F.e. {"type":"array","items":{"type":"string"}}
        """
        if "type" in _items:
            if _items.get("type") in self.SimpleTypeMap:
                return ArrayType(self.SimpleTypeMap.get(_items.get("type")))
            elif _items.get("type") == "array":
                return ArrayType(self._get_array(_items.get("items")))
            elif _items.get("type") == "object":
                return ArrayType(self._get_object(_items.get("properties")))
            else:
                raise Exception("Array element's type is not supported by JsonToSparkSchemaConverter")
        elif "$ref" in _items:
            obj = self._get_ref_object(_items.get("$ref"))
            array_type = self._get_object(obj.get("properties"))
            return ArrayType(array_type)
        else:
            raise Exception('Array type is not supported by JsonToSparkSchemaConverter')

    def _get_object(self, _properties: dict) -> StructType():
        """
        Returns StructType() for 'object'
        :param _properties: content of the 'properties'-field
        """
        result = StructType()
        for filed_name, field_info in _properties.items():
            if "type" in field_info:
                _type = field_info.get("type")
                if _type in self.SimpleTypeMap:
                    result = result.add(filed_name, self._get_simple_field(_type))
                elif _type == "array":
                    result = result.add(filed_name, self._get_array(field_info.get("items")))
                elif _type == "object":
                    result = result.add(filed_name, self._get_object(field_info.get("properties")))
            elif "oneOf" in field_info:
                result = result.add(filed_name, self._get_oneof_field(field_info.get("oneOf")))
            else:
                raise Exception('Type is not supported by JsonToSparkSchemaConverter')
        return result

    def _build_schema_from_json(self):
        """
        Main builder for schema
        """
        self.schema_for_spark = self._get_object(self._main_element.get("properties"))
