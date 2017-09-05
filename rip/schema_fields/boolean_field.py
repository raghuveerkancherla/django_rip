from rip.schema_fields.base_field import \
    BaseField
from rip.schema_fields.default_field_value import \
    DEFAULT_FIELD_VALUE
from rip.schema_fields.validation_result import \
    ValidationResult


class BooleanField(BaseField):
    data_type = bool
