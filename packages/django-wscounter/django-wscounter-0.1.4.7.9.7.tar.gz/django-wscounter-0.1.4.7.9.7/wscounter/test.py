import datetime
from cerberus import Validator

schema = {
    'model': {'type': 'string', 'required': True},
    'from': {'type': 'string', 'dependencies': ['to']},
    'to': {'type': 'string', 'dependencies': ['from']},
    'includeReport': {'type': 'boolean'},
    'nowMinus': {'type': 'integer'},
    'query': {'type': 'list'}
}

validator = Validator(schema)

validator.validate({
    'model': "test",
    'from': '01-2-2017',
    'to':  '01-2-2017',
    'includeReport': True,
    'nowMinus': 1,
    'query': []
}, schema)

print validator.errors
