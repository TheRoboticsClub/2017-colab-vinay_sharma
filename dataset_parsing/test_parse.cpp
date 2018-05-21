#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>

int main() {
// Create a root
std::cout.precision(17);
boost::property_tree::ptree root;

// Load the json file in this ptree
boost::property_tree::read_json("file.json", root);

// Read values
int height = root.get<int>("height", 0);
// You can also go through nested nodes
std::string msg = root.get<std::string>("some.complex.path");

std::cout << height << '\n';

std::cout << msg << '\n';

// A vector to allow storing our animals
std::vector< std::pair<std::string, std::string> > animals;

// Iterator over all animals
for (boost::property_tree::ptree::value_type &animal : root.get_child("animals"))
{
    // Animal is a std::pair of a string and a child

    // Get the label of the node
    std::string name = animal.first;
    // Get the content of the node
    std::string color = animal.second.data();
    animals.push_back(std::make_pair(name, color));
}

for (boost::property_tree::ptree::value_type &annotation : root.get_child("annotations"))
{
    // Animal is a std::pair of a string and a child

    // Get the label of the node
    double area = annotation.second.get<double>("area");
    // Get the content of the node

    std::cout << "Pi: " << area << std::endl;
}

}
