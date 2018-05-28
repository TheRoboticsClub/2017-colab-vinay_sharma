#include "rapidjson_1/document.h"
#include "rapidjson_1/stringbuffer.h"
#include "single_json/json.hpp"
#include <stdio.h>
#include <iostream>
#include <sstream>
#include <fstream>

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

rapidjson::Document doc;

clock_t begin_time = clock();

cout << "Starting Timer" << endl;
// do something

if (doc.Parse<0>(ss.str().c_str()).HasParseError())
  throw std::invalid_argument("json parse error");



if (doc.Parse<0>(ss.str().c_str()).HasParseError())
        throw std::invalid_argument("json parse error");

    if(!doc.HasMember("annotations"))
        throw std::invalid_argument("Invalid Annotations file Passed");

    const rapidjson::Value& a = doc["annotations"];

    if(!a.IsArray())
        throw std::invalid_argument("Invalid Annotations file Passed");

    for (rapidjson::Value::ConstValueIterator itr = a.Begin(); itr != a.End(); ++itr)
        std::cout << (*itr)["area"].GetDouble() << '\n';




cout << float( clock () - begin_time ) /  CLOCKS_PER_SEC;


cout << "here"  << endl;


if (doc.HasMember("annotations")) {
cout << "hello" << endl;

}


std::ifstream newfile("/opt/datasets/coco/annotations/instances_train2014.json");

begin_time = clock();


nlohmann::json j;
j = nlohmann::json::parse(newfile);

std::cout << float( clock () - begin_time ) /  CLOCKS_PER_SEC;


cout << "Done" << endl;


}
