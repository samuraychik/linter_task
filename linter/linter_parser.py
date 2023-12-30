from linter.linter_rules import ItemType, get_enum_item_by_name, \
    WhitespaceRule, EmptylineRule, NamingRule


class ParserDictIntegrityError(Exception):
    pass


class LinterStyleParser:
    def __init__(self):
        self.parsers_by_type = {
            ItemType.WHITESPACE_RULESET: "parse_whitespace_rules",
            ItemType.EMPTYLINE_RULESET: "parse_emptyline_rules",
            ItemType.NAMING_RULESET: "parse_naming_rules",
            ItemType.KEYWORDS: "parse_keywords",
            ItemType.BINARY_OPS: "parse_binary_operators",
            ItemType.SEPARATORS: "parse_separators",
        }

    def parse_style_doc(self, filename: str) -> dict:
        items_dict = {}

        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line.startswith("*"):
                    continue

                item_type = get_enum_item_by_name(ItemType, line[1:])

                parser_method = getattr(self, self.parsers_by_type[item_type])
                parser_method(f, items_dict)

        if not self.check_dict_integrity(items_dict):
            raise ParserDictIntegrityError()
        return items_dict

    def parse_whitespace_rules(self, file, items_dict: dict) -> None:
        default = {
            WhitespaceRule.BEFORE_BINOP: 1,
            WhitespaceRule.AFTER_BINOP: 1,
            WhitespaceRule.BEFORE_SEP: 0,
            WhitespaceRule.AFTER_SEP: 1,
        }
        self.parse_items_dict(file, items_dict, WhitespaceRule,
                              ItemType.WHITESPACE_RULESET, default)

    def parse_emptyline_rules(self, file, items_dict: dict) -> None:
        default = {
            EmptylineRule.MAX_IN_A_ROW: 1,
            EmptylineRule.BETWEEN_SUBROUTINES: 1,
            EmptylineRule.END_OF_FILE: 0,
        }
        self.parse_items_dict(file, items_dict, EmptylineRule,
                              ItemType.EMPTYLINE_RULESET, default)

    def parse_naming_rules(self, file, items_dict: dict) -> None:
        default = {
            NamingRule.IDENTIFIER: 1,
        }
        self.parse_items_dict(file, items_dict, NamingRule,
                              ItemType.NAMING_RULESET, default)

    def parse_keywords(self, file, items_dict: dict) -> None:
        self.parse_items_list(file, items_dict, ItemType.KEYWORDS)

    def parse_binary_operators(self, file, items_dict: dict) -> None:
        self.parse_items_list(file, items_dict, ItemType.BINARY_OPS)

    def parse_separators(self, file, items_dict: dict) -> None:
        self.parse_items_list(file, items_dict, ItemType.SEPARATORS)

    def parse_items_dict(self, file,
                         items_dict: dict, enum: type,
                         rule_type: ItemType, default: dict) -> None:

        ruleset = dict(default)
        line = next(file).strip()
        while line:
            rule_str, value_str = line.split(":")
            rule = get_enum_item_by_name(enum, rule_str)
            value = int(value_str)
            ruleset[rule] = value

            try:
                line = next(file).strip()
            except StopIteration:
                break
        
        items_dict[rule_type] = ruleset

    def parse_items_list(self, file,
                         items_dict: dict,
                         item_type: ItemType) -> None:
        line = next(file).strip()
        if not line:
            items_dict[item_type] = list()
        else:
            items_dict[item_type] = line.split(" ")

    def check_dict_integrity(self, items: dict):
        return len(items) == len(ItemType)
