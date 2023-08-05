import json
import os
import sys
from collections import OrderedDict
import logging
import jsonschema

log = logging.getLogger("mappyfile")

PY2 = sys.version_info[0] < 3
if PY2:
    str = unicode # NOQA


class Validator(object):

    def __init__(self):
        self.schemas = {}

    def get_schema_path(self, schemas_folder):
        """
        Return a file protocol URI e.g. file:///D:/mappyfile/mappyfile/schemas/ on Windows
        and file:////home/user/mappyfile/mappyfile/schemas/ on Linux
        """

        # replace any Windows path back slashes with forward slashes
        schemas_folder = schemas_folder.replace("\\", "/")

        # HACK Python 2.7 on Linux seems to remove the root slash
        # add this back in
        if schemas_folder.startswith("/"):
            schemas_folder = "/" + schemas_folder

        host = ""
        root_schema_path = "file://{}/{}".format(host, schemas_folder) + "/"

        return root_schema_path

    def get_schema(self, schema_name):
        """
        Had to remove the id property from map.json or it uses URLs for validation
        See various issues at https://github.com/Julian/jsonschema/pull/306
        """

        schema_name += ".json"

        if schema_name not in self.schemas.keys():

            schemas_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "schemas")
            schema_file = os.path.join(schemas_folder, schema_name)

            if not os.path.isfile(schema_file):
                raise IOError("The file %s does not exist" % schema_file)

            with open(schema_file) as f:
                try:
                    jsn_schema = json.loads(f.read())
                except ValueError as ex:
                    log.error("Could not load %s", schema_file)
                    raise ex

            root_schema_path = self.get_schema_path(schemas_folder)
            resolver = jsonschema.RefResolver(root_schema_path, None)
            # cache the schema for future use
            self.schemas[schema_name] = (jsn_schema, resolver)
        else:
            jsn_schema, resolver = self.schemas[schema_name]

        return jsn_schema, resolver

    def convert_lowercase(self, x):

        if isinstance(x, list):
            return [self.convert_lowercase(v) for v in x]
        elif isinstance(x, dict):
            return OrderedDict((k.lower(), self.convert_lowercase(v)) for k, v in x.items())
        else:
            if isinstance(x, (str, bytes)):
                x = x.lower()

        return x

    def validate(self, d, schema_name="map"):

        jsn_schema, resolver = self.get_schema(schema_name)
        lowercase_dict = self.convert_lowercase(d)

        jsn = json.loads(json.dumps(lowercase_dict), object_pairs_hook=OrderedDict)

        try:
            jsonschema.validate(jsn, jsn_schema, resolver=resolver)
        except jsonschema.ValidationError as ex:
            log.error(ex)
            return False

        return True
