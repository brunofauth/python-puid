from collections import OrderedDict

import scipy.stats as stats

from puid import Charsets
from puid import Puid

trials = 50_000
risk = 1e12


def occurs(trials, rand_id, char):
    expect = trials * rand_id.len / len(rand_id.chars)
    count = 0
    for _ in range(trials):
        for ch in rand_id.generate():
            if ch == char:
                count += 1

    return expect, count


def chi_square(trials, risk, chars):
    rand_id = Puid(trials, risk, charset=chars)

    observed = OrderedDict((char, 0) for char in rand_id.charset)
    for _ in range(trials):
        for ch in rand_id.generate():
            observed[ch] += 1

    chars_len = len(rand_id.charset)
    expected = [rand_id.size * trials / chars_len] * chars_len

    significance = 0.05
    _, p_value = stats.chisquare(list(observed.values()), expected)

    assert significance < p_value


def test_custom8():
    chi_square(trials, risk, chars='dingosky')


def test_hex():
    chi_square(trials, risk, chars=Charsets.HEX)


def test_alphanum():
    chi_square(trials, risk, chars=Charsets.ALPHANUM)


def test_safe32():
    chi_square(trials, risk, chars=Charsets.SAFE32)


def test_safe_ascii():
    chi_square(trials, risk, chars=Charsets.SAFE_ASCII)


def test_unicode():
    chi_square(trials, risk, chars='dîñgø$kyDÎÑGØßK¥')


def test_alpha_10_lower():
    chi_square(trials, risk, chars='abcdefghij')
