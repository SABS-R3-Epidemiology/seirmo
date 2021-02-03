#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import unittest
import seirmo as se


class TestDatasetLibraryAPIClass(unittest.TestCase):
    """
    Test the 'DatasetLibraryAPI' class.
    """
    def test__init__(self):
        se.DatasetLibrary()

    def test_french_flu(self):
        dataframe = se.DatasetLibrary().french_flu()
        column_keys = dataframe.head()
        expect_keys = [
            'time_index', 'year', 'week', 'day', 'inc', 'inc_low',
            'inc_up', 'inc100', 'inc100_low', 'inc100_up']
        self.assertTrue(set(column_keys) == set(expect_keys))


if __name__ == '__main__':
    unittest.main()
