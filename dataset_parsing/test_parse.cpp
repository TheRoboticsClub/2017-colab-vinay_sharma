#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>

int main() {
// Create a root

std::cout.precision(17);
boost::property_tree::ptree root;

// Load the json file in this ptree
boost::property_tree::read_json("/opt/datasets/coco/annotations/instances_train2014.json", root);



for (boost::property_tree::ptree::value_type &annotation : root.get_child("annotations"))
{
    // Animal is a std::pair of a string and a child

    // Get the label of the node
    double area = annotation.second.get<double>("area");
    // Get the content of the node

    std::cout << area << std::endl; 
}


}
