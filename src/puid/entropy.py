from math import ceil, log2, trunc

from puid.chars import Charset
from puid.chars_error import InvalidChars
from puid.puid_error import TotalRiskError


def bits_for_total_risk(total: int, risk: float) -> float:
    """
    Entropy bits necessary to produce a `total` `puid`s with given `risk` of repeat

    :param total: int
    :param risk: int
    :return float

    >>> bits_for_total_risk(100_000, 1e12)
    72.08241808752197
    """

    if total < 0 or risk < 0:
        raise TotalRiskError('total and risk must be non-negative')

    if total in [0, 1] or risk in [0, 1]:
        return 0

    if total < 1000:
        return log2(total) + log2(total - 1) + log2(risk) - 1
    else:
        return 2 * log2(total) + log2(risk) - 1


def bits_per_char(chars: Charset) -> float:
    """
    Entropy bits per character for either a predefined Chars enum or a string of characters

    :param chars: Either a Chars enum or a string

    raises CharsError subclass if `chars` is invalid

    >>> bits_per_char(Chars.BASE32)
    5.0

    >>> bits_per_char('dingosky_me')
    3.4594316186372973
    """
    return log2(len(chars))


def bits_for_len(chars, len):
    """
    Bits necessary for a `puid` of length `len` using characters `chars`

    :param chars: Either a Chars enum or a string
    :param len: Desired length of `puid`

    raises CharsError subclass if `chars` is invalid

    >>> bits_for_len('dingosky', 14)
    42
    """
    return trunc(len * bits_per_char(chars))


def len_for_bits(chars, bits):
    """
    Length necessary for a `puid` of `bits` using characters `chars`

    :param chars: Either a Chars enum or a string
    :param bits: Desired `bits` of `puid`

    raises CharsError subclass if `chars` is invalid

    >>> len_for_bits(Chars.SAFE_ASCII, 97)
    15
    """
    return ceil(bits / bits_per_char(chars))


if __name__ == '__main__':   # pragma: no cover
    import doctest

    doctest.testmod()
