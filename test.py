"""Test cases for baseconvert.exe"""

import subprocess
from dataclasses import dataclass

EXE = "baseconvert.exe"


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
        assert process.returncode == 0, f"Process failed with return code {process.returncode}"
        result = output.splitlines()[-1]
        assert result == case.expected, f"Test failed for {case}, got {result}"
    except AssertionError:
        print(output)
        raise


test_cases = (
    # Test cases for binary  conversion
    TestCase("0b11111111", "11111111", 2),
    TestCase("0b11111111", "255", 10),
    TestCase("0b11111111", "FF", 16),
    TestCase("-0b11111111", "11111111", 2),
    TestCase("-0b11111111", "-1", 10),
    TestCase("-0b11111111", "FF", 16),
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
    TestCase("-0xFF", "11111111", 2),
    TestCase("-0xFF", "-1", 10),
    TestCase("-0xFF", "FF", 16),
)


if __name__ == "__main__":
    for test_case in test_cases:
        run_test(test_case)
    print("All tests passed.")
