import unittest

from htmlmarkup.errors import WrongValidatorCall
from htmlmarkup.validators import AttributeValidator, ClassValidator, \
    DataAttributeValidator


class ValidatorsTestCase(unittest.TestCase):

    def setUp(self):
        self.validator = AttributeValidator()
        self.class_validator = ClassValidator()
        self.data_validator = DataAttributeValidator()

    def test_attribute_validator(self):
        self.assertTrue(self.validator('name', 'test-name'))
        self.assertTrue(self.validator('name', 123))
        self.assertTrue(self.validator('name', True))
        self.assertTrue(self.validator('name', 3.5))

    def test_attribute_validator_wrong(self):
        self.assertFalse(self.validator('name', [123]))
        self.assertFalse(self.validator('name', (123,)))
        self.assertFalse(self.validator('name', {'key': 'value'}))

    def test_class_validator(self):
        self.assertTrue(self.class_validator(['col-md-12', 'hidden']))
        self.assertTrue(self.class_validator(('col-md-12', 'hidden')))
        self.assertTrue(self.class_validator({'col-md-12', 'hidden'}))
        self.assertTrue(self.class_validator('col-md-12 hidden'))

    def test_class_validator_wrong(self):
        self.assertFalse(self.class_validator(1232))
        self.assertFalse(self.class_validator(3.6))

    def test_data_validator(self):
        self.assertTrue(self.data_validator('test data'))
        self.assertTrue(self.data_validator({'name': 'name', 'value': 123}))

    def test_data_validator_wrong(self):
        self.assertFalse(self.data_validator({
            'value': []
        }))
        self.assertFalse(self.data_validator({
            'value': {}
        }))
        self.assertFalse(self.data_validator({
            'value': ()
        }))

    def test_exception(self):
        with self.assertRaises(WrongValidatorCall):
            self.validator(123, 1232, 3444)

