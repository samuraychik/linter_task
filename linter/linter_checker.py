import re

from linter.linter_rules import ItemType, \
    WhitespaceRule, EmptylineRule, NamingRule, NamingCase
from linter.linter_logger import LinterLogger


class Linter:
    def __init__(self, code_style: dict, logger: LinterLogger):
        self.whitespace_rules = code_style[ItemType.WHITESPACE_RULESET]
        self.emptyline_rules = code_style[ItemType.EMPTYLINE_RULESET]
        self.naming_rules = code_style[ItemType.NAMING_RULESET]
        self.separators = code_style[ItemType.SEPARATORS]
        self.binary_ops = code_style[ItemType.BINARY_OPS]
        self.keywords = code_style[ItemType.KEYWORDS]
        
        self.index = 0
        self.logger = logger

    def get_case_regex(self, case: NamingCase) -> str:
        case_regex = {
            NamingCase.UPPER_SNAKE_CASE: r"[A-Z][_A-Z1-9]*",
            NamingCase.SNAKE_CASE: r"[a-z][_a-z1-9]*",
            NamingCase.PASCAL_CASE: r"([A-Z][a-z1-9]*)*",
            NamingCase.CAMEL_CASE: r"[a-z][a-z1-9]*([A-Z][a-z1-9]*)*",
        }
        return case_regex[case]

    def check_file(self, filepath: str) -> None:
        is_first_subroutine = True
        check_var_naming = False
        curr_emptylines = 0
        last_emptylines = 0

        with open(filepath, "r") as f:
            for line in f:
                self.index += 1
                line = line.strip().replace("\n", "")
                
                if line == "":
                    curr_emptylines += 1
                    continue
                
                last_emptylines = curr_emptylines
                curr_emptylines = 0

                self.check_max_emptylines(last_emptylines)
                self.check_whitespace_rules(line)

                subroutine = self.find_subroutine_at_line_start(line)
                if subroutine:
                    self.check_naming_case(line.removeprefix(subroutine))

                    if not is_first_subroutine:
                        self.check_subroutine_emptylines(last_emptylines)
                    else:
                        is_first_subroutine = False
                        check_var_naming = False

                if line.lower() == "begin":
                    check_var_naming = False
                if line.lower() == "var" or line.lower().startswith("var "):
                    check_var_naming = True
                if check_var_naming:
                    self.check_naming_case(line.removeprefix("var"))

            self.check_eof_emptylines(last_emptylines)

    def check_whitespace_rules(self, line: str) -> None:
        self.check_binary_ops(line)
        self.check_separators(line)

    def check_separators(self, line: str) -> None:
        before_correct = self.whitespace_rules[WhitespaceRule.BEFORE_SEP]
        after_correct = self.whitespace_rules[WhitespaceRule.AFTER_SEP]
        self.check_binary_items(line, self.separators,
                                before_correct, after_correct)

    def check_binary_ops(self, line: str) -> None:
        before_correct = self.whitespace_rules[WhitespaceRule.BEFORE_BINOP]
        after_correct = self.whitespace_rules[WhitespaceRule.AFTER_BINOP]
        self.check_binary_items(line, self.separators,
                                before_correct, after_correct)

    def check_max_emptylines(self, current: int) -> None:
        limit = self.emptyline_rules[EmptylineRule.MAX_IN_A_ROW]
        if current > limit:
            self.logger.log_emptylines_max(self.index - 1, current, limit)

    def check_subroutine_emptylines(self, count: int) -> None:
        correct = self.emptyline_rules[EmptylineRule.BETWEEN_SUBROUTINES]
        if count != correct:
            self.logger.log_emptylines_sub(self.index, count, correct)

    def check_eof_emptylines(self, count: int) -> None:
        correct = self.emptyline_rules[EmptylineRule.END_OF_FILE]
        if count != correct:
            self.logger.log_emptylines_eof(self.index, count, correct)

    def check_naming_case(self, line: str) -> None:
        identifiers = []
        clips = self.split_many(line, [",", "(", ")"])
        for clip in clips:
            identifier = clip.split(":")[0]
            identifier = identifier.strip()
            if identifier != "":
                identifiers.append(identifier)

        naming_case = NamingCase(self.naming_rules[NamingRule.IDENTIFIER])
        case_pattern = self.get_case_regex(naming_case)
        for name in identifiers:
            match = re.fullmatch(case_pattern, name)
            if not match:
                self.logger.log_naming_case(self.index, name, 
                                            naming_case.name)

    def check_binary_items(self, line: str, items: list,
                           before_correct: int, after_correct: int) -> None:
        before_errors = set()
        after_errors = set()

        binary_items = [item for item in items if item in line]
        if not binary_items:
            return
        for item in binary_items:
            matches_iter = re.finditer(r' *' + re.escape(item) + r' *', line)
            for match in matches_iter:
                whitespaces = match.group().split(item)
                before_actual = len(whitespaces[0])
                after_actual = len(whitespaces[1])
                if before_actual != before_correct:
                    before_errors.add((item, before_actual))
                if after_actual != after_correct:
                    after_errors.add((item, after_actual))

        for b_item, b_actual in before_errors:
            self.logger.log_before_item(self.index, b_item, 
                                        b_actual, before_correct)
        for a_item, a_actual in before_errors:
            self.logger.log_after_item(self.index, a_item, 
                                       a_actual, after_correct)

    def find_subroutine_at_line_start(self, line: str) -> str:
        for subroutine in ["program ", "procedure ", "function "]:
            if line.startswith(subroutine):
                return subroutine

    def split_many(self, text: str, seps: list) -> list:
        default_sep = seps[0]

        for sep in seps[1:]:
            text = text.replace(sep, default_sep)
        return [clip.strip() for clip in text.split(default_sep)]
