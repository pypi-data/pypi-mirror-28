import unittest

from cxc_toolkit.hodgepodge import (xor, utf8_to_hex,
                                    hex_to_utf8,
                                    )


class TestHodgepodge(unittest.TestCase):

    def test_xor(self):
        xor_hex = xor("12ab", "fac0")
        assert xor_hex == "e86b"
        hex_1 = "135af170b8c9"
        hex_2 = "c1879ab9010a34f"
        xor_hex = "d2dd6bc9b9c334f"
        assert xor_hex == xor(hex_1, hex_2)
        assert xor_hex == xor(hex_2, hex_1)

    def test_utf8_to_hex(self):
        string = "123"
        hex_string = "313233"
        assert utf8_to_hex(string) == hex_string
        assert string == hex_to_utf8(hex_string)
        string = "az9?"
        hex_string = "617a393f"
        assert utf8_to_hex(string) == hex_string
        assert string == hex_to_utf8(hex_string)
        string = "崔晓晨"
        hex_string = "e5b494e69993e699a8"
        assert utf8_to_hex(string) == hex_string
        assert string == hex_to_utf8(hex_string)
        string = "\\xff\\xff"
        hex_string = "ffff"
        assert string == hex_to_utf8(hex_string)
