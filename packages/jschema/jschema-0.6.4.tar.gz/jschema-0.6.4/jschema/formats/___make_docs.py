# -*- coding: utf-8 -*-
"""
TODO: refactoring
import os
import io

from jinja2 import Environment, FileSystemLoader

from jschema.errors import JrsMakeError

MODULE_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_INDEX_PATH = os.path.join(MODULE_DIR, "templates/docs_index.j2")
DEFAULT_SCHEMA_PATH = os.path.join(MODULE_DIR, "templates/docs_schema.j2")


def make_docs(schemas, options):
    if "dst" not in options:
        raise JrsMakeError("options['dst'] not exists")

    dst = options["dst"]
    if not os.path.exists(dst):
        os.makedirs(dst)

    index_path = DEFAULT_INDEX_PATH
    schema_path = DEFAULT_SCHEMA_PATH
    if "index_path" in options:
        index_path = os.path.abspath(options["index_path"])
    if "schema_path" in options:
        schema_path = os.path.abspath(options["schema_path"])

    if not os.path.exists(index_path):
        raise JrsMakeError("File not exists: '{}'".format(index_path))

    if not os.path.exists(schema_path):
        raise JrsMakeError("File not exists: '{}'".format(schema_path))

    SCHEMAS_DIR = os.path.join(dst, "schemas")
    if not os.path.exists(SCHEMAS_DIR):
        os.mkdir(SCHEMAS_DIR)

    index_dir, index_name = index_path.rsplit("/", 1)
    j2 = Environment(loader=FileSystemLoader(index_dir), trim_blocks=True, lstrip_blocks=True)
    docs_index = j2.get_template(index_name)

    with io.open(os.path.join(dst, "index.md"), "w", encoding="utf-8") as fstream:
        fstream.write(docs_index.render({"schemas": schemas}))

    schema_dir, schema_name = schema_path.rsplit("/", 1)
    j2 = Environment(loader=FileSystemLoader(schema_dir), trim_blocks=True, lstrip_blocks=True,
        extensions=["jinja2.ext.with_"])
    j2.filters["type"] = lambda value, expected: type(value) == expected
    j2.filters["intersectionAny"] = lambda arr1, arr2: len(set(arr1).intersection(arr2)) > 0
    j2.filters["intersectionValue"] = lambda arr1, arr2: list(set(arr1).intersection(arr2))[0]
    docs_schema = j2.get_template(schema_name)

    for sch in schemas.itervalues():
        with io.open(os.path.join(SCHEMAS_DIR, sch["id"] + ".md"), "w", encoding="utf-8") as fstream:
            fstream.write(docs_schema.render({"schema": sch}))
"""
