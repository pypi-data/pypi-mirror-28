import json

import sqlalchemy.types as types


class StringyJSON(types.TypeDecorator):
    """Stores and retrieves JSON as TEXT."""

    impl = types.TEXT

    def process_literal_param(self, value, dialect):
        pass

    def python_type(self):
        pass

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


# TypeEngine.with_variant says "use StringyJSON instead when
# connecting to 'sqlite'"
# Do that because unittest will use in-memory SQLite instead of PGSQL
JSON_TYPE = types.JSON().with_variant(StringyJSON, 'sqlite')
