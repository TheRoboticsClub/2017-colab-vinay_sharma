#include <rapidjson/document.h>
#include <rapidjson/prettywriter.h>
#include <rapidjson/stringbuffer.h>
#include <stdio.h>
#include <iostream>
#include <sstream>
#include <fstream>

using namespace rapidjson;
using namespace std;

int main() {

std::stringstream ss;
std::ifstream infile("/opt/datasets/coco/annotations/instances_train2014.json");


if (infile) {
  ss << infile.rdbuf();
  infile.close();
} 
else {
  throw std::runtime_error("!! Unable to open json file");
}

cout << "here"  << endl;

Document doc;

if (doc.Parse<0>(ss.str().c_str()).HasParseError())
  throw std::invalid_argument("json parse error");




cout << "here"  << endl;


if (doc.HasMember("annotations")) {
cout << "hello" << endl;

}


}
