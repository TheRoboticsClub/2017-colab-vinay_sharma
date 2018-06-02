#include "tree.h"

int main() {

    Tree root;

    root = Tree("hierarchy.xml");


    //root.printClassName();

    Tree* myresult;

    root.printChildrenRecursive();

    std::vector<std::string> syns = root.getImmediateSynonmys("airplane");

    std::vector<std::string>::iterator itr;

    if (!syns.empty()) {
        for (itr = syns.begin(); itr != syns.end(); itr++) {
            std::cout << *itr << '\n';
        }
    }
}
