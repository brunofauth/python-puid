import os
from collections import namedtuple

import pytest

from puid import Charsets
from puid import Puid


class Util:
    Params = namedtuple('Params',
                        'bin_file mod_name total risk chars ids_count')

    @staticmethod
    def fixed_bytes(hex_string):
        return Util.static_bytes_fn(bytearray.fromhex(hex_string))

    @staticmethod
    def file_bytes(bin_file):
        with open(bin_file, 'rb') as file:
            return Util.static_bytes_fn(bytearray(file.read()))

    @staticmethod
    def static_bytes_fn(bytes):
        offset = 0

        def get_bytes(n_bytes):
            nonlocal offset
            offset_bytes = bytes[offset:offset + n_bytes]
            offset += n_bytes
            return offset_bytes

        return get_bytes

    @staticmethod
    def data_path(data_name, file_name):
        return os.path.join(os.getcwd(), 'tests', 'data', data_name, file_name)

    @staticmethod
    def params(data_name):
        params_path = os.path.join(Util.data_path(data_name, 'params'))
        with open(params_path, 'r') as file:

            def next_param():
                return file.readline().strip()

            bin_file = Util.data_path('', next_param())
            test_name = next_param()
            total = int(next_param())
            risk = float(next_param())

            chars = Util.chars_param(next_param())
            count = int(next_param())

            return Util.Params(bin_file, test_name, total, risk, chars, count)

    @staticmethod
    def chars_param(param):
        chars_type, chars_def = param.split(':')
        if chars_type == 'predefined':
            return Util.predefined(chars_def)
        elif chars_type == 'custom':
            return chars_def
        else:
            raise ValueError('params file has invalid chars def:', param)

    @staticmethod
    def predefined(name):
        if name == 'alpha':
            return Charsets.ALPHA
        if name == 'alpha_lower':
            return Charsets.ALPHA_LOWER
        if name == 'alpha_upper':
            return Charsets.ALPHA_UPPER
        if name == 'alphanum':
            return Charsets.ALPHANUM
        if name == 'alphanum_lower':
            return Charsets.ALPHANUM_LOWER
        if name == 'alphanum_upper':
            return Charsets.ALPHANUM_UPPER
        if name == 'base16':
            return Charsets.BASE16
        if name == 'base32':
            return Charsets.BASE32
        if name == 'base32_hex':
            return Charsets.BASE32_HEX
        if name == 'base32_hex_upper':
            return Charsets.BASE32_HEX_UPPER
        if name == 'crockford32':
            return Charsets.CROCKFORD32
        if name == 'decimal':
            return Charsets.DECIMAL
        if name == 'hex':
            return Charsets.HEX
        if name == 'hex_upper':
            return Charsets.HEX_UPPER
        if name == 'safe_ascii':
            return Charsets.SAFE_ASCII
        if name == 'safe32':
            return Charsets.SAFE32
        if name == 'safe64':
            return Charsets.SAFE6
        if name == 'symbol':
            return Charsets.SYMBOL
        if name == 'word_safe32':
            return Charsets.WORD_SAFE32

        return None

    @staticmethod
    def rand_id_mod(dir_name):
        params = Util.params(dir_name)
        rand_bytes = Util.file_bytes(params.bin_file)
        return Puid(total=params.total,
                    risk=params.risk,
                    charset=params.chars,
                    entropy_source=rand_bytes)

    @staticmethod
    def test_data(data_name):
        rand_id = Util.rand_id_mod(data_name)
        ids_file = Util.data_path(data_name, 'ids')

        with open(ids_file) as ids:
            for id in ids:
                assert rand_id.generate() == id.strip()


@pytest.fixture
def util():
    return Util
