#include <algorithm>
#include <bitset>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <sstream>
#include <string>

int main(int argc, char *argv[]) {
  if (argc < 3) {
    std::cerr << "Usage: " << argv[0] << " <value> <base> <nbits>" << std::endl;
    return 1;
  }

  std::uint32_t base = std::stoul(argv[2]);
  if (base != 2 && base != 10 && base != 16) {
    std::cerr << "Error: base must be 2, 10, or 16." << std::endl;
    return 1;
  }

  std::uint32_t nbits = 32;
  if (argc > 3) {
    nbits = std::stoul(argv[3]);
    if (nbits < 1 || nbits > 64) {
      std::cerr << "Error: nbits must be between 1 and 64." << std::endl;
      return 1;
    }
  }

  std::string value = argv[1];
  if (value.empty()) {
    std::cerr << "Error: value cannot be empty." << std::endl;
    return 1;
  }

  value.erase(std::remove(value.begin(), value.end(), '_'), value.end());

  bool is_negative = value.compare(0, 1, "-") == 0;
  if (is_negative) {
    value.erase(0, 1);
  }
  if (value.size() > 1 && value.compare(0, 1, "0") == 0) {
    value.erase(0, 1);
  }
  if (value.empty()) {
    std::cerr
        << "Error: value cannot be empty after removing leading characters."
        << std::endl;
    return 1;
  }

  std::int64_t result;
  if (value.compare(0, 1, "b") == 0) {
    result = std::stoull(value.substr(1), nullptr, 2);
  } else if (value.compare(0, 1, "x") == 0) {
    result = std::stoull(value.substr(1), nullptr, 16);
  } else {
    result = std::stoull(value, nullptr, 10);
  }
  if (is_negative) {
    result = -result;
  }

  std::ostringstream oss;
  if (base == 2) {
    oss << std::bitset<64>(result);
  } else if (base == 10) {
    oss << result;
  } else if (base == 16) {
    oss << std::uppercase << std::hex << result;
  }
  std::string output = oss.str();

  // Debugging output
  if (argc > 4) {
    std::cout << "Value: " << value << std::endl;
    std::cout << "Base: " << base << std::endl;
    std::cout << "Nbits: " << nbits << std::endl;
    std::cout << "Result: " << result << std::endl;
    std::cout << "Negative: " << std::boolalpha << is_negative << std::endl;
    std::cout << "Output: " << output << std::endl;
    std::cout << "Output size: " << output.size() << std::endl;
  }

  // Padding
  if (base != 10) {
    std::size_t fill_size = nbits / static_cast<std::size_t>(std::log2(base));
    std::size_t erase_count = output.size() - fill_size;
    if (erase_count > 1 && erase_count < output.size()) {
      output.erase(output.find_first_not_of('-'), erase_count);
    }
    if (output.size() < fill_size) {
      output.insert(0, fill_size - output.size(), '0');
    }
  }

  std::cout << output << std::endl;

  return 0;
}