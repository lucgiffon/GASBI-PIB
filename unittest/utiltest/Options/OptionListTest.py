# -*- coding: utf-8 -*-
"""Module Containing Unittests for OptionList class."""

from _collections_abc import Iterable

import unittest

from util.Options.Option import Option
from util.Options.OptionList import OptionList
from util.Exceptions.ErrorOptionMissing import ErrorOptionMissing


class OptionListTest(unittest.TestCase):
    """This classe contain unittests for OptionList."""
    def setUp(self):
        """Set attributes to test OptionList's methods.

        optionlist1 is an OptionList object.
        optionlist2 is an OptionList Object.
        optionlistest is an OptionList which contain OptionList objects.
        """
        option1 = Option('option_name1',
                         'option_value1',
                         'option_group',
                         'option_tool',
                         'option_subgroup1')

        option2 = Option('option_name2',
                         'option_value2',
                         'option_group',
                         'option_tool',
                         'option_subgroup1')

        option3 = Option('option_name3',
                         'option_value3',
                         'option_group',
                         'option_tool',
                         'option_subgroup2')

        option4 = Option('option_name4',
                         'option_value4',
                         'option_group',
                         'option_tool',
                         'option_subgroup2')

        self.__optionlist1 = OptionList([option1, option2], 'option_subgroup1')
        self.__optionlist2 = OptionList([option3, option4], 'option_subgroup2')
        self.__optionlisttest = OptionList([self.__optionlist1,
                                            self.__optionlist2], 'test')

    def test___getitem__(self):
        """Test the __getitem__ special method."""
        test_value = 'option_value1'
        self.assertEqual(test_value,
                         self.__optionlisttest['option_subgroup1/' +
                                               'option_name1'])
        self.assertIs(self.__optionlist1,
                      self.__optionlisttest['option_subgroup1'])

        with self.assertRaises(ErrorOptionMissing):
            self.__optionlisttest['option_subgroup3']

    def test___setitem__(self):
        """Test the __setitem__ special method."""
        test_value = 'option_value3'
        self.__optionlisttest['option_subgroup1/option_name1'] = test_value
        self.assertEqual(test_value,
                         self.__optionlisttest['option_subgroup1/' +
                                               'option_name1'])
        with self.assertRaises(ErrorOptionMissing):
            self.__optionlisttest['option_subgroup1/option_name3']

    def test_append(self):
        """Test the append method."""
        test_option = Option('option_name4',
                             'option_value4',
                             'option_group',
                             'option_tool',
                             'option_subgroup')
        self.__optionlisttest.append(test_option)
        self.assertIn(test_option, self.__optionlisttest)

    def test___iter__(self):
        """Test the __iter__ method."""
        self.assertIsInstance(self.__optionlisttest, Iterable)

    def test___repr__(self):
        """Test the __repr__ method."""
        message = ("[[Name: option_name1\tValue: option_value1\t" +
                   "Group: option_group\tTool: option_tool\t" +
                   "SubGroup: option_subgroup1, Name: option_name2\t" +
                   "Value: option_value2\tGroup: option_group\t" +
                   "Tool: option_tool\tSubGroup: option_subgroup1], " +
                   "[Name: option_name3\tValue: option_value3\t" +
                   "Group: option_group\tTool: option_tool\t" +
                   "SubGroup: option_subgroup2, Name: option_name4\t" +
                   "Value: option_value4\tGroup: option_group\t" +
                   "Tool: option_tool\tSubGroup: option_subgroup2]]")
        self.assertEqual(str(self.__optionlisttest), message)

if __name__ == '__main__':
    unittest.main()
