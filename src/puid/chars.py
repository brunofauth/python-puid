from __future__ import annotations

import dataclasses as dc
from enum import Enum
from collections.abc import Iterable
from puid.chars_error import InvalidChars, NonUniqueChars, LengthOutOfBounds


def CharsetMeta(type):

    def __call__(self, *args, **kwargs):
        raise RuntimeError(
            "Instantiate this class through one of it's constructor classmethods"
        )


@dc.dataclass(frozen=True, slots=True)
class Charset:
    kind: Charsets
    characters: str

    def __len__(self) -> int:
        return len(self.characters)

    def __iter__(self) -> Iterable[str]:
        yield from self.characters

    @classmethod
    def predefined(cls, kind: Charsets) -> Charset:
        instance = cls.__new__(cls)
        cls.__init__(instance, kind=kind, characters=kind.value)
        return instance

    @classmethod
    def custom(cls, characters: str) -> Charset:
        is_valid_charset(characters)
        instance = cls.__new__(cls)
        cls.__init__(instance, kind=Charsets.CUSTOM, characters=characters)
        return instance


print(type(Charset))


def is_valid_charset(chars: str) -> bool:
    min_len = 2
    max_len = 256

    if len(chars) not in range(min_len, max_len + 1):
        raise LengthOutOfBounds(
            f'Charsets must be [{min_len}-{max_len}] long. Yours is {len(chars)}'
        )

    if len(chars) != len(set(chars)):
        raise NonUniqueChars('Some characters repeat in your charset')

    for char in chars:
        if not _valid_char(char):
            raise InvalidChars(f'Invalid character with code: {ord(char)}')

    return True


def _valid_char(char: str) -> bool:
    code_point = ord(char)

    if 160 < code_point:
        return True

    if char == '!':
        return True
    if code_point < ord('#'):
        return False
    if char in ("'", '\\', '`'):
        return False
    if ord('~') < code_point:
        return False

    return True


class Charsets(Enum):
    """
    Predefined Characters

    These enums are intended to be passed to the `Puid` class initializer for configuration
    """

    CUSTOM = ""

    ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    ALPHA_LOWER = 'abcdefghijklmnopqrstuvwxyz'
    ALPHA_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ALPHANUM = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    ALPHANUM_LOWER = 'abcdefghijklmnopqrstuvwxyz0123456789'
    ALPHANUM_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    BASE16 = '0123456789ABCDEF'
    BASE32 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
    BASE32_HEX = '0123456789abcdefghijklmnopqrstuv'
    BASE32_HEX_UPPER = '0123456789ABCDEFGHIJKLMNOPQRSTUV'
    CROCKFORD32 = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
    DECIMAL = '0123456789'
    HEX = '0123456789abcdef'
    HEX_UPPER = '0123456789ABCDEF'
    SAFE_ASCII = '!#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}~'
    SAFE32 = '2346789bdfghjmnpqrtBDFGHJLMNPQRT'
    SAFE64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    SYMBOL = '!#$%&()*+,-./:;<=>?@[]^_{|}~'
    WORD_SAFE32 = '23456789CFGHJMPQRVWXcfghjmpqrvwx'

    def __len__(self):
        return len(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"


if __name__ == '__main__':  # pragma: no cover
    import doctest

    doctest.testmod()
