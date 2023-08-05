from typing import Union, Any, Dict, Iterable

from htmlmarkup.constants import CLASS_ATTRIBUTE_NAME, DATA_ATTRIBUTE_NAME
from htmlmarkup.validators import AttributeValidator, ClassValidator, \
    DataAttributeValidator
from ..constants import SINGLE_TAGS
from ..errors import WrongContentType


class Generator:
    @classmethod
    def _transform_content(cls, content: Union[str, list]) -> str:
        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            for index, item in enumerate(content):
                content[index] = cls._transform_content(item)

            return ''.join(content)
        elif content is None:
            return ''
        else:
            raise WrongContentType

    @classmethod
    def to_html(cls, tag_name: str, content: Any,
                attributes: Dict[str, Union[str, dict]]) -> str:
        raise NotImplementedError


class AttributesGenerator:
    attribute_template = '{attribute}="{value}"'

    @classmethod
    def convert_to_string(cls, attributes_dict: Dict[
            str, Union[str, list, dict]]):
        for attribute, value in cls._get_normalized_attributes(attributes_dict):
            yield cls.convert_attribute_string(attribute, value)

    @classmethod
    def convert_attribute_string(cls, attribute: str,
                                 value: Union[str, list, dict]) -> str:
        return cls.attribute_template.format(
            attribute=attribute,
            value=str(value)
        )

    @classmethod
    def _get_normalized_attributes(cls, attributes: Dict[
            str, Union[str, list, dict]]):
        validator = AttributeValidator()
        class_validator = ClassValidator()
        data_attr_validator = DataAttributeValidator()

        for attribute, value in attributes.items():
            if attribute is None or value is None:
                continue

            if attribute == CLASS_ATTRIBUTE_NAME and class_validator(value):
                value = cls._transform_class_attribute(value)

                if len(value) == 0:
                    continue

                yield attribute, value
            elif attribute == DATA_ATTRIBUTE_NAME and data_attr_validator(
                    value):
                for data_name, data_value in cls._get_data_attributes(
                        attributes[DATA_ATTRIBUTE_NAME]):
                    yield data_name, data_value
            elif validator(attribute, value):
                yield attribute, value
            else:
                continue

    @staticmethod
    def _get_data_attributes(data_dict: Dict[str, str]):
        for name, value in data_dict.items():
            yield 'data-' + name, value

    @staticmethod
    def _transform_class_attribute(classes: Union[str, list]) -> str:
        if isinstance(classes, Iterable) and not isinstance(classes, str):
            return ' '.join(classes)

        return classes


class TagGenerator(AttributesGenerator, Generator):
    single_tag_template = '<{tag_name}{attributes}>'
    closable_tag_template = '<{tag_name}{attributes}>{content}</{tag_name}>'

    @classmethod
    def to_html(cls, tag_name: str, content: Any,
                attributes: Dict[str, Union[str, dict]]) -> str:
        template = cls.closable_tag_template
        content = cls._transform_content(content)

        if TagGenerator.is_single(tag_name):
            template = cls.single_tag_template
            content = ''

        return template.format(
            tag_name=tag_name,
            content=content,
            attributes=cls._transform_attributes(attributes)
        )

    @staticmethod
    def is_single(tag_name: str) -> bool:
        return tag_name in SINGLE_TAGS

    @classmethod
    def _transform_attributes(cls,
                              attributes_dict: Union[None, dict] = None) -> str:
        if attributes_dict is None:
            return ''

        attributes = [x for x in cls.convert_to_string(attributes_dict)]
        attributes.insert(0, '')

        return ' '.join(attributes)
