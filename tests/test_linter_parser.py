import os
import sys
import unittest
from linter_parser import LinterStyleParser


class ParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = LinterStyleParser

    def tearDown(self) -> None:
        del self.parser
