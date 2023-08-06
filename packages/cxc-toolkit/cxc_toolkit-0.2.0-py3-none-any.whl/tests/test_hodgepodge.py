import unittest

from cxc_toolkit.hodgepodge import (xor_bytes,
                                    xor_hex,
                                    is_word,
                                    is_normal_character,
                                    )


class TestHodgepodge(unittest.TestCase):

    def test_xor_bytes(self):
        bytes_1 = b"h3ib"
        bytes_2 = b"wkmn"
        xor_shortest_hex = "1f58040c"
        xor_longest_hex = xor_shortest_hex
        assert xor_shortest_hex == xor_bytes(bytes_1, bytes_2).hex()
        assert xor_shortest_hex == xor_bytes(bytes_2, bytes_1).hex()
        assert xor_longest_hex == xor_bytes(bytes_1, bytes_2,
                                            longest=True).hex()
        assert xor_longest_hex == xor_bytes(bytes_2, bytes_1,
                                            longest=True).hex()

        bytes_1 = b"1\".# s_hi+"
        bytes_2 = b"@w-ch`~ss123&&"
        xor_shortest_hex = "715503404813211b1a1a"
        xor_longest_hex = "715503404813211b1a1a32332626"
        assert xor_shortest_hex == xor_bytes(bytes_1, bytes_2).hex()
        assert xor_shortest_hex == xor_bytes(bytes_2, bytes_1).hex()
        assert xor_longest_hex == xor_bytes(bytes_1, bytes_2,
                                            longest=True).hex()
        assert xor_longest_hex == xor_bytes(bytes_2, bytes_1,
                                            longest=True).hex()

    def test_xor_hex(self):
        xor_shortest_hex = xor_hex("12ab", "fac0")
        assert xor_shortest_hex == "e86b"
        hex_1 = "135af170b8c9"
        hex_2 = "c1879ab9010a34f"
        xor_shortest_hex = "d2dd6bc9b9c3"
        xor_longest_hex = "d2dd6bc9b9c334f"
        assert xor_shortest_hex == xor_hex(hex_1, hex_2)
        assert xor_shortest_hex == xor_hex(hex_2, hex_1)
        assert xor_longest_hex == xor_hex(hex_1, hex_2, longest=True)
        assert xor_longest_hex == xor_hex(hex_2, hex_1, longest=True)

    def test_is_word(self):
        assert is_word("a")
        assert is_word("C")
        assert is_word("1")
        assert is_word("0")
        assert is_word("_")

        assert is_word(b"1")
        assert is_word(b"a")
        assert is_word(b"_")

        assert not is_word(";")
        assert not is_word("\\")
        assert not is_word(" ")

        assert not is_word(b";")
        assert not is_word(b"\\")
        assert not is_word(b" ")

        with self.assertRaises(ValueError):
            is_word("hi")

    def test_is_normal_character(self):
        assert is_normal_character("a")
        assert is_normal_character(" ")
        assert is_normal_character(".")
        assert is_normal_character("\n")

        assert is_normal_character(b"a")
        assert is_normal_character(b" ")

        assert not is_normal_character("@")
        assert not is_normal_character("\\")

        assert not is_normal_character(b"@")
        assert not is_normal_character(b"\\")
