#include <iostream>

int main() {

std::int someInt = 45;

std::string output = someInt.ToString(new std::string('0', 12));

std::cout << output << '\n';

}
