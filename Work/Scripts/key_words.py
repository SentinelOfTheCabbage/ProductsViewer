from enum import Enum


class CompareOp(Enum):
    EQUAL = "="
    NOT_EQUAL = "!="
    LESS = "<"
    LESS_OR_EQUAL = "<="
    MORE = ">"
    MORE_OR_EQUAL = ">="


class Expression:
    def __init__(self, field: str, compare_op: CompareOp,  value):
        self.field = field
        self.compare_op = compare_op
        self.value = value

    def set_field(self, field):
        self.field = field

    def set_compare_op(self, compare_op):
        self.compare_op = compare_op

    def set_value(self, value):
        self.value = value

    def get_expression(self):
        return self.field, self.compare_op, self.value

