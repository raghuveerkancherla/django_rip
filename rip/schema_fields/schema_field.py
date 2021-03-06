from rip.crud.resource_schema_mixin import ResourceSchemaMixin
from rip.generic_steps.default_data_cleaner import \
    DefaultRequestCleaner
from rip.generic_steps.default_schema_serializer import \
    DefaultEntitySerializer
from rip.generic_steps.default_schema_validation import \
    DefaultSchemaValidation
from rip.schema_fields.base_field import BaseField
from rip.schema_fields.field_types import FieldTypes
from rip.schema_fields.default_field_value import \
    DEFAULT_FIELD_VALUE
from rip.schema_fields.validation_result import \
    ValidationResult


class SchemaField(BaseField):
    data_type = (dict,)
    """
    Use the schema of a Resource to represent (serialize / clean / validated)
    """
    def __init__(self, of_type,
                 required=False,
                 field_type=FieldTypes.DEFAULT,
                 nullable=True,
                 entity_attribute=None,
                 validator_cls=DefaultSchemaValidation,
                 serializer_cls=DefaultEntitySerializer,
                 cleaner_cls=DefaultRequestCleaner,
                 show_in_list=True):
        super(SchemaField, self).__init__(required=required,
                                          field_type=field_type,
                                          nullable=nullable,
                                          entity_attribute=entity_attribute,
                                          show_in_list=show_in_list)
        self.of_type = of_type
        resource = self.of_type()
        self.validator = validator_cls(resource=resource)
        self.serializer = serializer_cls(resource=resource)
        self.cleaner = cleaner_cls(resource=resource)

    def validate(self, request, value):
        validation_result = super(SchemaField, self).validate(request, value)

        if not validation_result.is_success:
            return validation_result

        if value == DEFAULT_FIELD_VALUE:
            return ValidationResult(is_success=True)
        if value is None and self.nullable:
            return ValidationResult(is_success=True)

        errors = self.validator.validate_data(request, value)
        if errors:
            return ValidationResult(is_success=False, reason=errors)

        return ValidationResult(is_success=True)

    def serialize(self, request, value):
        if value is None:
            return None
        return self.serializer.serialize_entity(request, value)

    def clean(self, request, value):
        if value is None:
            return None
        return self.cleaner.clean(request, value)
