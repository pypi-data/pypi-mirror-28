import unittest

from cxc_toolkit.hodgepodge import (xor, string_to_hex,
                                    hex_to_string,
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

    def test_string_to_hex(self):
        string = "123"
        hex_string = "313233"
        assert string_to_hex(string) == hex_string
        assert string == hex_to_string(hex_string)
        string = "az9?"
        hex_string = "617a393f"
        assert string_to_hex(string) == hex_string
        assert string == hex_to_string(hex_string)
        string = "崔晓晨"
        hex_string = "e5b494e69993e699a8"
        assert string_to_hex(string) == hex_string
        assert string == hex_to_string(hex_string)
