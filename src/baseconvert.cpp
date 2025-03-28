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

  bool is_signed = value.compare(0, 2, "-0") == 0;
  if (is_signed) {
    value.erase(0, 2);
  } else if (value.compare(0, 1, "0") == 0) {
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

  std::uint64_t max_value = 1ULL << nbits;

  bool is_negative = is_signed && result & (1ULL << (nbits - 1));
  if (is_negative) {
    result -= max_value;
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

  std::cout << "Value: " << value << std::endl;
  std::cout << "Base: " << base << std::endl;
  std::cout << "Nbits: " << nbits << std::endl;
  std::cout << "Signed: " << (is_signed ? "true" : "false") << std::endl;
  std::cout << "Result: " << result << std::endl;
  std::cout << "Max value: " << max_value << std::endl;
  std::cout << "Is negative: " << (is_negative ? "true" : "false") << std::endl;
  std::cout << "Output: " << output << std::endl;
  std::cout << "Output size: " << output.size() << std::endl;

  std::size_t fill_size = nbits / std::ceil(std::log2(base));
  if (output.size() > fill_size) {
    output.erase(output.find_first_not_of('-'),
                 output.size() - nbits / std::floor(std::log2(base)));
    // output.insert(0, fill_size - output.size(), '0');
  }

  std::cout << output << std::endl;

  return 0;
}