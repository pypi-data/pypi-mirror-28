# -*- coding: utf-8 -*-


def dump_methods(schema):
    tree = {}
    for key, sch in schema.schemas.items():
        if sch["type"] == "method":
            if "." in key:
                ns, method = key.split(".")
            else:
                ns = "default"
                method = key
            if ns not in tree:
                tree[ns] = {}
            tree[ns][method] = {}
            tree[ns][method] = sch

    return tree
