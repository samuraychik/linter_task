import re

from linter_rules import ItemType, \
    WhitespaceRule, EmptylineRule, NamingRule, NamingCase
from linter_logger import LinterLogger


class Linter:
    def __init__(self, code_style: dict, logger: LinterLogger):
        self.whitespace_rules = code_style[ItemType.WHITESPACE_RULESET]
        self.emptyline_rules = code_style[ItemType.EMPTYLINE_RULESET]
        self.naming_rules = code_style[ItemType.NAMING_RULESET]
        self.separators = code_style[ItemType.SEPARATORS]
        self.binary_ops = code_style[ItemType.BINARY_OPS]
        self.keywords = code_style[ItemType.KEYWORDS]
        self.logger = logger

    def get_case_regex(self, case: NamingCase) -> str:
        case_regex = {
            NamingCase.UPPER_SNAKE_CASE: r"[A-Z][_A-Z1-9]*",
            NamingCase.SNAKE_CASE: r"[a-z][_a-z1-9]*",
            NamingCase.PASCAL_CASE: r"([A-Z][a-z1-9]*)*",
            NamingCase.CAMEL_CASE: r"[a-z][a-z1-9]*([A-Z][a-z1-9]*)*",
        }
        return case_regex[case]

    def check_all_file(self, filepath):
        is_first_subroutine = True
        check_var_naming = False
        curr_emptylines = 0
        last_emptylines = 0

        with open(filepath, "r") as f:
            for (index, line) in enumerate(f):
                line = line.strip().replace("\n", "")
                
                if line == "":
                    curr_emptylines += 1
                    continue
                
                last_emptylines = curr_emptylines
                curr_emptylines = 0

                self.check_max_emptylines(index - last_emptylines, last_emptylines)
                self.check_whitespace_rules(index, line)

                subroutine = self.find_subroutine_at_line_start(line)
                if subroutine:
                    self.check_naming_rules(index, line.removeprefix(subroutine))
                    if not is_first_subroutine:
                        self.check_subroutine_emptylines(index, last_emptylines)
                    is_first_subroutine = False

                if line.lower() == "begin":
                    check_var_naming = False
                if line.lower() == "var" or line.lower().startswith("var "):
                    check_var_naming = True
                if check_var_naming:
                    self.check_naming_rules(index, line.removeprefix("var"))

            self.check_eof_emptylines(index, last_emptylines)
            

    def check_whitespace_rules(self, index: int, line: str) -> None:
        bin_status = self.check_binary_op_rules(line)
        sep_status = self.check_separators_rules(line)
        self.logs_errors_for_line(index, bin_status | sep_status)
    
    def check_max_emptylines(self, index: int, current: int) -> None:
        errors = set()

        limit = self.emptyline_rules[EmptylineRule.MAX_IN_A_ROW]
        if current > limit:
            errors.add(f"Too many empty lines in a row - "
                       f"{current}, limit is {limit}")
        self.logs_errors_for_line(index, errors)
    
    def check_subroutine_emptylines(self, index: int, count: int) -> None:
        errors = set()

        correct = self.emptyline_rules[EmptylineRule.BETWEEN_SUBROUTINES]
        if count != correct:
            errors.add(f"Should have {count} empty line(s) between "
                       f"subroutines, not {correct}.")
        self.logs_errors_for_line(index, errors)

    def check_eof_emptylines(self, index: int, count: int) -> None:
        errors = set()
        
        correct = self.emptyline_rules[EmptylineRule.END_OF_FILE]
        if count != correct:
            errors.add(f"Should have {correct} empty line(s) at "
                       f"the end of file, not {count}")
        self.logs_errors_for_line(index, errors)

    def check_naming_rules(self, index: int, line: str) -> None:
        errors = set()

        identifiers = []
        clips = self.split_many(line, [",", "(", ")"])
        for clip in clips:
            identifier = clip.split(":")[0]
            identifier = identifier.strip()
            if identifier != "":
                identifiers.append(identifier)

        naming_case = self.naming_rules[NamingRule.IDENTIFIER]
        case_pattern = self.get_case_regex(naming_case)
        for id_name in identifiers:
            match = re.fullmatch(case_pattern, id_name)
            if not match:
                errors.add(f"Identifier '{id_name}' "
                           f"is not in {naming_case.value}.")
        self.logs_errors_for_line(index, errors)

    def check_separators_rules(self, line: str) -> set:
        errors = set()

        separators = [sep for sep in self.separators if sep in line]
        if not separators:
            return errors
        for sep in separators:
            matches_iter = re.finditer(r' *' + re.escape(sep) + r' *', line)
            for match in matches_iter:
                whitespaces = match.group().split(sep)
                if len(whitespaces[0]) != self.whitespace_rules[WhitespaceRule.BEFORE_SEP]:
                    errors.add(f"Before '{sep}' should be "
                               f"{self.whitespace_rules[WhitespaceRule.BEFORE_SEP]} whitespace(s)")
                if len(whitespaces[1]) != self.whitespace_rules[WhitespaceRule.AFTER_SEP]:
                    errors.add(f"After '{sep}' should be "
                               f"{self.whitespace_rules[WhitespaceRule.AFTER_SEP]} whitespace(s)")
        return errors

    def check_binary_op_rules(self, line: str) -> set:
        errors = set()

        binary_ops = [binop for binop in self.binary_ops if binop in line]
        if not binary_ops:
            return errors
        for binop in binary_ops:
            matches_iter = re.finditer(r' *' + re.escape(binop) + r' *', line)
            for match in matches_iter:
                whitespaces = match.group().split(binop)
                if len(whitespaces[0]) != self.whitespace_rules[WhitespaceRule.BEFORE_BINOP]:
                    errors.add(f"Before '{binop}' should be "
                               f"{self.whitespace_rules[WhitespaceRule.BEFORE_BINOP]} whitespace(s)")
                if len(whitespaces[1]) != self.whitespace_rules[WhitespaceRule.AFTER_BINOP]:
                    errors.add(f"After '{binop}' should be "
                               f"{self.whitespace_rules[WhitespaceRule.AFTER_BINOP]} whitespace(s)")
        return errors

    def find_subroutine_at_line_start(self, line: str) -> str:
        for subroutine in ["program ", "procedure ", "function "]:
            if line.startswith(subroutine):
                return subroutine

    def split_many(self, text: str, seps: list) -> list:
        default_sep = seps[0]

        for sep in seps[1:]:
            text = text.replace(sep, default_sep)
        return [clip.strip() for clip in text.split(default_sep)]

    def logs_errors_for_line(self, index: int, log: set) -> None:
        if log:
            print(f"In line {index + 1}, {log}")
