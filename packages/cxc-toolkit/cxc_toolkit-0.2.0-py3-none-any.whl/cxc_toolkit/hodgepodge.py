import re


def xor_bytes(bytes_1, bytes_2, longest=False):
    """
    Xor bytes_1 and bytes_2, return the result as a bytes

    :param bytes_1:
    :param bytes_2:
    :type ytes_1: bytes
    :type bytes_2: bytes
    :return:
    :rtype: bytes
    """
    # init variables
    bytearray_1 = bytearray(bytes_1)
    bytearray_2 = bytearray(bytes_2)
    xor_bytearray = bytearray()

    # make bytearray_1 be the longest bytearray
    if len(bytearray_1) < len(bytearray_2):
        bytearray_1, bytearray_2 = bytearray_2, bytearray_1

    for i in range(len(bytearray_1)):
        if i < len(bytearray_2):
            xor_bytearray.append(bytearray_1[i] ^ bytearray_2[i])
        else:
            if longest:
                xor_bytearray += bytearray_1[i:]
            break
    return bytes(xor_bytearray)


def xor_hex(hex_1, hex_2, longest=False):
    """
    Xor hex_1 and hex_2, return the result as a hex

    :param hex_1: string represent of a hex
    :param hex_2: string represent of another hex
    :type hex_1: str
    :type hex_2: str
    :return: xor of hex_1 and hex_2 and present as string
    :rtype: str
    """
    # init variable
    xor_hex = ""

    # make hex_1 be the longer string
    if len(hex_1) < len(hex_2):
        hex_1, hex_2 = hex_2, hex_1

    for i in range(len(hex_1)):
        if i < len(hex_2):
            xor_hex += "{:x}".format(int(hex_1[i], 16) ^ int(hex_2[i], 16))
        else:
            if longest:
                xor_hex += hex_1[i:]
            break
    return xor_hex


def is_word(c):
    """
    Determine if character c is word.
    Word means in set {a-z, A-Z, 0-9, "_"}

    :param c:
    :type c: str/bytes
    :return:
    :rtype: bool
    """
    if len(c) != 1:
        raise ValueError("c must be a string with length 1")

    if isinstance(c, bytes):
        c = c.decode("ascii", errors="ignore")

    regex = r"^\w$"
    pattern = re.compile(regex)
    match = pattern.match(c)
    return bool(match)


def is_normal_character(c):
    """
    Determine if character c is normal character.
    Normal character means in set {word, space, ",", "."}

    :param c:
    :type c: str/bytes
    :return:
    :rtype: bool
    """
    if isinstance(c, bytes):
        c = c.decode("ascii", errors="ignore")

    if is_word(c) or c.isspace() or c in ",.":
        return True
    return False
