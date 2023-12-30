from enum import Enum


class UnknownItemError(Exception):
    pass


class ItemType(Enum):
    KEYWORDS = "KEYWORDS"
    BINARY_OPS = "BINARY_OPS"
    UNARY_OPS = "UNARY_OPS"
    SEPARATORS = "SEPARATORS"
    WHITESPACE_RULESET = "WHITESPACE_RULESET"
    EMPTYLINE_RULESET = "EMPTYLINE_RULESET"
    NAMING_RULESET = "NAMING_RULESET"


class WhitespaceRule(Enum):
    BEFORE_BINOP = "BEFORE_BINOP"
    AFTER_BINOP = "AFTER_BINOP"
    BEFORE_SEP = "BEFORE_SEP"
    AFTER_SEP = "AFTER_SEP"


class EmptylineRule(Enum):
    MAX_IN_A_ROW = "MAX_IN_A_ROW"
    BETWEEN_SUBROUTINES = "BETWEEN_SUBROUTINES"
    END_OF_FILE = "END_OF_FILE"


class NamingRule(Enum):
    IDENTIFIER = "IDENTIFIER"


class NamingCase(Enum):
    SNAKE_CASE = 0
    UPPER_SNAKE_CASE = 1
    PASCAL_CASE = 2
    CAMEL_CASE = 3


def get_enum_item_by_name(enum: type, name: str):
    for item in enum.__members__.values():
        if item.name == name:
            return item
    raise UnknownItemError()
