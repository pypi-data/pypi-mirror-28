from typing import Union, Type

from htmlmarkup.mixins.generators import TagGenerator


class Tag(TagGenerator):

    def __init__(self, tag_name: str, content=None,
                 attributes: Union[None, dict] = None):
        self.name = tag_name
        self.content = content
        self.attributes = attributes

    @property
    def single(self):
        return super().is_single(self.name)

    def to_string(self):
        return super().to_html(
            self.name,
            self.content,
            self.attributes
        )

    def __str__(self):
        return self.to_string()

    @classmethod
    def _transform_content(cls, content: Union[str, list, Type['Tag']]) -> str:
        if isinstance(content, Tag):
            return content.to_string()

        return super()._transform_content(content)



