def xor(hex_1, hex_2):
    """
    Xor hex_1 and hex_2, return the result as a hex

    :param hex_1: string represent of a hex
    :param hex_2: string represent of another hex
    :type hex_1: string
    :type hex_2: string
    :return: xor of hex_1 and hex_2 and present as string
    :rtype: string
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
            xor_hex += hex_1[i:]
            break
    return xor_hex
