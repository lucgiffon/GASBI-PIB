# -*- coding: utf-8 -*-
"""Module Containing Unittests for Option class."""

import unittest
from util.Options.Option import Option


class OptionTest(unittest.TestCase):
    """This classe contain unittests for Option."""
    def setUp(self):
        """Set attributes to test Option's methods.

        optiontest is an Option object.
        """
        name = 'option_name'
        value = 'option_value'
        group = 'option_group'
        tool = 'option_tool'
        subgroup = 'option_subgroup'
        self.__optiontest = Option(name, value, group, tool, subgroup)

    def test_get_name(self):
        """Test get_name method."""
        self.assertEqual(self.__optiontest.get_name(), 'option_name')

    def test_get_value(self):
        """Test get_value method."""
        self.assertEqual(self.__optiontest.get_value(), 'option_value')

    def test_set_value(self, new_value='option_value2'):
        """Test set_value method."""
        self.__optiontest.set_value(new_value)
        self.assertEqual(self.__optiontest.get_value(), 'option_value2')

    def test_get_tool(self):
        """Test get_tool method."""
        self.assertEqual(self.__optiontest.get_tool(), 'option_tool')

    def test_get_group(self):
        """Test get_group method."""
        self.assertEqual(self.__optiontest.get_group(), 'option_group')

    def test___repr__(self):
        """Test __repr__ method."""
        message = str(self.__optiontest)
        message_test = ("Name: option_name\t" +
                        "Value: option_value\t" +
                        "Group: option_group\t" +
                        "Tool: option_tool\t" +
                        "SubGroup: option_subgroup")
        self.assertEqual(message, message_test)

if __name__ == '__main__':
    unittest.main()
