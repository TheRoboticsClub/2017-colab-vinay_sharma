#include <iostream>
#include <map>

int main() {

std::map<std::string, int> my_map;
std::map<std::string, int>::iterator it;

my_map.insert(std::make_pair("bottle", 10));
my_map.insert(std::make_pair("cup", 20));
my_map.insert(std::make_pair("jar", 5));
my_map.insert(std::make_pair("person", 30));
my_map.insert(std::make_pair("rat", 2));
my_map.insert(std::make_pair("zebra", 15));

it = my_map.find("jar");


if (it != my_map.end()) {
	std::cout << it->second << '\n';
}

}
