from linter_rules import WhitespaceRule, ItemsType, get_item_type_by_value


class CodeStyleParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_style_doc(link: str):
        items_dict = {"keywords": [],
                      "binary-ops": [],
                      }
        whitespace_rules_dict = {"before_binop": 0,  # для этих шняг можно и энумчик наверное со значением как в файлике
                                 "after_binop": 0,
                                 "after_unop": 0,
                                 "before_sep": 0,
                                 "after_sep": 0,
                                 }
        with open(link, "r") as f:
            for line in f:
                line = line.strip()
                item_type = get_item_type_by_value(line)
                if item_type:
                    if (item_type == ItemsType.KEYWORD
                            or item_type == ItemsType.BINARY_OP
                            or item_type == ItemsType.UNARY_OP):
                        items = next(f)
                        whitespace_rules_dict[item_type] = items.split(",")
                        print(whitespace_rules_dict[item_type])
                    # elif item_type == ItemsType.WHITESPACE_RULESET:
                    #     while line.strip():
                    #         rule = "*".split(line).



