# -*- coding: utf-8 -*-
from ._options import Options
from ._dump_methods import dump_methods
from ._jinja2_env import jinja2_env


def format_js(schema, options):
    opts = Options(options)
    template = jinja2_env.get_template("schema_js.j2")

    with open(opts.dst, "w") as fstream:
        fstream.write(template.render({"schemas": dump_methods(schema)}))
