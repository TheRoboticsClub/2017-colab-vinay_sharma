#include <iostream>
#include <vector>

void append(std::vector<std::string> * v);

int main() {

std::vector<std::string> tobepassed;

tobepassed.push_back("first");
tobepassed.push_back("second");

append(NULL);

for (std::vector<std::string>::const_iterator i = tobepassed.begin(); i != tobepassed.end(); ++i)
    std::cout << *i << '\n';

}


void append(std::vector<std::string> * myvec) {
    if (myvec != NULL)
        myvec->push_back("last");

}
