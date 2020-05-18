from typing import List
import sqlalchemy.types as types


class BitField(types.TypeDecorator):
    """List of bit flag, stored as num
    [0, 0, 0, 1, 0, 1] -> 5
    """

    impl = types.SmallInteger

    def process_bind_param(self, value: List[bool], dialect) -> int:
        return int("".join([
            str(int(x)) for x in value
        ]), base=2)

    def process_result_value(self, value: int, dialect) -> List[bool]:
        _lst = list(map(lambda x: bool(int(x)), bin(value)[2::]))
        zero_padding = [False] * (6 - len(_lst))
        return zero_padding + _lst


class CommaSeparatedString(types.TypeDecorator):
    separator: str = ";"
    impl = types.String

    def process_bind_param(self, value: List[str], dialect) -> str:
        if not value:
            return ""
        return self.separator.join(value)

    def process_result_value(self, value: str, dialect) -> List[str]:
        if not value:
            return []
        return value.split(self.separator)
