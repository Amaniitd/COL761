#include<iostream>
#include<string>
#include<fstream>
#include<vector>
#include<map>
using namespace std;

void splitString(string line, char delimiter, vector<string> &v)
{   
    
    string temp = "";
    for (int i = 0; i < line.length(); ++i)
    {

        if (line[i] == delimiter)
        {
            v.push_back(temp);
            temp = "";
        }
        else
        {
            temp.push_back(line[i]);
        }
    }
    v.push_back(temp);
}


void modify_dataset(string filename, string outputfilename){
    int size = 0;
    fstream fi;
    ofstream fo(outputfilename+"modified_dataset");
    fi.open(filename);

    map<string, int> graphid;
    int graphno = 0;
    map<string,int> labelid;
    int labelno = 0;

    if (fi.is_open() && fo.is_open())
    {
        string line;
        while (std::getline(fi, line))
        {   
            if(line.length()==0 || line=="\n" || line==""){
                continue;
            }

            if(line[0] == '#'){
                line.erase(line.begin());
                graphid[line] = graphno++;
                fo << "t # "<<graphid[line]<<endl;

                string temp;
                std::getline(fi, temp);

                int v = stoi(temp);
                if(v<=1){
                    cout<<v<<endl;
                }

                for(int i=0;i<v;++i){
                    std::getline(fi, line);
                    if(labelid.find(line)==labelid.end()){
                        labelid[line] = labelno++;
                    }
                    fo << "v "<<i<<" "<<labelid[line]<<endl;
                }

                std::getline(fi, temp);
                int e = stoi(temp);

                if(e<=1){
                    cout<<e<<endl;
                }

                for(int i=0;i<e;++i){
                    std::getline(fi, line);
                    vector<string> a;
                    splitString(line, ' ', a);
                    fo << "e "<<a[0]<<" "<<a[1]<<" "<<a[2]<<endl;
                }


            }
        
        }
    }

    fi.close();
    fo.close();

    ofstream fo_g(outputfilename+"graphid_mapping");
    for(auto itr: graphid){
        fo_g<<itr.first<<" "<<itr.second<<endl;
    }
    fo_g.close();

    ofstream fo_l(outputfilename+"labelid_mapping");
    for(auto itr: labelid){
        fo_l<<itr.first<<" "<<itr.second<<endl;
    }
    fo_l.close();

}

int main(){
    string filename = "./modified_dataset.fp";
    modify_dataset(filename, "./");
}