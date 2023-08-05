from typing import Iterable

from htmlmarkup.constants import CLASS_ATTRIBUTE_NAME, DATA_ATTRIBUTE_NAME
from htmlmarkup.errors import WrongValidatorCall


class AttributeValidator:

    allowed_types = (str, int, float, bool)

    attribute_name = None

    @classmethod
    def get_rule_result(cls, attribute, value) -> bool:
        if attribute is None or not isinstance(attribute, str):
            return False
        for allowed_type in cls.allowed_types:
            if isinstance(value, allowed_type):
                return True

        return False

    def __call__(self, *args):
        if self.attribute_name is not None and len(args) == 1:
            return self.get_rule_result(self.attribute_name, args[0])
        elif len(args) == 2:
            return self.get_rule_result(args[0], args[1])

        raise WrongValidatorCall


class ClassValidator(AttributeValidator):

    allowed_types = (str, Iterable)
    attribute_name = CLASS_ATTRIBUTE_NAME


class DataAttributeValidator(AttributeValidator):

    attribute_name = DATA_ATTRIBUTE_NAME

    @classmethod
    def get_rule_result(cls, attribute, value) -> bool:

        if isinstance(value, str):
            return True
        if isinstance(value, dict):
            for data_attr, data_value in value.items():
                if not super().get_rule_result(data_attr, data_value):
                    return False
        else:
            return False

        return True
