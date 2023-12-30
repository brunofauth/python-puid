from __future__ import annotations

import pytest

from puid import Charsets
from puid import Puid
from puid.chars_error import InvalidChars, NonUniqueChars
from puid.puid_error import BitsError, TotalRiskError


def check_puid(
    id: Puid,
    bits: float,
    bpc: float,
    puid_len: int,
    ere: float,
    kind: Charsets,
):
    assert round(id.bitwidth, 2) == bits
    assert round(id.bits_per_char, 2) == bpc
    assert round(id._ere, 2) == ere
    assert len(id) == puid_len
    assert id.charset.kind == kind
    assert len(id.generate()) == puid_len


def test_default():
    rand_id = Puid()
    check_puid(rand_id, 132, 6, 22, 0.75, Charsets.SAFE64)


def test_bits():
    rand_id = Puid(bitwidth=48)
    check_puid(rand_id, 48, 6, 8, 0.75, Charsets.SAFE64)


def test_total_risk():
    rand_id = Puid.from_risk(total=250_000, risk=1e12)
    check_puid(rand_id, 78, 6, 13, 0.75, Charsets.SAFE64)


def test_entropy_source():
    from random import getrandbits

    def prng_bytes(n):
        return bytearray(getrandbits(8) for _ in range(n))

    prng_id = Puid(entropy_source=prng_bytes)
    check_puid(prng_id, 132, 6, 22, 0.75, Charsets.SAFE64)


def test_invalid_bits():
    with pytest.raises(BitsError):
        Puid(bitwidth=-10)


def test_safe32_chars():
    rand_id = Puid.from_risk(total=1e6, risk=1e15, charset=Charsets.SAFE32)
    check_puid(rand_id, 90, 5, 18, 0.62, Charsets.SAFE32)


def test_alpha_chars():
    rand_id = Puid.from_risk(total=1e6, risk=1e15, charset=Charsets.ALPHA)
    check_puid(rand_id, 91.21, 5.7, 16, 0.71, Charsets.ALPHA)


def test_custom_chars():
    rand_id = Puid(charset='dingosky')
    check_puid(rand_id, 129, 3, 43, 0.38, Charsets.CUSTOM)


def test_non_unique_chars():
    with pytest.raises(NonUniqueChars):
        Puid(charset='unique')


def test_invalid_chars():
    with pytest.raises(InvalidChars):
        Puid(charset='no space')


def test_char_count_pow_2(util):
    hex_bytes = util.fixed_bytes("99 b4 4f 80 c8 89")
    hex_id = Puid(bitwidth=24, charset=Charsets.HEX, entropy_source=hex_bytes)
    assert hex_id.generate() == "99b44f"
    assert hex_id.generate() == "80c889"


def test_3bit_custom(util):
    dingosky_bytes = util.fixed_bytes("c7 c9 00 2a bd 72")
    dingosky_id = Puid(bitwidth=24,
                       charset="dingosky",
                       entropy_source=dingosky_bytes)
    assert dingosky_id.generate() == "kiyooodd"
    assert dingosky_id.generate() == "insgkskn"


def test_2bit_custom(util):
    dna_bytes = util.fixed_bytes("cb db 52 a2")
    dna_id = Puid(bitwidth=16, charset="ATCG", entropy_source=dna_bytes)
    assert dna_id.generate() == "GACGGTCG"
    assert dna_id.generate() == "TTACCCAC"


def test_1bit_custom(util):
    tf_bytes = util.fixed_bytes("fb 04 2c b3")
    tf_id = Puid(bitwidth=16, charset="FT", entropy_source=tf_bytes)
    assert tf_id.generate() == "TTTTTFTTFFFFFTFF"
    assert tf_id.generate() == "FFTFTTFFTFTTFFTT"


def test_hex_with_carry(util):
    hex_bytes = util.fixed_bytes("c7 c9 00 2a bd")
    hex_id = Puid(bitwidth=12,
                  charset=Charsets.HEX_UPPER,
                  entropy_source=hex_bytes)
    assert hex_id.generate() == "C7C"
    assert hex_id.generate() == "900"
    assert hex_id.generate() == "2AB"


def test_3bit_with_carry(util):
    #    C    7    C    9    0    0    2    A    B    D    7    2
    # 1100 0111 1100 1001 0000 0000 0010 1010 1011 1101 0111 0010
    #
    #  110 001 111 100 100 100 000 000 001 010 101 011 110 101 110 010
    #  |-| |-| |-| |-| |-| |-| |-| |-| |-| |-| |-| |-| |-| |-| |-| |-|
    #   k   i   y   o   o   o   d   d   i   n   s   g   k   s   k   n

    dingosky_bytes = util.fixed_bytes("c7 c9 00 2a bd 72")
    dingosky_id = Puid(bitwidth=9,
                       charset="dingosky",
                       entropy_source=dingosky_bytes)
    assert dingosky_id.generate() == "kiy"
    assert dingosky_id.generate() == "ooo"
    assert dingosky_id.generate() == "ddi"
    assert dingosky_id.generate() == "nsg"
    assert dingosky_id.generate() == "ksk"


