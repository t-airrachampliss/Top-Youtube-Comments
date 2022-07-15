import unittest
from unittest.mock import patch
from db import get_youtuber, get_all_comments
    
class Test_DB(unittest.TestCase):
    # TODO: Create a mock object for the user's ingredient
    @patch('builtins.input', return='laksnfjsng')
    def test_get_youtuber(self, mock_input):
        with self.assertRaises(True) as ny:
            input_test = get_youtuber

    # TODO: Create a mock database?
    def test_get_all_comments(self):


if __name__ == '__main__':
    unittest.main()