import pytest

from puid.chars import is_valid_charset, Charsets, Charset
from puid.chars_error import InvalidChars
from puid.chars_error import NonUniqueChars
from puid.chars_error import LengthOutOfBounds


def predefined_chars():
    sets = (Charset.predefined(cs) for cs in Charsets if cs != Charsets.CUSTOM)
    yield from sets


def test_chars_out_of_bounds():
    with pytest.raises(LengthOutOfBounds):
        is_valid_charset("a")
    with pytest.raises(LengthOutOfBounds):
        is_valid_charset("".join(["a"] * 257))


def test_chars_not_unique():
    with pytest.raises(NonUniqueChars):
        Charset.custom("non-unique")


def test_invalid_chars():
    with pytest.raises(InvalidChars):
        is_valid_charset("dingosky\n")

    with pytest.raises(InvalidChars):
        is_valid_charset("dingosky'")

    with pytest.raises(InvalidChars):
        is_valid_charset('dingosky"')

    with pytest.raises(InvalidChars):
        is_valid_charset('dingosky`')

    with pytest.raises(InvalidChars):
        is_valid_charset("dingosky\\")

    with pytest.raises(InvalidChars):
        is_valid_charset("dingosky" + chr(ord("~") + 2))


def test_chars_not_valid():
    with pytest.raises(InvalidChars):
        is_valid_charset("'\\`")


def test_predefined_chars():
    for charset in predefined_chars():
        assert is_valid_charset(charset)


def test_predefined_chars_object():
    alpha = Charset.predefined(kind=Charsets.ALPHA)
    assert len(alpha) == 52


def test_custom_chars_object():
    dingosky = Charset.custom('dingosky')
    assert len(dingosky) == 8


def test_predefined_chars_values():
    for value in [chars.characters for chars in predefined_chars()]:
        assert is_valid_charset(value)


def test_chars_repr():
    hex_ = Charset.predefined(kind=Charsets.HEX)
    assert repr(hex_) == \
        "Charset(kind=Charsets.HEX, characters='0123456789abcdef')"


def test_chars_iter():
    assert [char for char in Charset.custom('dingosky')] == list('dingosky')
