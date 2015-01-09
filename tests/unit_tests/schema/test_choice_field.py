# -*- coding: utf-8 -*-

from unittest.case import TestCase

import pytest

from rip.schema.fields import ChoiceField


class Foo:
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                getattr(other, 'id', None) == self.id)


class TestChoiceField(TestCase):
    def test_validate_for_invalid_choice(self):
        choice_field = ChoiceField(choices=(1, 2))

        result = choice_field.validate(request=None, value=3)

        assert result.is_success is False

    def test_validate_for_valid_choice(self):
        choice_field = ChoiceField(choices=(1, 2))

        result = choice_field.validate(request=None, value=1)

        assert result.is_success is True

    def test_validate_custom_object_in_choices(self):
        choice_field = ChoiceField(choices=(Foo(1), Foo(2)))

        result = choice_field.validate(request=None, value=Foo(1))

        assert result.is_success is True

    def test_validate_custom_object_not_in_choices(self):
        choice_field = ChoiceField(choices=(Foo(1), Foo(2)))

        result = choice_field.validate(request=None, value=Foo("1"))

        assert result.is_success is False

    def test_pass_invalid_choices(self):
        with pytest.raises(TypeError):
            ChoiceField(choices='petromax lighte than venuma')