def test_3bit_unicode_with_carry(util):
    dingosky_bytes = util.fixed_bytes("c7 c9 00 2a bd 72")
    dingosky_id = Puid(bitwidth=9,
                       charset="dîngøsky",
                       entropy_source=dingosky_bytes)
    assert dingosky_id.generate() == "kîy"
    assert dingosky_id.generate() == "øøø"
    assert dingosky_id.generate() == "ddî"
    assert dingosky_id.generate() == "nsg"
    assert dingosky_id.generate() == "ksk"


def test_5bit_with_carry(util):
    #    D    2    E    3    E    9    D    A    1    9    0    3    B    7    3    C
    # 1101 0010 1110 0011 1110 1001 1101 1010 0001 1001 0000 0011 1011 0111 0011 1100
    #
    # 11010 01011 10001 11110 10011 10110 10000 11001 00000 01110 11011 10011 1100
    # |---| |---| |---| |---| |---| |---| |---| |---| |---| |---| |---| |---|
    #   26    11    17    30    19    22    16    25     0    14    27    19
    #    M     h     r     R     B     G     q     L     2     n     N     B

    safe32_bytes = util.fixed_bytes("d2 e3 e9 da 19 03 b7 3c")
    safe32_id = Puid(bitwidth=20,
                     charset=Charsets.SAFE32,
                     entropy_source=safe32_bytes)
    assert safe32_id.generate() == "MhrR"
    assert safe32_id.generate() == "BGqL"
    assert safe32_id.generate() == "2nNB"


def test_5_plus_bit(util):
    # shifts: [(25, 5), (27, 4), (31, 3)])
    #
    #    5    3    c    8    8    d    e    6    3    e    2    7    e    f
    # 0101 0011 1100 1000 1000 1101 1110 0110 0011 1110 0010 0111 1110 1111
    #
    # 01010 01111 00100 01000 1101 111 00110 00111 11000 10011 111 10111 1
    # 01010 01111 00100 01000 1101 111 00110 00111 11000 10011 111 10111
    # |---| |---| |---| |---| xxxx xxx |---| |---| |---| |---| xxx |---|
    #   10    15     4     8   27   28    6     7    24    19   30   23
    #    k     p     e     i              g     h     y     t         x

    alpha_lower_bytes = util.fixed_bytes("53 c8 8d e6 3e 27 ef")
    alpha_lower_id = Puid(bitwidth=14,
                          charset=Charsets.ALPHA_LOWER,
                          entropy_source=alpha_lower_bytes)
    assert alpha_lower_id.generate() == "kpe"
    assert alpha_lower_id.generate() == "igh"
    assert alpha_lower_id.generate() == "ytx"


def test_6_plus_bit(util):
    #
    # shifts: [(61, 6), (63, 5)]
    #
    #    D    2    E    3    E    9    F    A    1    9    0    0
    # 1101 0010 1110 0011 1110 1001 1111 1010 0001 1001 0000 0000
    #
    # 110100 101110 001111 101001 11111 010000 110010 000000 0
    # |----| |----| |----| |----| xxxxx |----| |----| |----|
    #   52     46     15     41     62     16     50      0
    #    0      u      P      p             Q      y      A
    #

    alphanum_bytes = util.fixed_bytes("d2 e3 e9 fa 19 00")
    alphanum_id = Puid(bitwidth=17,
                       charset=Charsets.ALPHANUM,
                       entropy_source=alphanum_bytes)
    assert alphanum_id.generate() == "0uP"
    assert alphanum_id.generate() == "pQy"


def test_alpha_10_lower(util):
    alpha_10_lower_bytes = util.fixed_bytes(
        "8a a4 e3 8a 63 e9 d2 19 12 ce 28 51")
    alpha_10_lower_id = Puid(bitwidth=14,
                             charset="abcdefghij",
                             entropy_source=alpha_10_lower_bytes)

    alpha_10_lower_id.generate() == "ieiig"
    alpha_10_lower_id.generate() == "dheig"
    alpha_10_lower_id.generate() == "eedib"


