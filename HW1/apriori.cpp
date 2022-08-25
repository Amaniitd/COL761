#include "apriori.h"

int main(int a, char *args[])
{
    double st = CT();
    string infile = args[1];
    string otfile = args[3];
    int thr = stoi(args[2]);
    doApriori(infile, thr);
    set<set<string>>::iterator fi;
    ofile.open(otfile, ios::out);
    for (fi = itemsets.begin(); fi != itemsets.end(); ++fi)
    {
        set<string> temp = *fi;
        set<string>::iterator op;

        if (fi != itemsets.begin())
        {
            ofile << "\n";
        }

        for (op = temp.begin(); op != temp.end(); ++op)
        {
            if (op != temp.begin())
            {
                ofile << " ";
            }
            ofile << *op;
        }
    }

    double en = CT();
    cout << en - st << endl;
    ofile.close();
    return 0;
}
