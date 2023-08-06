# -*- coding: utf-8 -*-
import os
import json

from ._options import Options
from ._dump_methods import dump_methods


def format_json(schema, options):
    opts = Options(options)
    formated = dump_methods(schema)
    for ns in formated:
        for method, sch in formated[ns].items():
            if ns == "default":
                key = method
            else:
                key = "{}.{}".format(ns, method)

            dst = os.path.join(opts.dst, schema.schemas_dirs[key])
            if not os.path.exists(dst):
                os.makedirs(dst)

            fpath =os.path.join(dst, "{}.json".format(key.replace(".", "_")))
            with open(fpath, "w") as fstream:
                fstream.write(json.dumps(sch, indent=2, separators=(",", ": ")) + "\n")