def test_alpha_upper():
    alpha_upper_id = Puid(bitwidth=48, charset=Charsets.ALPHA_UPPER)
    check_puid(alpha_upper_id, 51.7, 4.7, 11, 0.59, Charsets.ALPHA_UPPER)


def test_base16(util):
    base16_bytes = util.fixed_bytes("c7 c9 00 2a 16 32")
    base16_id = Puid(bitwidth=12,
                     charset=Charsets.BASE16,
                     entropy_source=base16_bytes)
    assert base16_id.generate() == "C7C"
    assert base16_id.generate() == "900"
    assert base16_id.generate() == "2A1"
    assert base16_id.generate() == "632"


def test_base32(util):
    #
    # shifts: [(32, 5)]
    #
    #    D    2    E    3    E    9    F    A    1    9    1    2    C    E
    # 1101 0010 1110 0011 1110 1001 1111 1010 0001 1001 0001 0010 1100 1110
    #
    # 11010 01011 10001 11110 10011 11110 10000 11001 00010 01011 00111 0
    # |---| |---| |---| |---| |---| |---| |---| |---| |---| |---|
    #   26    11    17    30    19    30    16    25     2    11
    #    2     L     R     6     T     6     Q     Z     C     L

    base32_bytes = util.fixed_bytes("d2 e3 e9 fa 19 12 ce")
    base32_id = Puid(bitwidth=25,
                     charset=Charsets.BASE32,
                     entropy_source=base32_bytes)
    assert base32_id.generate() == "2LR6T"
    assert base32_id.generate() == "6QZCL"


def test_base32_hex(util):
    base32_hex_bytes = util.fixed_bytes("d2 e3 e9 da 19 12 ce 28")
    base32_hex_id = Puid(bitwidth=30,
                         charset=Charsets.BASE32_HEX,
                         entropy_source=base32_hex_bytes)
    assert base32_hex_id.generate() == "qbhujm"
    assert base32_hex_id.generate() == "gp2b72"


def test_base32_hex_upper(util):
    base32_hex_upper_bytes = util.fixed_bytes("d2 e3 e9 da 19 12 ce 28")
    base32_hex_upper_id = Puid(bitwidth=20,
                               charset=Charsets.BASE32_HEX_UPPER,
                               entropy_source=base32_hex_upper_bytes)
    assert base32_hex_upper_id.generate() == "QBHU"
    assert base32_hex_upper_id.generate() == "JMGP"
    assert base32_hex_upper_id.generate() == "2B72"


def test_crockford32(util):
    crockford32_bytes = util.fixed_bytes("d2 e3 e9 da 19 03 b7 3c")
    crockford32_id = Puid(bitwidth=20,
                          charset=Charsets.CROCKFORD32,
                          entropy_source=crockford32_bytes)
    assert crockford32_id.generate() == "TBHY"
    assert crockford32_id.generate() == "KPGS"
    assert crockford32_id.generate() == "0EVK"


def test_safe_ascii():
    safe_ascii_id = Puid(bitwidth=52, charset=Charsets.SAFE_ASCII)
    check_puid(safe_ascii_id, 58.43, 6.49, 9, 0.81, Charsets.SAFE_ASCII)


def test_wordSafe32(util):
    wordSafe32_bytes = util.fixed_bytes("d2 e3 e9 da 19 03 b7 3c")
    wordSafe32_id = Puid(bitwidth=20,
                         charset=Charsets.WORD_SAFE32,
                         entropy_source=wordSafe32_bytes)
    assert wordSafe32_id.generate() == "pHVw"
    assert wordSafe32_id.generate() == "XgRm"
    assert wordSafe32_id.generate() == "2PqX"


def test_unicode_chars(util):
    unicode_bytes = util.fixed_bytes(
        'ec f9 db 7a 33 3d 21 97 a0 c2 bf 92 80 dd 2f 57 12 c1 1a ef')
    unicode_id = Puid(bitwidth=24,
                      charset='dîngøsky:￦',
                      entropy_source=unicode_bytes)

    assert unicode_id.generate() == '￦gî￦￦nî￦'
    assert unicode_id.generate() == 'ydkîsnsd'
    assert unicode_id.generate() == 'îøsîndøk'
    pass


def test_256_chars():
    single_byte = Charsets.SAFE64.value

    double_start = 256
    double_byte = "".join([chr(n + double_start) for n in range(128)])

    triple_start = 19904
    triple_byte = "".join([chr(n + triple_start) for n in range(64)])

    chars = single_byte + double_byte + triple_byte
    id = Puid(charset=chars)

    assert len(id.generate()) == len(id)
    assert id.bits_per_char == 8
    assert id._ere == 0.5


def test_repr():
    rand_id = Puid()
    assert isinstance(repr(rand_id), str)
