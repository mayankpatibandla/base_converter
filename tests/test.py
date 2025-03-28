"""Test cases for baseconvert.exe"""

import subprocess
from dataclasses import dataclass

EXE = "./baseconvert.exe"


@dataclass
class TestCase:
    """Test case for base conversion.

    :param input: Input string to convert.
    :type input: str
    :param expected: Expected output string.
    :type expected: str
    :param base_to: Base to convert to.
    :type base_to: int
    :param nbits: Number of bits to use for conversion (default is 8).
    :type nbits: int
    """

    input: str
    expected: str
    base: int
    nbits: int = 8


def run_test(case: TestCase) -> None:
    """Run a test case.

    :param case: Test case to run.
    :type case: TestCase
    :raises AssertionError: If the test case fails.
    :rtype: None
    """

    args = EXE, case.input, str(case.base), str(case.nbits), ""
    process = subprocess.run(args, capture_output=True, text=True, check=False)
    output = process.stdout.strip()

    try:
        assert process.returncode == 0, f"Process failed for {case}"
        result = output.splitlines()[-1]
        assert result == case.expected, f"Test failed for {case}, got {result}"
    except AssertionError:
        print(output)
        print(process.stderr.strip())
        raise


test_cases = [
    # Test cases for binary conversion
    TestCase("0b11111111", "11111111", 2),
    TestCase("0b11111111", "255", 10),
    TestCase("0b11111111", "FF", 16),
    TestCase("-0b00000001", "11111111", 2),
    TestCase("-0b00000001", "-1", 10),
    TestCase("-0b00000001", "FF", 16),
    # Test cases for decimal conversion
    TestCase("255", "11111111", 2),
    TestCase("255", "255", 10),
    TestCase("255", "FF", 16),
    TestCase("-1", "11111111", 2),
    TestCase("-1", "-1", 10),
    TestCase("-1", "FF", 16),
    # Test cases for hexadecimal conversion
    TestCase("0xFF", "11111111", 2),
    TestCase("0xFF", "255", 10),
    TestCase("0xFF", "FF", 16),
    TestCase("-0x1", "11111111", 2),
    TestCase("-0x1", "-1", 10),
    TestCase("-0x1", "FF", 16),
    # Additional test cases
    TestCase("0b00000000", "0", 10),
    TestCase("0", "00000000", 2),
    TestCase("0", "00", 16),
    TestCase("42", "00101010", 2),
    TestCase("-0x2a", "-42", 10),
    TestCase("0b101010", "42", 10),
    TestCase("0x2A", "00101010", 2),
    TestCase("127", "01111111", 2, 8),
    TestCase("128", "10000000", 2, 8),
    TestCase("-128", "10000000", 2, 8),
    TestCase("-1", "FFFFFFFF", 16, 32),
    TestCase("1", "01", 16, 8),
]

test_cases += [TestCase(hex(i), str(i), 10) for i in range(0xFF)]
test_cases += [TestCase(str(i), hex(i)[2:].zfill(2).upper(), 16) for i in range(0xFF)]
test_cases += [TestCase(bin(i), str(i), 10) for i in range(0xFF)]
test_cases += [TestCase(str(i), bin((i + (1 << 8)) & ((1 << 8) - 1))[2:].zfill(8), 2) for i in range(-0x80, 0)]

if __name__ == "__main__":
    for test_case in test_cases:
        run_test(test_case)
    print("All tests passed.")
