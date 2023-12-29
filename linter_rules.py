from enum import Enum


class WhitespaceRule(Enum):
    BEFORE_BINOP = "before_binop"
    AFTER_BINOP = "after_binop"
    AFTER_UNOP = "after_unop"
    BEFORE_SEP = "before_sep"
    AFTER_SEP = "after_sep"


class ItemsType(Enum):
    KEYWORD = "*KEYWORDS:"
    BINARY_OP = "*BINARY-OPS:"
    UNARY_OP = "*UNARY-OPS:"
    SEPARATOR = "*SEPARATORS:"
    WHITESPACE_RULESET = "*WHITESPACE-RULESET:"
    EMPTYLINE_RULESET = "*EMPTYLINE-RULESET:"
    NAMING_RULESET = "*NAMING-RULESET:"


def get_item_type_by_value(value: str):
    for item_type in ItemsType.__members__.values():
        if item_type.value == value:
            return item_type
