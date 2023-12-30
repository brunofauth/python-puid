from __future__ import annotations

import dataclasses as dc
import secrets
from math import ceil, log2
from collections.abc import Callable
from typing import Any, assert_never

import puid.chars
from puid.chars import Charsets, Charset, is_valid_charset
from puid.bits import muncher
from puid.chars_error import InvalidChars
from puid.encoder import get_encoder
from puid.entropy import bits_for_total_risk
from puid.puid_error import BitsError, TotalRiskError


@dc.dataclass(slots=True, init=False)
class Puid:
    bitwidth: float = 128
    charset: Charset = dc.field(init=False)
    bits_per_char: float = dc.field(init=False)
    _len_in_chars: int = dc.field(init=False)

    _bits_muncher: Any = dc.field(init=False)
    _encoded: Any = dc.field(init=False)
    _ere: Any = dc.field(init=False)

    @classmethod
    def from_risk(
        cls,
        total: int,
        risk: float,
        charset: Charsets | str = Charsets.SAFE64,
        entropy_source: Callable[[int | None], bytes] = secrets.token_bytes,
    ) -> Puid:
        return cls(
            bitwidth=bits_for_total_risk(total, risk),
            charset=charset,
            entropy_source=entropy_source,
        )

    def __init__(
        self,
        bitwidth: float = 128,
        charset: Charsets | str = Charsets.SAFE64,
        entropy_source: Callable[[int | None], bytes] = secrets.token_bytes,
    ) -> None:
        if bitwidth <= 0:
            raise BitsError("bits must be a positive integer")

        # yapf: disable
        match charset:
            case puid.chars.Charsets() as charset:
                self.charset = Charset.predefined(kind=charset)
            case str(chars):
                self.charset = Charset.custom(characters=chars)
            case unreachable:
                assert_never(unreachable)
        # yapf: enable

        n_chars = len(self.charset.characters)
        self.bits_per_char = log2(n_chars)
        self._len_in_chars = int(ceil(bitwidth / self.bits_per_char))
        self.bitwidth = self._len_in_chars * self.bits_per_char

        self._bits_muncher = muncher(n_chars, self._len_in_chars,
                                     entropy_source)
        chars_encoder = get_encoder(self.charset)

        def encoded(values):
            return [chr(chars_encoder(value)) for value in values]

        self._encoded = encoded
        self._ere = (self.bits_per_char * n_chars) / (
            8 * len(self.charset.characters.encode('utf-8')))

    def __len__(self) -> int:
        return self._len_in_chars

    def generate(self):
        values = self._bits_muncher()
        return "".join(self._encoded(values))
