from puid.bits import bit_shifts
from puid.chars import Charset, Charsets


def check_predefined(chars, shifts):
    n_chars = len(Charset(kind=chars, characters=chars.value))
    assert bit_shifts(n_chars) == shifts


def test_bit_shifts_pow_2():
    assert bit_shifts(
        len(Charset(
            kind=Charsets.CUSTOM,
            characters='dingosky',
        ))) == [(7, 3)]
    check_predefined(Charsets.HEX, [(15, 4)])
    check_predefined(Charsets.BASE32_HEX_UPPER, [(31, 5)])
    check_predefined(Charsets.SAFE64, [(63, 6)])


def test_bit_shifts_non_pow_2():
    check_predefined(Charsets.ALPHA, [(51, 6), (55, 4), (63, 3)])
    check_predefined(Charsets.ALPHA_LOWER, [(25, 5), (27, 4), (31, 3)])
    check_predefined(Charsets.ALPHANUM, [(61, 6), (63, 5)])
    check_predefined(Charsets.ALPHANUM_LOWER, [(35, 6), (39, 4), (47, 3),
                                               (63, 2)])
    check_predefined(Charsets.SAFE_ASCII, [(89, 7), (91, 6), (95, 5),
                                           (127, 2)])
