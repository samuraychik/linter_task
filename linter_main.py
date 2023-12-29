import argparse
import os
import sys

from linter_parser import LinterStyleParser
from linter_checker import Linter
from linter_logger import LinterLogger

argparser = argparse.ArgumentParser(
    description="Check your pascal code style!")

argparser.add_argument("-s", "style_path", metavar="STYLE_PATH", nargs='+',
                       type=str, default="pascal_rules.txt",
                       help="path to your file with style rules")

argparser.add_argument("-l", "log_path", metavar="LOG_PATH", nargs='+',
                       type=str, default="style_check_result.txt",
                       help="path to your file with style rules")

argparser.add_argument("code_paths", metavar="PATH_TO_CODE", nargs='+',
                       type=str, help="paths to your files or folders")


def log_error(message):
    print(f"<H_ERROR> {message}")


def main(argv=None):
    args = argparser.parse_args(argv)
    style_path = args.style_path
    log_path = args.log_path
    input_paths = args.code_path
    file_paths = []
    for path in input_paths:
        if os.path.isdir(path):
            file_paths += [os.path.abspath(os.path.join(path, file))
                           for file in os.listdir(path)
                           if os.path.isfile(
                                os.path.join(path, file)
                            )]
        elif os.path.isfile(path):
            file_paths.append(path)
        else:
            log_error(f"{path}: incorrect path value")

    parser = LinterStyleParser()
    style_dict = parser.parse_style_doc(style_path)

    logger = LinterLogger(log_path)
    linter = Linter(style_dict, logger)

    for file_path in file_paths:
        logger.log_new_header(os.path.basename(file_path))
        linter.check_all_file(file_path)


if __name__ == "__main__":
    main()
