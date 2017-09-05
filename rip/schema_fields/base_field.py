from abc import ABCMeta

import six

from rip.schema_fields.default_field_value import DEFAULT_FIELD_VALUE
from rip.schema_fields.field_types import FieldTypes
from rip.schema_fields.validation_result import ValidationResult


class BaseField(six.with_metaclass(ABCMeta)):
    # can be a data type like unicode / int or a tuple of data types
    data_type = None

    def __init__(self, required=False,
                 field_type=FieldTypes.DEFAULT,
                 nullable=True,
                 entity_attribute=None,
                 show_in_list=True):
        self.entity_attribute = entity_attribute
        self.nullable = nullable
        self.required = required
        self.field_type = field_type
        self.show_in_list = show_in_list

        assert self.data_type is not None

    def _get_valid_data_types(self):
        """
        If the data_type is already a list of classes return.
        Else convert to a list and return
        """
        if isinstance(self.data_type, (list, tuple, set)):
            return self.data_type
        else:
            return self.data_type, # comma makes the return a tuple

    def get_message_for_type_error(self):
        return "Expected type {}.".format(
                    str([d.__name__ for d in self._get_valid_data_types()]))

    def validate(self, request, value):
        """
        This is not for business validation
        This should be only used for type validation
        Hence the only input is the value of the field
        :param value:
        :return:
        """
        if self.required and value == DEFAULT_FIELD_VALUE:
            return ValidationResult(is_success=False,
                                    reason='This field is required')
        if not self.nullable and value is None:
            return ValidationResult(is_success=False,
                                    reason='null is not a valid value')
        if not self.required and value == DEFAULT_FIELD_VALUE:
            return ValidationResult(is_success=True)
        if self.nullable and value is None:
            return ValidationResult(is_success=True)

        valid_data_types = self._get_valid_data_types()
        data_valid = False

        for data_type in valid_data_types:
            try:
                if data_type in [int, float, unicode, basestring]:
                    data_type(value)
                    data_valid = True
                else:
                    data_valid = isinstance(value, data_type)
                break
            except (ValueError, TypeError):
                continue
        if not data_valid:
            return ValidationResult(
                is_success=False,
                reason=self.get_message_for_type_error())

        return ValidationResult(is_success=True)

    def serialize(self, request, value):
        return value

    def clean(self, request, value):
        """
        Called during update and create
        If there are deeper nesting within a field,
        which may have readonly fields, this function
        will be overridden
        :param request:
        :param value:
        :return:
        """
        if isinstance(value, self._get_valid_data_types()) or\
                value in [DEFAULT_FIELD_VALUE, None]:
            return value
        else:
            try:
                ret = [typ(value) for typ in self._get_valid_data_types()]
            except (ValueError, TypeError):
                pass
            return ret[0]


class DictionaryField(BaseField):
    data_type = dict
