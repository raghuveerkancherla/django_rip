# -*- coding: utf-8 -*-

from rip.schema.base_field import BaseField, FieldTypes
from rip.schema.validation_result import ValidationResult


class ChoiceField(BaseField):
    """Restrict the value which is received.
    """
    def __init__(self, choices, entity_attribute=None, required=False,
                 field_type=FieldTypes.DEFAULT):
        """Pass list of allowed values.

        :param choices: `list` or `tuple` or `set` of values.
        """
        super(ChoiceField, self).__init__(
            required=required, field_type=field_type,
            entity_attribute=entity_attribute)

        self._validate_choices_type(choices)
        self.choices = choices

    def _validate_choices_type(self, choices):
        allowed_types = (list, tuple, set, )
        # Prohibit user from giving any data type in choices attribute
        msg = u"choices: {} should of any one of the type {}".format(
            choices, allowed_types)
        if not isinstance(choices, allowed_types):
            raise TypeError(msg)

    def validate(self, request, value):
        validation_result = super(ChoiceField, self).validate(request, value)

        if not validation_result.is_success:
            return validation_result

        if value in self.choices:
            return ValidationResult(is_success=True)
        return ValidationResult(
            is_success=False, reason=u"{} isn't valid choice".format(value))
