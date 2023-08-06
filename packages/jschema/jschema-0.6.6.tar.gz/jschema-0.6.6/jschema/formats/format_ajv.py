# -*- coding: utf-8 -*-
import os

from jschema import __version__

from ._options import Options
from ._dump_methods import dump_methods
from ._jinja2_env import jinja2_env


def format_ajv(schema, options):
    opts = Options(options)
    template = jinja2_env.get_template("schema_ajv.j2")

    for key, sch in schema.schemas.items():
        if sch["type"] != "method":
            continue

        dst = os.path.join(opts.dst, schema.schemas_dirs[key])
        if not os.path.exists(dst):
            os.makedirs(dst)

        name = key.replace(".", "_")

        file_path = os.path.join(dst, name + ".js")
        with open(file_path, "w") as fstream:
            fstream.write(template.render({
                "schema": sch,
                "jschemaVersion": __version__
            }))
        print(" - Created: {}".format(file_path))
