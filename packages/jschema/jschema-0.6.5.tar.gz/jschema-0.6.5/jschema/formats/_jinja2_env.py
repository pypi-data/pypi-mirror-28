# -*- coding: utf-8 -*-
import os

from jinja2 import Environment, FileSystemLoader

from ._filters import json_dumps_filter
from ._filters import upper_camel_case_filter
from ._filters import camel_case_filter

jinja2_env = Environment(
    loader=FileSystemLoader(os.path.join(str(os.path.dirname(__file__)), "templates")),
    trim_blocks=True,
    lstrip_blocks=True,
    extensions=["jinja2.ext.with_"]
)
jinja2_env.filters["jsonDumps"] = json_dumps_filter
jinja2_env.filters["upperCamelCase"] = upper_camel_case_filter
jinja2_env.filters["camelCase"] = camel_case_filter
jinja2_env.filters["ljust"] = lambda value, size: value.ljust(size)
