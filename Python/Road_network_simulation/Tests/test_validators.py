import unittest
from modules.validators import Validators

class Test_validate_integer(unittest.TestCase):
    def test_valid_integer(self):
        "Tests a valid integer, expects no error"
        result = Validators.validate_integer(42)
        self.assertEqual(result, 42)

    def test_invalid_integer(self):
        "Tests an invalid integer, expects ValueError"
        with self.assertRaises(ValueError):
            Validators.validate_integer("abc")

    def test_valid_string_integer(self):
        "Tests a valid string integer, expects no error"
        result = Validators.validate_integer("42")
        self.assertEqual(result, 42)

    def test_integer_out_of_bounds(self):
        "Tests an integer out of bounds, expects ValueError"
        with self.assertRaises(ValueError):
            Validators.validate_integer("101", lower_bound=0, upper_bound=100)

    def test_integer_in_bounds(self):
        "Tests an integer in bounds, expects no error"
        result = Validators.validate_integer("42", lower_bound=0, upper_bound=100)
        self.assertEqual(result, 42)

    def test_only_one_bound(self):
        "Tests only one bound, expects no error"
        result = Validators.validate_integer(0, lower_bound=0)
        self.assertEqual(result, 0)

    def test_string_bound(self):
        "Tests a string bound, expects ValueError"
        with self.assertRaises(TypeError):
            Validators.validate_integer("0", lower_bound="noodles", upper_bound=0)
    
    def test_upper_bound(self):
        "Tests an upper bound, expects no error"
        result = Validators.validate_integer("100", upper_bound=100)
        self.assertEqual(result, 100)

class Test_validate_float(unittest.TestCase):
    
    def test_valid_integer(self):
        "Tests a valid float, expects no error"
        result = Validators.validate_float(5.7)
        self.assertEqual(result, 5.7)

    def test_invalid_integer(self):
        "Tests an invalid str, expects ValueError"
        with self.assertRaises(ValueError):
            Validators.validate_float("abc")

    def test_valid_string_integer(self):
        "Tests a valid string float, expects no error"
        result = Validators.validate_float("42.5")
        self.assertEqual(result, 42.5)

    def test_integer_out_of_bounds(self):
        "Tests an integer out of bounds, expects ValueError"
        with self.assertRaises(ValueError):
            Validators.validate_float("101.23", lower_bound=0, upper_bound=100.24)

    def test_integer_in_bounds(self):
        "Tests an integer in bounds, expects no error"
        result = Validators.validate_float("42.45", lower_bound=0, upper_bound=100)
        self.assertEqual(result, 42.45)

    def test_only_one_bound(self):
        "Tests only one bound, expects no error"
        result = Validators.validate_float(0, lower_bound=0)
        self.assertEqual(result, 0)

    def test_string_bound(self):
        "Tests a string bound, expects ValueError"
        with self.assertRaises(TypeError):
            Validators.validate_float("0", lower_bound="noodles", upper_bound=0)
    
    def test_upper_bound(self):
        "Tests an upper bound, expects no error"
        result = Validators.validate_float("100", upper_bound=100)
        self.assertEqual(result, 100)

class Test_is_in_options(unittest.TestCase):
    def test_valid_option(self):
        "Tests a valid option, expects no error"
        result =Validators.validate_options("R", ["R", "L", "S"])
        self.assertEqual(result, "R")

    def test_invalid_option(self):
        "Tests an invalid option, expects ValueError"
        with self.assertRaises(ValueError):
           Validators.validate_options("R", ["L", "S"])

    def test_valid_option_with_lower(self):
        "Tests a valid option with lowercase, expects no error"
        result =Validators.validate_options("r", ["r", "L", "S"])
        self.assertEqual(result, "r")

    def test_valid_option_with_mixed_case(self):
        "Tests a valid option with mixed case, expects error"
        with self.assertRaises(ValueError):
            result =Validators.validate_options("r", ["R", "L", "S"])

    def test_invalid_option_with_mixed_case(self):
        "Tests an invalid option with mixed case, expects ValueError"
        with self.assertRaises(ValueError):
           Validators.validate_options("r", ["L", "S"])
            
    def test_invalid_option_list(self):
        "Tests an invalid option list, expects TypeError"
        with self.assertRaises(TypeError):
           Validators.validate_options("5", "5")
    
    def test_invalid_option_list(self):
        "Tests an invalid option list, expects ValueError"
        with self.assertRaises(ValueError):
           Validators.validate_options("5", [5, 6, 7])

