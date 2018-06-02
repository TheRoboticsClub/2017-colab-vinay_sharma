#include <boost/property_tree/xml_parser.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/foreach.hpp>
#include <iostream>

int main() {

    boost::property_tree::ptree root;
    try {
     boost::property_tree::read_xml("hierarchy.xml", root);
    }
    catch(std::exception & e)
     {
         std::cout << "caught exception" << '\n';
     }


     boost::property_tree::ptree::const_assoc_iterator i_pts = root.find("class");
     if(root.not_found() != i_pts) {
       const boost::property_tree::ptree & pts = (*i_pts).second;
       std::cout << "found" << '\n';
     }

}


/*

Test if a node have children
if(!node.empty())
	{
	// do something
	}
Iterate on any children of a node
// tree is a boost::property_tree::ptree
BOOST_FOREACH(  boost::property_tree::ptree::value_type const&v, tree ) {
	// v.first is the key
	if(v.second.empty()) {
		// normal key:value
		// use subtree.data() as string value or subtree.get_value<T>()
	} else {
		// subtree
		//  use v.second as child
	}
}
// iterate on children (example array)
BOOST_FOREACH(  boost::property_tree::ptree::value_type const&v, tree.get_child("children") ) {
	const std::string & key = v.first; // key
	const boost::property_tree::ptree & subtree = v.second; // value (or a subnode)
	if(subtree.empty()) {
		// This is a key:value
		//  use subtree.data() as string value or subtree.get_value<T>()
	} else {
		// This is a subtree
		//  use subtree as child
	}
}
// or without BOOST_FOREACH
for(boost::property_tree::ptree::const_iterator v = tree.begin(); v != tree.end(); ++v) {
	float value = v->second.get_value<float>();
}
Add or replace an unique element to a property vector
tree.put("name", value);
tree.put<int>("version", 1);
Add multiple element to a property vector
 tree.add("path", "value1");
 tree.add("path", "value2");

In JSON this code does not create a "vector"
Add a treenode to a property tree
boost::property_tree::ptree elem;
// fill elem
ptree_parent.push_back( std::make_pair("key", elem ) );
Add an element to a property vector
boost::property_tree::ptree elem;
// fill elem
ptree_parent.push_back( std::make_pair("", elem ) );
ptree_parent.add_child( "key", elem );

Add or replace an element in a property tree
ptree_parent.put_child("name", elem);

*/
