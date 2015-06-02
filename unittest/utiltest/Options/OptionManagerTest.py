# -*- coding: utf-8 -*-
"""Module Containing Unittests for Optionmanager class"""

import unittest

from util.Options.OptionManager import OptionManager
from util.Options.OptionList import OptionList
from util.Options.Option import Option


class OptionManagerTest(unittest.TestCase):
    """This classe contain unittests for Optionmanager"""
    def setUp(self):
        """Set attributes to test OptionManager's methods.

        option_manager_test is a void OptionManager object.
        option_manager_test1 is an OptionManager filled with test options.
        configuration_file is a a string containing the path to the
        test configuration file.
        """
        self.__option_manager_test = OptionManager()
        self.__configuration_file = 'configuration_file_test'

        general_option_list = OptionList([Option('OUT_PATH', '/home/',
                                                 'General', 'GASBI'),
                                          Option('SEQUENCE_PATH', '/home/',
                                                 'General', 'GASBI'),
                                          Option('TAG', 'test', 'General',
                                                 'GASBI')],
                                         'General')

        basic_glimmer_option_list = OptionList([Option('ICM_MODEL_PATH',
                                                       'default',
                                                       'CDSFindingTool',
                                                       'Glimmer', 'Basic'),
                                                Option('GENE_LEN', '200',
                                                       'CDSFindingTool',
                                                       'Glimmer', 'Basic')],
                                               'Basic')

        expert_glimmer_option_list = OptionList([Option('MAX_OLAP', '50',
                                                        'CDSFindingTool',
                                                        'Glimmer',
                                                        'Expert')],
                                                'Expert')

        glimmer_option_list = OptionList([basic_glimmer_option_list,
                                          expert_glimmer_option_list],
                                         'Glimmer')

        cds_finding_tool_option_list = OptionList([glimmer_option_list],
                                                  'CDSFindingTool')

        all_option_list = OptionList([general_option_list,
                                      cds_finding_tool_option_list],
                                     'all_options')

        self.__option_manager_test2 = OptionManager(all_option_list)

    def test_set_options(self):
        """Test the set_options method."""
        self.__option_manager_test.set_options(self.__configuration_file)
        sequence_path \
            = self.__option_manager_test.get_options()['General/SEQUENCE_PATH']
        self.assertEqual('/home/', sequence_path)

        with self.assertRaises(FileNotFoundError):
            self.__option_manager_test.set_options('not_existant_file')

        with self.assertRaises(IndexError):
            self.__option_manager_test.set_options('corrupted_configuration_' +
                                                   'file_test')

    def test_get_options(self):
        """test the get_options method."""
        general_option_list = OptionList([Option('OUT_PATH', '/home/',
                                                 'General', 'GASBI'),
                                          Option('SEQUENCE_PATH', '/home/',
                                                 'General', 'GASBI'),
                                          Option('TAG', 'test', 'General',
                                                 'GASBI')],
                                         'General')

        basic_glimmer_option_list = OptionList([Option('ICM_MODEL_PATH',
                                                       'default',
                                                       'CDSFindingTool',
                                                       'Glimmer', 'Basic'),
                                                Option('GENE_LEN', '200',
                                                       'CDSFindingTool',
                                                       'Glimmer', 'Basic')],
                                               'Basic')

        expert_glimmer_option_list = OptionList([Option('MAX_OLAP', '50',
                                                        'CDSFindingTool',
                                                        'Glimmer',
                                                        'Expert')],
                                                'Expert')

        glimmer_option_list = OptionList([basic_glimmer_option_list,
                                          expert_glimmer_option_list],
                                         'Glimmer')

        cds_finding_tool_option_list = OptionList([glimmer_option_list],
                                                  'CDSFindingTool')

        all_option_list = OptionList([general_option_list,
                                      cds_finding_tool_option_list],
                                     'all_options')

        self.__option_manager_test2 = OptionManager(all_option_list)
        all_options = self.__option_manager_test2.get_options()

        self.assertEqual(all_options['General/SEQUENCE_PATH'],
                         '/home/')

    def test_check_options(self):
        """test for check_options has not been done yet"""
        pass

if __name__ == '__main__':
    unittest.main()
