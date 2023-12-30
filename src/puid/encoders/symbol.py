from __future__ import annotations
from collections.abc import Callable


def symbol() -> Callable[[int], int]:
    bang = ord("!")
    hash_symbol = ord("#") - 1
    open_paren = ord("(") - 5
    colon = ord(":") - 13
    open_square_bracket = ord("[")
    close_square_bracket = ord("]") - 21
    open_curly_bracket = ord("{") - 24

    def encode(n: int) -> int:
        if n == 0:
            return bang
        if n < 5:
            return n + hash_symbol
        if n < 13:
            return n + open_paren
        if n < 20:
            return n + colon
        if n == 20:
            return open_square_bracket
        if n < 24:
            return n + close_square_bracket
        return n + open_curly_bracket

    return encode
