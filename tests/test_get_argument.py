import unittest
from gemtoolsconfig.handlers import get_argument
from gemtoolsconfig.exceptions import ArgumentError


class TestGetArgument(unittest.TestCase):
    def test_get_argument(self):
        # Test getting an argument that exists in the dictionary
        kwargs = {'name': 'Alice'}
        self.assertEqual(get_argument(kwargs, 'name'), 'Alice')

        # Test getting an argument with a default value
        kwargs = {'age': 30}
        self.assertEqual(get_argument(kwargs, 'name', default='Bob'), 'Bob')

        # Test getting a required argument that doesn't exist in the dictionary
        kwargs = {'age': 30}
        with self.assertRaises(ArgumentError):
            get_argument(kwargs, 'name')

        # Test getting an argument with choices that is not in the list
        kwargs = {'name': 'Charlie'}
        with self.assertRaises(ArgumentError):
            get_argument(kwargs, 'name', choices=['Alice', 'Bob'])
