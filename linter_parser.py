from linter_rules import ItemType, get_enum_item_by_value, \
    WhitespaceRule, EmptylineRule, NamingRule, NamingCase


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

                item_type = get_enum_item_by_value(ItemType, line[1:])

                parser_method = getattr(self, self.parsers_by_type[item_type])
                parser_method(f, items_dict)

        return items_dict

    def parse_whitespace_rules(self, file, items_dict: dict) -> None:
        whitepsace_ruleset = {
            WhitespaceRule.BEFORE_BINOP: 1,
            WhitespaceRule.AFTER_BINOP: 1,
            WhitespaceRule.BEFORE_SEP: 0,
            WhitespaceRule.AFTER_SEP: 1,
        }

        line = next(file).strip()
        while line:
            rule_str, value_str = line.split(":")
            rule = get_enum_item_by_value(WhitespaceRule, rule_str)
            value = int(value_str)
            whitepsace_ruleset[rule] = value

            try:
                line = next(file).strip()
            except StopIteration:
                break

        items_dict[ItemType.WHITESPACE_RULESET] = whitepsace_ruleset

    def parse_emptyline_rules(self, file, items_dict: dict) -> None:
        emptyline_ruleset = {
            EmptylineRule.BETWEEN_SUBROUTINES: 1,
            EmptylineRule.END_OF_FILE: 0,
            EmptylineRule.MAX_IN_A_ROW: 1,
        }
        
        line = next(file).strip()
        while line:
            rule_str, value_str = line.split(":")
            rule = get_enum_item_by_value(EmptylineRule, rule_str)
            value = int(value_str)
            emptyline_ruleset[rule] = value

            try:
                line = next(file).strip()
            except StopIteration:
                break

        items_dict[ItemType.EMPTYLINE_RULESET] = emptyline_ruleset

    def parse_naming_rules(self, file, items_dict: dict) -> None:
        naming_ruleset = {
            NamingRule.IDENTIFIER: NamingCase.PASCAL_CASE,
        }

        line = next(file).strip()
        while line:
            rule_str, value_str = line.split(":")
            rule = get_enum_item_by_value(NamingRule, rule_str)
            value = get_enum_item_by_value(NamingCase, value_str)
            naming_ruleset[rule] = value

            try:
                line = next(file).strip()
            except StopIteration:
                break

        items_dict[ItemType.NAMING_RULESET] = naming_ruleset

    def parse_keywords(self, file, items_dict: dict) -> None:
        self.parse_items_list(file, items_dict, ItemType.KEYWORDS)

    def parse_binary_operators(self, file, items_dict: dict) -> None:
        self.parse_items_list(file, items_dict, ItemType.BINARY_OPS)

    def parse_separators(self, file, items_dict: dict) -> None:
        self.parse_items_list(file, items_dict, ItemType.SEPARATORS)

    def parse_items_list(self, file,
                         items_dict: dict,
                         item_type: ItemType) -> None:
        line = next(file).strip()
        if not line:
            items_dict[item_type] = list()
        else:
            items_dict[item_type] = line.split(" ")
