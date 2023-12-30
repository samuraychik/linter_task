import argparse
import os
import sys

from linter import linter_checker as lc
from linter import linter_logger as ll
from linter import linter_parser as lp


argparser = argparse.ArgumentParser(
    description="Check your Pascal code style!")

argparser.add_argument("-s", "--style_path", metavar="S_PATH",
                       type=str, default="default_pascal_style.txt",
                       help="path to your file with style rules")

argparser.add_argument("-l", "--log_path", metavar="L_PATH",
                       type=str, default="style_check_result.txt",
                       help="path to output your log")

argparser.add_argument("code_paths", metavar="C_PATH", nargs='+',
                       type=str, help="paths to your files or folders")


def log_error(message):
    print(f"<H_ERROR> {message}")


def main(argv=None):
    args = argparser.parse_args(argv)
    style_path = args.style_path
    log_path = args.log_path
    input_paths = args.code_paths
    
    file_paths = []
    for path in input_paths:
        if os.path.isdir(path):
            file_paths += [os.path.abspath(os.path.join(path, file))
                           for file in os.listdir(path)
                           if os.path.isfile(os.path.join(path, file))]
        elif os.path.isfile(path):
            file_paths.append(path)
        else:
            log_error(f"{path}: incorrect path value")

    parser = lp.LinterStyleParser()
    style_dict = parser.parse_style_doc(style_path)

    open(log_path, 'w').close() # resets the log file
    logger = ll.LinterLogger(log_path)
    linter = lc.Linter(style_dict, logger)

    for file_path in file_paths:
        logger.log_new_header(os.path.basename(file_path))
        linter.check_file(file_path)
    
    print(f"Created new Linter log at {log_path}")
    sys.exit(0)


if __name__ == "__main__":
    main()
