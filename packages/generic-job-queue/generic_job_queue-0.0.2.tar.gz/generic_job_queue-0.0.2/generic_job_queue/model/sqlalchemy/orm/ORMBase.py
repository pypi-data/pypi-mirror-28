from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime

class _BaseMixin:
    @declared_attr
    def __tablename__(cls):
        class_name = cls.__name__
        # Below will convert CamelCase to snake_case
        snake_cased_class_name = ''
        for index, char in enumerate(class_name):
            has_previous_char = index > 0
            is_upper_case = char == char.upper()
            should_append_underscore = is_upper_case and has_previous_char
            if should_append_underscore:
                snake_cased_class_name += "_{}".format(char.lower())
            else:
                snake_cased_class_name += char.lower()
        return snake_cased_class_name

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

Base = declarative_base(cls=_BaseMixin)
