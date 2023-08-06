import unittest

from cxc_toolkit.hodgepodge import xor


class TestHodgepodge(unittest.TestCase):

    def test_xor(self):
        xor_hex = xor("12ab", "fac0")
        assert xor_hex == "e86b"
        hex_1 = "135af170b8c9"
        hex_2 = "c1879ab9010a34f"
        xor_hex = "d2dd6bc9b9c334f"
        assert xor_hex == xor(hex_1, hex_2)
        assert xor_hex == xor(hex_2, hex_1)
