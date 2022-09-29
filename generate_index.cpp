#include<iostream>
#include<string>
#include<fstream>
#include<vector>
#include <string>
#include<map>
using namespace std;

void splitString(string line, char delimiter, vector<string> &v)
{   
    
    string temp = "";
    for (int i = 0; i < line.length(); ++i)
    {

        if (line[i] == delimiter)
        {
            if(temp!=" "&&temp.size()>0)
                v.push_back(temp);
            temp = "";
        }
        else
        {
            temp.push_back(line[i]);
        }
    }
    if(temp!=" "&&temp.size()>0)
        v.push_back(temp);
}


void generate_index(string filename, string outputfilename){
    int size = 0;
    fstream fi;
    fi.open(filename);

    map<int, vector<int>> graphidlist;
    int max_id = -1;

    if (fi.is_open())
    {
        string line;
        while (std::getline(fi, line))
        {   
            if(line.length()==0 || line=="\n" || line==""){
                continue;
            }

            if(line[0] == 't'){
                
                vector<string> title;
                splitString(line, ' ', title);

                // id of frequent graph
                // cout<<title[2]<<endl;
                int id = stoi(title[2]);
                max_id = max(max_id, id);

                while(std::getline(fi, line) && line[0]!='x');

                line = line.substr(2);

                vector<string> graph_id;
                splitString(line, ' ', graph_id);

                for(int i=0;i<graph_id.size();++i){
                    
                    // cout<<"print: "<<graph_id[i]<<endl;
                    int id_contain = stoi(graph_id[i]);

                    if(graphidlist.find(id_contain)==graphidlist.end()){
                        graphidlist[id_contain] = vector<int>();
                        graphidlist[id_contain].push_back(id);
                    }
                    else{
                        graphidlist[id_contain].push_back(id);
                    }
                }

            }
        
        }
    }

    fi.close();

    ofstream fo(outputfilename);


    if (fo.is_open())
    {
        for(auto &v: graphidlist){
            vector<int> hash(max_id+1, 0);
            for(auto &id: v.second){
                // cout<<"III = " <<id<<endl;
                hash[id] = 1;
            }
            fo<<v.first;
            for(int i=0;i<hash.size();++i){
                fo<<' '<<hash[i];
            }
            fo<<endl;
        }
    }

    fo.close();



}

int main(){
    string filename = "./modified_dataset.fp";
    string outputfile = "./features.txt";
    generate_index(filename, outputfile);
}