import os
import argparse

from .schema import Schema

def parseArguments():
    parser = argparse.ArgumentParser(prog="jschema")

    parser.add_argument("--src", help="Source directory with schemas (default: %(default)s)", default=str(os.path.abspath(os.getcwd())))
    parser.add_argument("--dst", help="Destination directory for compiled schemas, destination path for js format", required=True)
    parser.add_argument("--fmt", choices=["ajv", "js", "json", "golang"],  help="Schema output format", required=True)
    parser.add_argument("--ns", help="namespace name (default: %(default)s1)", default=None)

    return parser.parse_args()

def main():
    args = parseArguments()
    schema = Schema()

    schema.load(args.src)
    schema.resolve_refs()
    if args.fmt not in ["docs"]:
        schema.clear()

    schema.format(args.fmt, {"dst": args.dst, "ns": args.ns})
