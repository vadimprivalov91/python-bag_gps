from typing import TypeVar

T = TypeVar('T')


class CommaSeparatedValues():
    def __init__(self, s = str):    # -> None
        self.xs = dict(enumerate(map(str.strip, s.split(','))))

    def get(self, i = int, default = T):     # -> T
        x = self.xs.get(i, default)
        return type(default)(x) if x is not '' else default
