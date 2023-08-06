# -*- coding: utf-8 -*-
import os
from ..errors import JrsFormatingError
from ._options import Options
from ._dump_methods import dump_methods
from ._jinja2_env import jinja2_env


def format_golang(schema, options):
    opts = Options(options)
    template = jinja2_env.get_template("method_meta_golang.j2")

    for key, sch in schema.schemas.items():
        if sch["type"] != "method":
            continue

        key_split = key.split(".")
        if len(key_split) == 1:
            ns = opts.ns
            name = key_split[0]
        elif len(key_split) == 2:
            ns = key_split[0]
            name = key_split[1]
        else:
            raise JrsFormatingError("Expect zero or one dot in schema id")

        sch_dir = os.path.join(opts.dst, schema.schemas_dirs[key])
        if not os.path.exists(sch_dir):
            os.makedirs(sch_dir)

        package = schema.schemas_dirs[key].rsplit("/", 1)[-1]
        if package == "":
            package = sch_dir.strip("/").rsplit("/", 1)[-1]

        sch_path = os.path.join(sch_dir, key.replace(".", "_") + "_meta.go")
        with open(sch_path, "w") as fstream:
            fstream.write(template.render({
                "package": package,
                "ns": ns,
                "name": name,
                "schema": sch
            }))
        print(" - Created: {}".format(sch_path))
