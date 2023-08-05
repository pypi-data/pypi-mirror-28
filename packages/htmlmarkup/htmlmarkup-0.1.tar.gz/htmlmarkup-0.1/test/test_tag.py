import unittest

from htmlmarkup.errors import WrongContentType
from htmlmarkup.tags.base import Tag


class TagTestCase(unittest.TestCase):
    def setUp(self):
        self.single_pattern = '<input name="test_single" type="text" id="1">'
        self.closeable_pattern = '<div id="2" class="test_class bordered">text_in_div</div>'
        self.parentless_pattern = '<form name="test-form"><input type="text" value="123"></form>'
        self.list_pattern = '<form name="test-form"><input><textarea></textarea>test text</form>'
        self.class_attribute_test = '<div class="col-md-12 bordered hidden">text</div>'
        self.data_attribute_test = '<div data-text="text" data-value="123" data-hidden="True">text</div>'
        self.nested_test = '<div><p>text</p><p>text1</p><p>text2</p></div>'

    def test_single(self):
        single_tag = Tag('input', attributes={
            'name': 'test_single',
            'type': 'text',
            'id': 1
        })

        self.assertIs(single_tag.single, True)
        self.assertEqual(single_tag.to_string(), self.single_pattern)

    def test_wrong_content(self):
        with self.assertRaises(WrongContentType):
            tag = Tag('div', {})
            tag.to_string()

    def test_closeable(self):
        closeable = Tag('div', 'text_in_div', {
            'id': 2,
            'class': 'test_class bordered',
        })

        self.assertIs(closeable.single, False)
        self.assertEqual(closeable.to_string(), self.closeable_pattern)

    def test_parentless(self):
        child = Tag('input', attributes={
            'type': 'text',
            'value': 123,
        })
        parent = Tag('form', child, {
            'name': 'test-form',
        })

        self.assertEqual(parent.to_string(), self.parentless_pattern)

    def test_list_content(self):
        parent = Tag('form', [
                Tag('input'),
                Tag('textarea'),
                'test text'
            ],
            {'name': 'test-form'}
        )

        self.assertEqual(parent.to_string(), self.list_pattern)

    def test_class_list(self):
        div = Tag('div', 'text', {
            'class': [
                'col-md-12',
                'bordered',
                'hidden'
            ]
        })

        self.assertEqual(div.to_string(), self.class_attribute_test)

    def test_data_attribute(self):
        div = Tag('div', 'text', {
            'data': {
                'text': 'text',
                'value': 123,
                'hidden': True
            }
        })

        self.assertEqual(div.to_string(), self.data_attribute_test)

    def test_nested_tag(self):
        div = Tag('div', [
            Tag('p', 'text'),
            [
                Tag('p', 'text1'),
                Tag('p', 'text2'),
            ]
        ],)

        self.assertEqual(div.to_string(), self.nested_test)