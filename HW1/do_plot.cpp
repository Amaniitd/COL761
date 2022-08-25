#include "apriori.h"
#include "fptree.h"

int main(int a, char *args[])
{
    double st = CT();
    string infile = args[1];
    int thr = stoi(args[2]);
    string cmd = args[3];
    if (cmd == "-apriori"){
        doApriori(infile, thr);
    }else{
        doFptree(infile, thr);
    }
    double en = CT();
    cout << en - st << endl;
}
