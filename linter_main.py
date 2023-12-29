import argparse
import os
import sys

from linter_parser import LinterStyleParser


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
    parser = LinterStyleParser()
    parser.parse_style_doc("pascal_rules.txt")


if __name__ == "__main__":
    main()
