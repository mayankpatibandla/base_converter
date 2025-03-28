import sys


def str_to_unsigned(value: str, base: int) -> bytearray:
    """
    Convert a string representation of a number to an unsigned byte array.

    :param value: The number to convert (as a string).
    :param base: The base of the number (2, 8, 10, or 16).
    :return: The byte array representation of the number.
    """
    assert base in (2, 8, 10, 16), "Base must be one of: 2, 8, 10, 16"
    value = value.replace("_", "")
    signed = value.startswith("-0")
    if signed:
        value = value[2:]
    elif value.startswith("0"):
        value = value[1:]
    if not value:
        val = 0
    elif value.startswith("b"):
        val = int(value[1:], 2)
    elif value.startswith("o"):
        val = int(value[1:], 8)
    elif value.startswith("x"):
        val = int(value[1:], 16)
    else:
        val = int(value, 10)

    return bytearray(val.to_bytes((val.bit_length() + 7) // 8, "big"))


def convert_tobase(value: str, nbits: int = 32, base: int = 16) -> str:
    """
    Convert a number to a specified base.

    :param value: The number to convert (as a string).
    :param signed: Whether the number is signed (default is False).
    :param nbits: The number of bits (default is 32).
    :param base: The base to convert to (default is 16).
    :return: The converted number as a string.
    """
    assert base in (2, 8, 10, 16), "Base must be one of: 2, 8, 10, 16"
    value = value.replace("_", "")
    signed = value.startswith("-0")
    if signed:
        value = value[2:]
    elif value.startswith("0"):
        value = value[1:]
    if not value:
        val = 0
    elif value.startswith("b"):
        val = int(value[1:], 2)
    elif value.startswith("o"):
        val = int(value[1:], 8)
    elif value.startswith("x"):
        val = int(value[1:], 16)
    else:
        val = int(value, 10)

    if signed and val & (1 << (nbits - 1)):
        # print(f"Negative value detected: {val}")
        val -= 1 << nbits
    result = (val + (2**nbits)) % (2**nbits)
    if base == 2:
        return bin(result)[2:].zfill(nbits)
    if base == 8:
        return oct(result)[2:].zfill(nbits // 3)
    if base == 10:
        if signed and val & (1 << (nbits - 1)):
            result = -result
        return str(result).zfill(nbits // 3)
    if base == 16:
        return hex(result)[2:].upper().zfill(nbits // 4)


def test_convert_tobase(expected: str, value: str, nbits: int = 32, base: int = 16) -> None:
    """
    Test the convert_tobase function.

    :param expected: The expected output.
    :param value: The input value to convert.
    :param nbits: The number of bits.
    :param base: The base to convert to.
    """
    result = convert_tobase(value, nbits, base)
    assert result == expected, f"Expected {expected}, but got {result}"
    print(f"Test passed for value {value}: {result} == {expected}")


def main():
    """
    Main function to run the script from the command line.
    """
    assert len(sys.argv) > 1, "Usage: python test.py <value> <nbits> <base>"
    value = sys.argv[1]
    nbits = int(sys.argv[2]) if len(sys.argv) > 2 else 32
    base = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    print(convert_tobase(value, nbits, base))


def test():
    """
    Run the test cases for the convert_tobase function.
    """
    # Test cases
    test_convert_tobase("00000000", "0")
    test_convert_tobase("00000001", "1")
    test_convert_tobase("00000002", "2")
    test_convert_tobase("00000003", "3")
    test_convert_tobase("00000004", "4")
    test_convert_tobase("00000005", "5")
    test_convert_tobase("00000006", "6")
    test_convert_tobase("00000007", "7")
    test_convert_tobase("00000008", "8")
    test_convert_tobase("00000009", "9")
    test_convert_tobase("0000000A", "10")
    test_convert_tobase("0000000B", "11")
    test_convert_tobase("0000000C", "12")
    test_convert_tobase("0000000D", "13")
    test_convert_tobase("0000000E", "14")
    test_convert_tobase("0000000F", "15")

    # Test signed numbers
    test_convert_tobase("FFFFFFF0", "-16")
    test_convert_tobase("FFFFFFF1", "-15")
    test_convert_tobase("FFFFFFF2", "-14")
    test_convert_tobase("FFFFFFF3", "-13")
    test_convert_tobase("FFFFFFF4", "-12")
    test_convert_tobase("FFFFFFF5", "-11")
    test_convert_tobase("FFFFFFF6", "-10")
    test_convert_tobase("FFFFFFF7", "-9")
    test_convert_tobase("FFFFFFF8", "-8")
    test_convert_tobase("FFFFFFF9", "-7")
    test_convert_tobase("FFFFFFFA", "-6")
    test_convert_tobase("FFFFFFFB", "-5")
    test_convert_tobase("FFFFFFFC", "-4")
    test_convert_tobase("FFFFFFFD", "-3")
    test_convert_tobase("FFFFFFFE", "-2")
    test_convert_tobase("FFFFFFFF", "-1")
    test_convert_tobase("00000000", "-0")

    # Test nbits = 4 and base = 2
    test_convert_tobase("0000", "0", nbits=4, base=2)
    test_convert_tobase("0001", "1", nbits=4, base=2)
    test_convert_tobase("0010", "2", nbits=4, base=2)
    test_convert_tobase("0011", "3", nbits=4, base=2)
    test_convert_tobase("0100", "4", nbits=4, base=2)
    test_convert_tobase("0101", "5", nbits=4, base=2)
    test_convert_tobase("0110", "6", nbits=4, base=2)
    test_convert_tobase("0111", "7", nbits=4, base=2)
    test_convert_tobase("1000", "8", nbits=4, base=2)
    test_convert_tobase("1001", "9", nbits=4, base=2)
    test_convert_tobase("1010", "10", nbits=4, base=2)
    test_convert_tobase("1011", "11", nbits=4, base=2)
    test_convert_tobase("1100", "12", nbits=4, base=2)
    test_convert_tobase("1101", "13", nbits=4, base=2)
    test_convert_tobase("1110", "14", nbits=4, base=2)
    test_convert_tobase("1111", "15", nbits=4, base=2)

    # Test signed numbers with nbits = 4 and base = 2
    test_convert_tobase("1100", "-4", nbits=4, base=2)
    test_convert_tobase("1101", "-3", nbits=4, base=2)
    test_convert_tobase("1110", "-2", nbits=4, base=2)
    test_convert_tobase("1111", "-0b1111", nbits=4, base=2)
    test_convert_tobase("0000", "-0", nbits=4, base=2)


if __name__ == "__main__":
    main()
    # test()