class Test_is_valid_path(unittest.TestCase):
    def test_valid_path(self):
        "Tests a valid path, expects no error"
        result = Validators.validate_path(r"Tests\test_validators.py")
        self.assertEqual(result, r"Tests\test_validators.py")

    def test_invalid_path(self):
        "Tests an invalid path, expects ValueError"
        with self.assertRaises(ValueError):
            Validators.validate_path("C:/Users/username/Documents/noodles/doodles/woodles/")
            
    def test_case_insensitive_path(self):
        "Tests a case insensitive path, expects no error"
        result = Validators.validate_path(r"Tests\test_validators.py")
        self.assertEqual(result, r"Tests\test_validators.py")

    def test_empty_path(self):
        "Tests an empty path, expects ValueError"
        with self.assertRaises(ValueError):
            Validators.validate_path("")

class Test_extract_file_data_general(unittest.TestCase):
    def test_emptyfile(self):
        """Test empty file, expects empty list."""
        result =Validators.extract_file_data(r'Tests/regex_tests\emptyfile.txt')
        self.assertEqual(result, [])
    
    def test_emptylines_segs(self):
        """Test empty lines in file, expects them to be filtered away."""
        result =Validators.extract_file_data(r'Tests/regex_tests\emptylines_segs.txt')
        self.assertEqual(result, [((1,2),(3,4)),((3,4),(5,6)),((5,6),(-5,-9)),((3,9),(1,-2))])
    
    def test_whitespace_segs(self):
        """Test whitespace in file, expects it to be sorted away and data to be extracted."""
        result =Validators.extract_file_data(r'Tests/regex_tests\whitespace_segs.txt')
        self.assertEqual(result, [((1,5),(9,4)),((5,9),(1,2)),((1,9),(9,2)),((1,2),(3,4))])


class Test_extract_file_data_segments(unittest.TestCase):
    def test_characters(self):
        """Test segments with characters, expects ValueError."""
        with self.assertRaises(ValueError):
           Validators.extract_file_data(r'Tests/regex_tests\segments\characters.txt')

    def test_correct_file(self):
        """Test segments with correct data, expects correct data."""
        result =Validators.extract_file_data(r'Tests/regex_tests\segments\correctfile.txt')
        self.assertEqual(result, [((1,2),(3,4)),((5,6),(7,8)),((9,1),(1,1))])

    def test_large_numbers(self):
        """Test large numbers, expects the data."""
        result =Validators.extract_file_data(r'Tests/regex_tests\segments\large_numbers.txt')
        self.assertEqual(result, [((1132324123143214,123432143242),(9120924321,123423142134))])

    def test_missing_data_middle(self):
        """Test missing data in the middle, expects ValueError."""
        with self.assertRaises(ValueError):
           Validators.extract_file_data(r'Tests/regex_tests\segments\missing_data_middle.txt')

    def test_negatives(self):
        """Test negative data, expects the data."""
        result =Validators.extract_file_data(r'Tests/regex_tests\segments\negatives.txt')
        self.assertEqual(result, [((-1,-2),(-3,-4)),((-5,-6),(-7,-8)),((-9,1),(2,3))])

    def test_too_few_args(self):
        """Test too few arguments, expects ValueError."""
        with self.assertRaises(ValueError):
           Validators.extract_file_data(r'Tests/regex_tests\segments\too_few_args.txt')
            
    def test_too_many_args(self):
        """Test too many arguments, expects ValueError."""
        with self.assertRaises(ValueError):
           Validators.extract_file_data(r'Tests/regex_tests\segments\too_many_args.txt')
