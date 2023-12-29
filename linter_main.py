import argparse
import os
import sys
from linter_parser import CodeStyleParser
from linter_checker import Linter
from linter_rules import ItemsType, WhitespaceRule

argparser = argparse.ArgumentParser(
    description="Check your pascal code style!")

argparser.add_argument("path", metavar="PATH", type=str,
                       help="path to your file or folder")  # Заменить на получение кучи параметров


def log_error(message):
    print(f"<H_ERROR> {message}")


def main(argv=None):
    # args = argparser.parse_args(argv)
    # if os.path.isdir(args.path):
    #     print("Это путь до директории")
    # elif os.path.isfile(args.path):
    #     print("Это путь до файла")
    # else:
    #     log_error(f"{args.path}: incorrect path value")
    #     sys.exit(1)

    test_dict = {ItemsType.WHITESPACE_RULESET: {WhitespaceRule.BEFORE_SEP: 0,
                                                WhitespaceRule.AFTER_SEP: 0,
                                                WhitespaceRule.BEFORE_BINOP: 1,
                                                WhitespaceRule.AFTER_BINOP: 1,
                                                WhitespaceRule.AFTER_UNOP: 0,
                                                },
                 ItemsType.EMPTYLINE_RULESET: {},
                 ItemsType.NAMING_RULESET: {},
                 ItemsType.KEYWORDS: {},
                 ItemsType.UNARY_OPS: {'-'},
                 ItemsType.BINARY_OPS: {'=', '-', '+'},
                 ItemsType.SEPARATORS: {',', ':', ';'}
                 }
    linter = Linter(test_dict)
    linter.check_all_file("test_text.txt")


if __name__ == "__main__":
    main()
