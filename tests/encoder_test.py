from puid.chars import Charsets, Charset
from puid.encoder import get_encoder


def encoder_chars(chars: Charsets) -> None:
    charset = Charset.predefined(chars)
    chars_encoder = get_encoder(charset)
    encoded = "".join([chr(chars_encoder(code)) for code in range(len(chars))])
    assert encoded == charset.characters


def test_encoders():
    encoder_chars(Charsets.ALPHA)
    encoder_chars(Charsets.ALPHA_LOWER)
    encoder_chars(Charsets.ALPHA_UPPER)
    encoder_chars(Charsets.ALPHANUM)
    encoder_chars(Charsets.ALPHANUM_LOWER)
    encoder_chars(Charsets.ALPHANUM_UPPER)
    encoder_chars(Charsets.BASE16)
    encoder_chars(Charsets.BASE32)
    encoder_chars(Charsets.BASE32_HEX)
    encoder_chars(Charsets.BASE32_HEX_UPPER)
    encoder_chars(Charsets.CROCKFORD32)
    encoder_chars(Charsets.DECIMAL)
    encoder_chars(Charsets.HEX)
    encoder_chars(Charsets.HEX_UPPER)
    encoder_chars(Charsets.SAFE_ASCII)
    encoder_chars(Charsets.SAFE32)
    encoder_chars(Charsets.SAFE64)
    encoder_chars(Charsets.SYMBOL)
    encoder_chars(Charsets.WORD_SAFE32)
