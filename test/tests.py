#!/usr/bin/env python3

import unittest
import pandas as pd
from pandas.util.testing import assert_series_equal


from unittest.mock import patch
from datetime import datetime, timedelta
import time
#from location_data_tests import getSiteNums, clean_up_sites, pullinfo, getDateInput
import os

from campsiteFinder import source

class test_UserInputs(unittest.TestCase):

    def test_user_inputs_correct_dates(self):
        user_input = [
            'iAMaString', #string entry
            '1234', #int entry
            '12-August-2018',   #bad format #1
            '12 Aug 2018',      #bad format #2
            '12-08-2018',       #bad format #3
            '08-12-2018',       #bad format #4
            str(datetime.today() - timedelta(days=1)), #edge case day before
            str(datetime.today()),                      #edge case day of
            '2018-03-12',       #date in the past
            str(datetime.today() - timedelta(days=30*4+1)), #far edge of search window
            '2018-08-12', #good start entry
            #rerun test for second input loop

            'iAMaString', #string entry
            '1234', #int entry
            '14-August-2018',   #bad format #1
            '14 Aug 2018',      #bad format #2
            '14-08-2018',       #bad format #3
            '08-14-2018',       #bad format #4
            str(datetime.today() - timedelta(days=1)), #edge case day before
            str(datetime.today()),
            '2018-08-11', #day before search start
            '2018-08-12', #entry same date as search start
            '2018-08-14' #good end entry
        ]
        expected_dates = ('2018-08-12', '2018-08-14')

        with patch('builtins.input', side_effect=user_input):
            stacks = source.getDateInput()
        self.assertEqual(stacks, expected_dates)

    def test_user_inputs_correct_site_numbers(self):
        user_input=[
        'iAMaString',
        '1234',
        '12 34',
        '1 2 3 4 1 2 3 4',
        '1 3 9'
        '1-2-3',
        '1, 2, 6'
        ]

        expected_site_list = [0, 1, 5]

        #incorrect = len(user_input)-1
        #count = 0
        with patch('builtins.input', side_effect=user_input):
            output = source.getSiteNums()
        self.assertEqual(output, expected_site_list)


    def test_user_site_list_are_ints(self):
        user_input = ['1, 3, 4']

        with patch('builtins.input', side_effect=user_input):
            output = source.getSiteNums()
        for s in output:
            self.assertEqual(s, int(s))

    def test_input_email(self):
        user_input = [
        'notaGoodaddress',
        '@gmail.com',
        'mike@',
        'john@.com',
        'john.smith@gmail.com'
        ]

        expected_email = 'john.smith@gmail.com'
        with patch('builtins.input', side_effect=user_input):
            output = source.getEmailaAddress()
        self.assertEqual(output, expected_email)

    def test_yes_response_for_repeater(self):
        user_input = [
        '123',
        'fox',
        'y',
        '5',
        '10'
        ]

        expected_output = (5, 10, True)

        with patch('builtins.input', side_effect=user_input):
            output = source.asktoRepeat()
        self.assertEqual(output, expected_output)

        def test_no_response_for_repeater(self):
            user_input = [
            '123',
            'fox',
            'n'
            ]

            expected_output = (0, 0, False)

            with patch('builtins.input', side_effect=user_input):
                output = source.asktoRepeat()
            self.assertEqual(output, expected_output)

class TestBasicFuncs(unittest.TestCase):

    def setUp(self):
        pass


    def test_clean_up_sites_commas(self):
        self.assertEqual(source.clean_up_sites('1, 3, 4,'), '1 3 4')

    def test_clean_up_sites_extra_spaces(self):
        self.assertEqual(source.clean_up_sites('1  3   4   5  2'), '1 3 4 5 2')

    def test_clean_up_sites_spacesandcommas(self):
        self.assertEqual(source.clean_up_sites('1,  3,   4  5,'), '1 3 4 5')

    def test_int_list(self):
        self.assertEqual(source.intList(['1','2', '3']), [0, 1, 2])

    def test_int_list_finds_duplicate_values(self):
        self.assertEqual(source.intList(['1','2', '2', '2', '4']), [0, 1, 3])

    def test_dates_are_added_to_payload_dict(self):
        self.assertEqual(source.addDates(datetime.strptime('2018-08-12', '%Y-%m-%d'), datetime.strptime('2018-09-01', '%Y-%m-%d')),
            {'arrivalDate': 'Sun Aug 12 2018', 'departureDate': 'Sat Sep 01 2018', 'camping_common_3012': "4"})



class DFTests(unittest.TestCase):

    def setUp(self):
        pass



if __name__ == '__main__':
    unittest.main()
