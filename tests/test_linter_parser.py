import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from linter import linter_rules as lr
from linter import linter_parser as lp


class ParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = lp.LinterStyleParser()

    def tearDown(self) -> None:
        del self.parser

    def test_parse_binops(self):
        res = self.parser.parse_style_doc(
            "tests/test_files/style_docs/binops.txt")
        expected = ["+", "magic", "42", "(^_^)"]
        self.assertCountEqual(res[lr.ItemType.BINARY_OPS], expected)
        self.assertCountEqual(res[lr.ItemType.SEPARATORS], list())
        self.assertCountEqual(res[lr.ItemType.KEYWORDS], list())
        
    def test_parse_separators(self):
        res = self.parser.parse_style_doc(
            "tests/test_files/style_docs/separators.txt")
        expected = ["+", "magic", "42", "(^_^)"]
        self.assertCountEqual(res[lr.ItemType.SEPARATORS], expected)
        self.assertCountEqual(res[lr.ItemType.BINARY_OPS], list())
        self.assertCountEqual(res[lr.ItemType.KEYWORDS], list())

    def test_parse_keywords(self):
        res = self.parser.parse_style_doc(
            "tests/test_files/style_docs/keywords.txt")
        expected = ["+", "magic", "42", "(^_^)"]
        self.assertCountEqual(res[lr.ItemType.KEYWORDS], expected)
        self.assertCountEqual(res[lr.ItemType.BINARY_OPS], list())
        self.assertCountEqual(res[lr.ItemType.SEPARATORS], list())

    def test_parse_whitespace_rules(self):
        res = self.parser.parse_style_doc(
            "tests/test_files/style_docs/whitespace.txt")
        expected = {
            lr.WhitespaceRule.BEFORE_BINOP: 1,
            lr.WhitespaceRule.AFTER_BINOP: 2,
            lr.WhitespaceRule.BEFORE_SEP: 3,
            lr.WhitespaceRule.AFTER_SEP: 4,
        }
        self.assertCountEqual(res[lr.ItemType.WHITESPACE_RULESET], expected)

    def test_parse_emptyline_rules(self):
        res = self.parser.parse_style_doc(
            "tests/test_files/style_docs/emptyline.txt")
        expected = {
            lr.EmptylineRule.MAX_IN_A_ROW: 1,
            lr.EmptylineRule.BETWEEN_SUBROUTINES: 2,
            lr.EmptylineRule.END_OF_FILE: 3,
        }
        print(res[lr.ItemType.EMPTYLINE_RULESET])
        self.assertCountEqual(res[lr.ItemType.EMPTYLINE_RULESET], expected)

    def test_parse_naming_rules(self):
        res = self.parser.parse_style_doc(
            "tests/test_files/style_docs/naming.txt")
        expected = {
            lr.NamingRule.IDENTIFIER: 1,
        }
        self.assertCountEqual(res[lr.ItemType.NAMING_RULESET], expected)


if __name__ == "__main__":
    unittest.main()
