# -*- coding: utf-8 -*-
import re


def parse_options(options_string):
    options = {}
    for item in re.split(r"\s+", options_string.strip()):
        key, val = item.split(":", 1)
        options[key] = val

    return options
