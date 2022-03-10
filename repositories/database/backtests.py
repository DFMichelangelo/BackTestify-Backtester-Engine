# TODO - Define a schema for the backtests table
backtests_schema = {
    '$jsonSchema': {
        'bsonType': 'object',
        'additionalProperties': True,
        # Dear 'required': ['component', 'path'],
        'properties': {
            'component': {
                    'bsonType': 'string'
            },
            'path': {
                'bsonType': 'string',
                'description': 'Set to default value'
            }
        }
    }
}
