#include "fptree.h"


int main(int argc, char **argv)
{
    string filename = argv[1];
    int percent_support = atoi(argv[2]);
    doFptree(filename, percent_support);
    string output_file = argv[3];
    ofstream ofs(output_file);
    for (auto &itemset : tree->frequent_itemsets)
    {
        for (auto &itr : itemset)
        {
            ofs << itr << ' ';
        }
        ofs << endl;
    }
    ofs.close();
}