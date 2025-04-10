import unittest
from src.utils import StringUtils, ListUtils


class TestStringUtils(unittest.TestCase):
    def setUp(self):
        self.string_utils = StringUtils()

    def test_reverse_string(self):
        self.assertEqual(self.string_utils.reverse_string("hello"), "olleh")
        self.assertEqual(self.string_utils.reverse_string(""), "")
        self.assertEqual(self.string_utils.reverse_string("a"), "a")

    def test_count_vowels(self):
        self.assertEqual(self.string_utils.count_vowels("hello"), 2)
        self.assertEqual(self.string_utils.count_vowels("AEIOU"), 5)
        self.assertEqual(self.string_utils.count_vowels("xyz"), 0)

    def test_is_palindrome(self):
        self.assertEqual(self.string_utils.is_palindrome("bob"),True)
        self.assertEqual(self.string_utils.is_palindrome("Bob"),True)
        self.assertEqual(self.string_utils.is_palindrome("dog"),False)

    def test_to_uppercase(self):
        self.assertEqual(self.string_utils.to_uppercase("hello"),"HELLO")
        self.assertEqual(self.string_utils.to_uppercase("hELLo"),"HELLO")

    def test_to_lowercase(self):
        self.assertEqual(self.string_utils.to_lowercase("HELLO"),"hello")
        self.assertEqual(self.string_utils.to_lowercase("hELLo"),"hello")

class TestListUtils(unittest.TestCase):
    def setUp(self):
        self.list_utils = ListUtils()

    def test_find_max(self):
        self.assertEqual(self.list_utils.find_max([1, 2, 3, 4, 5]), 5)
        self.assertEqual(self.list_utils.find_max([-5, -2, -10]), -2)
        self.assertIsNone(self.list_utils.find_max([]))

    def test_find_min(self):
        self.assertEqual(self.list_utils.find_min([1, 2, 3, 4, 5]), 1)
        self.assertEqual(self.list_utils.find_min([-5, -2, -10]), -10)
        self.assertIsNone(self.list_utils.find_min([]))

    def test_calculate_average(self):
        self.assertEqual(self.list_utils.calculate_average([]),None)
        self.assertEqual(self.list_utils.calculate_average([4,3,2]),3)
        self.assertEqual(self.list_utils.calculate_average([5,4,3,2,1]),3)

    def test_remove_duplicates(self):
        self.assertEqual(self.list_utils.remove_duplicates([1,2,2,3,3,3]),[1,2,3])
        self.assertEqual(self.list_utils.remove_duplicates([0,0,0,0,0]),[0])

    def test_sort_ascending(self):
        self.assertEqual(self.list_utils.sort_ascending([3,1,7,4,5]),[1,3,4,5,7])
        self.assertEqual(self.list_utils.sort_ascending([-2,0,-8,5,-6]),[-8,-6,-2,0,5])
        self.assertEqual(self.list_utils.sort_ascending([]),[])

    def test_sort_descending(self):
        self.assertEqual(self.list_utils.sort_descending([3,1,7,4,5]),[7,5,4,3,1])
        self.assertEqual(self.list_utils.sort_descending([-2,0,-8,5,-6]),[5,0,-2,-6,-8])
        self.assertEqual(self.list_utils.sort_descending([]),[])