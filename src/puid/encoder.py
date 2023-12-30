from __future__ import annotations

import typing
from collections.abc import Callable

from puid.chars import Charsets, Charset
from puid.encoders.alpha import alpha
from puid.encoders.alpha import alpha_lower
from puid.encoders.alpha import alpha_upper
from puid.encoders.alphanum import alphanum
from puid.encoders.alphanum import alphanum_lower
from puid.encoders.alphanum import alphanum_upper
from puid.encoders.base16 import base16
from puid.encoders.base32 import base32
from puid.encoders.base32 import base32_hex
from puid.encoders.base32 import base32_hex_upper
from puid.encoders.crockford32 import crockford32
from puid.encoders.decimal import decimal
from puid.encoders.hex import hex_lower
from puid.encoders.hex import hex_upper
from puid.encoders.safe32 import safe32
from puid.encoders.safe64 import safe64
from puid.encoders.safe_ascii import safe_ascii
from puid.encoders.symbol import symbol
from puid.encoders.word_safe32 import word_safe32

from puid.encoders.custom import custom

Encoder = Callable[[int], int]
EncoderFactory = Callable[[], Encoder]

_ENCODERS: dict[Charsets, EncoderFactory] = {
    Charsets.ALPHA: alpha,
    Charsets.ALPHA_LOWER: alpha_lower,
    Charsets.ALPHA_UPPER: alpha_upper,
    Charsets.ALPHANUM: alphanum,
    Charsets.ALPHANUM_LOWER: alphanum_lower,
    Charsets.ALPHANUM_UPPER: alphanum_upper,
    Charsets.BASE16: base16,
    Charsets.BASE32: base32,
    Charsets.BASE32_HEX: base32_hex,
    Charsets.BASE32_HEX_UPPER: base32_hex_upper,
    Charsets.CROCKFORD32: crockford32,
    Charsets.DECIMAL: decimal,
    Charsets.HEX: hex_lower,
    Charsets.HEX_UPPER: hex_upper,
    Charsets.SAFE32: safe32,
    Charsets.SAFE64: safe64,
    Charsets.SAFE_ASCII: safe_ascii,
    Charsets.SYMBOL: symbol,
    Charsets.WORD_SAFE32: word_safe32,
}


def get_encoder(charset: Charset) -> Encoder:
    match charset.kind:
        case Charsets.CUSTOM:
            return custom(charset.characters)
        case other:
            return _ENCODERS[other]()
