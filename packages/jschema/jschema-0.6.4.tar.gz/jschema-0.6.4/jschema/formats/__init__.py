from .format_ajv import format_ajv
from .format_golang import format_golang
from .format_js import format_js
from .format_json import format_json

formats = {
    "ajv": format_ajv,
    "golang": format_golang,
    "js": format_js,
    "json": format_json
}
