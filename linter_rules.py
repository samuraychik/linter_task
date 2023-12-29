from enum import Enum


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
    AFTER_UNOP = "AFTER_UNOP"
    BEFORE_SEP = "BEFORE_SEP"
    AFTER_SEP = "AFTER_SEP"


class EmptylineRule(Enum):
    pass


class NamingRule(Enum):
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"


class NamingCase(Enum):
    SNAKE_CASE = "snake_case"
    UPPER_SNAKE_CASE = "UPPER_SNAKE_CASE"
    PASCAL_CASE = "PascalCase"
    CAMEL_CASE = "camelCase"


def get_enum_item_by_value(enum: type, value: str):
    for item in enum.__members__.values():
        if item.value == value:
            return item
