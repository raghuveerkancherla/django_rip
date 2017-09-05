from rip import datetime_converter
from rip.schema_fields.base_field import \
    BaseField


class DateTimeField(BaseField):
    data_type = int

    def get_message_for_type_error(self):
        return "Expected a unicode timestamp."

    def serialize(self, request, value):
        if value is None:
            return value
        timezone = request.context_params['timezone']
        return datetime_converter.datetime_to_timestamp(
            value, timezone=timezone)

    def clean(self, request, value):
        if value is None:
            return value
        timezone = request.context_params['timezone']
        return datetime_converter.timestamp_to_datetime(float(value), timezone)
