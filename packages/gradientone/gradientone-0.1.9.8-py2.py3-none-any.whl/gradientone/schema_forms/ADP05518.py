from common_elements import FORM_BOTTOM
from gradientone.device_drivers.can.can_helpers import get_trace_variables, properties_from_cfg
from gradientone.device_drivers.can.can_headers import registers

PROPERTIES = properties_from_cfg()
# pull out only the values that can be Mapped to a PDO
PDO_MAPPABLE = [key for key in PROPERTIES.keys() if PROPERTIES[key]["pdo"]
                and PROPERTIES[key]["plot"]]
TRACE_VARIABLES = sorted(get_trace_variables())

PROPERTIES_LIST = [{"value": key, "name": key.replace("_", " ").capitalize(),
                    "category": "poll"} for key in sorted(PDO_MAPPABLE)] + \
                  [{"value": key,
                    "name": key.replace("_", " ").replace(":", ": ").capitalize(),
                    "category": "trace"} for key in TRACE_VARIABLES]

REGISTERS_LIST = [{"value": key, "name": key.replace("_", " ").capitalize(),
              "category": "register"} for key in registers]

SCHEMA_DICT = {
    "type": "object",
    "title": "Config",
    "properties": {
        "name": {
            "title": "Config Name",
            "type": "string"
        },
        "node_id": {
            "title": "Node ID",
            "type": "string",
            "description": "Note: hardware must be physically set to this node id"
        },
        "relative_move": {
            "title": "Relative Move",
            "type": "boolean"
        },
        "motor_end_position": {
            "title": "Destination (steps)",
            "type": "number",
            "minimum": 0,
            "maximum": 65536
        },
        "trace_period": {
            "title": "Trace Period",
            "type": "number",
            "minimum": 1,
            "maximum": 0xffff
        },
        "timeout": {
            "title": "Command Timeout (s)",
            "type": "number",
            "minimum": 0,
            "maximum": 10
        },
        "comment": {
            "title": "Comment",
            "type": "string",
            "maxLength": 200,
            "validationMessage": "Exceeds character limit!"
        },
        "properties": {
            "title": "Properties",
            "type": "array",
            "items": {"type": "string"},
            "htmlClass": "propertySelect",
            "maxItems": 6,
            "description": "Please select no more than 6 properties."
        },
    },
    "required": [
        "name",
        "node_id",
        "motor_end_position",
        "time_window",
        "trace",
        "properties"
    ]
}

FORM_DICT = [
    {
        "key": "name",
        "placeholder": "Copley"
    },
    {
        "key": "node_id",
        "default": 1
    },
    {
        "key": "relative_move",
        "default": True
    },
    {
        "key": "motor_end_position",
        "default": 5000
    },
    {
        "key": "trace_period",
        "default": 110
    },
    {
        "key": "timeout",
        "default": 10
    },
    {
        "key": "properties",
        "type": "strapselect",
        "placeholder": "Please select a property.",
        "options": {
            "multiple": "true",
            "filter": "item.category.indexOf('trace') > -1"
        },
        "validationMessage": "Please select a min of 1 and max of 6 properties!",
        "titleMap": PROPERTIES_LIST
    },
] + FORM_BOTTOM

