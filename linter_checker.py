from linter_rules import ItemsType, WhitespaceRule
import re


class Linter:
    def __init__(self, code_style: dict):
        self.whitespace_rules = code_style[ItemsType.WHITESPACE_RULESET]
        self.emptyline_rules = code_style[ItemsType.EMPTYLINE_RULESET]
        self.naming_rules = code_style[ItemsType.NAMING_RULESET]
        self.separators = code_style[ItemsType.SEPARATORS]
        self.binary_ops = code_style[ItemsType.BINARY_OPS]
        self.unary_ops = code_style[ItemsType.UNARY_OPS]
        self.keywords = code_style[ItemsType.KEYWORDS]

    def check_all_file(self, filepath):
        with open(filepath, "r") as f:
            for (index, line) in enumerate(f):
                line = line.replace("\n", "")
                self.check_whitespace_rules(index, line)

    def check_whitespace_rules(self, index: int, line: str) -> []:
        bin_status = self.check_binary_op_rules(line)
        sep_status = self.check_separators_rules(line)
        un_status = self.check_unary_op_rules(line)
        print(f"{index + 1}. '{line}': {bin_status | sep_status | un_status}")

    def check_naming_rules(self, line: str):
        pass

    def check_unary_op_rules(self, line: str):
        check_logs = set()
        unary_ops = [unop for unop in self.unary_ops if unop in line]
        if not unary_ops:
            return check_logs
        for unop in unary_ops:
            matches_iter = re.finditer(r'^\w+' + re.escape(unop) + r' *\w*\d*', line)
            for match in matches_iter:
                whitespaces = match.group().split(unop)
                if len(whitespaces[1]) != self.whitespace_rules[WhitespaceRule.AFTER_UNOP]:
                    check_logs.add(f"After '{unop}' should be "
                                   f"{self.whitespace_rules[WhitespaceRule.AFTER_UNOP]} whitespace(s)")
        return check_logs

    def check_separators_rules(self, line: str):
        check_logs = set()
        separators = [sep for sep in self.separators if sep in line]
        if not separators:
            return check_logs
        for sep in separators:
            matches_iter = re.finditer(r' *' + re.escape(sep) + r' *', line)
            for match in matches_iter:
                whitespaces = match.group().split(sep)
                if len(whitespaces[0]) != self.whitespace_rules[WhitespaceRule.BEFORE_SEP]:
                    check_logs.add(f"Before '{sep}' should be "
                                   f"{self.whitespace_rules[WhitespaceRule.BEFORE_SEP]} whitespace(s)")
                if len(whitespaces[1]) != self.whitespace_rules[WhitespaceRule.AFTER_SEP]:
                    check_logs.add(f"After '{sep}' should be "
                                   f"{self.whitespace_rules[WhitespaceRule.AFTER_SEP]} whitespace(s)")
        return check_logs

    def check_binary_op_rules(self, line: str):
        check_logs = set()
        binary_ops = [binop for binop in self.binary_ops if binop in line]
        if not binary_ops:
            return check_logs
        for binop in binary_ops:
            matches_iter = re.finditer(r' *' + re.escape(binop) + r' *', line)
            for match in matches_iter:
                whitespaces = match.group().split(binop)
                if len(whitespaces[0]) != self.whitespace_rules[WhitespaceRule.BEFORE_BINOP]:
                    check_logs.add(f"Before '{binop}' should be "
                                   f"{self.whitespace_rules[WhitespaceRule.BEFORE_BINOP]} whitespace(s)")
                if len(whitespaces[1]) != self.whitespace_rules[WhitespaceRule.AFTER_BINOP]:
                    check_logs.add(f"After '{binop}' should be "
                                   f"{self.whitespace_rules[WhitespaceRule.AFTER_BINOP]} whitespace(s)")
        return check_logs
