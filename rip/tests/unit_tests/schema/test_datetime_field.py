import unittest

from rip.request import Request
from rip.schema_fields.datetime_field import DateTimeField


class TestValidateDatetimeField(unittest.TestCase):
    def test_return_success_if_nullable_and_value_is_none(self):
        field = DateTimeField(nullable=True)

        result = field.validate(request=None, value=None)

        assert result.is_success

    def test_return_failure_if_not_nullable_and_value_is_none(self):
        field = DateTimeField(nullable=False)

        result = field.validate(request=None, value=None)

        assert not result.is_success

    def test_success_if_value_is_timestamp(self):
        field = DateTimeField()

        request = Request(user=None, request_params=None,
                          context_params={
                              'protocol': 'http',
                              'timezone': 'UTC',
                            })
        result = field.validate(request=request, value=1234567222)

        assert result.is_success

    def test_fails_on_invalid_date(self):

        field = DateTimeField()

        result = field.validate(request=None, value='13123adasdf')

        assert not result.is_success


class TestCleanDatetimeField(unittest.TestCase):
    def test_fails_on_invalid_date(self):

        field = DateTimeField()

        result = field.validate(request=None, value='13123adasdf')

        assert not result.is_success
        assert result.reason == 'Expected a unicode timestamp.'
