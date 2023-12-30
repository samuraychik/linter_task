import os
import sys
import unittest
import linter_main as linter

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))


class LinterTestCase(unittest.TestCase):
    def test_skip_bad_path(self):
        with self.assertRaises(SystemExit) as e:
            linter.main([r"this_path/does_not/exist"])
        self.assertEqual(e.exception.code, 0)

    def test_check_var_naming(self):
        with self.assertRaises(SystemExit) as e:
            linter.main([r"test_files/pascal_code/one_var_line.txt"])

        first_path = r"style_check_result.txt"
        second_path = r"test_files/reports/var_one_line_report.txt"
        with open(first_path) as file1, open(second_path) as file2:
            self.assertCountEqual(list(file1), list(file2))

    def test_check_hard_var_naming(self):
        with self.assertRaises(SystemExit) as e:
            linter.main([r"test_files/pascal_code/three_lines_with_vars.txt"])

        first_path = r"style_check_result.txt"
        second_path = r"test_files/reports/var_three_lines_report.txt"
        with open(first_path) as file1, open(second_path) as file2:
            self.assertCountEqual(list(file1), list(file2))

    def test_check_function(self):
        with self.assertRaises(SystemExit) as e:
            linter.main([r"test_files/pascal_code/with_function.txt"])

        first_path = "style_check_result.txt"
        second_path = "test_files/reports/function_report.txt"
        with open(first_path) as file1, open(second_path) as file2:
            self.assertCountEqual(list(file1), list(file2))

    def test_check_two_functions(self):
        with self.assertRaises(SystemExit) as e:
            linter.main(["test_files/pascal_code/with_two_functions.txt"])

        first_path = "style_check_result.txt"
        second_path = "test_files/reports/two_functions_report.txt"
        with open(first_path) as file1, open(second_path) as file2:
            self.assertCountEqual(list(file1), list(file2))

    def test_check_all_files_in_directory(self):
        with self.assertRaises(SystemExit) as e:
            linter.main(["test_files/pascal_code"])

        first_path = "style_check_result.txt"
        second_path = "test_files/reports/directory_report.txt"
        with open(first_path) as file1, open(second_path) as file2:
            self.assertCountEqual(list(file1), list(file2))
