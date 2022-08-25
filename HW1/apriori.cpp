#include<bits/stdc++.h>
#include<iostream>
#include<fstream>
#include<cstring>
#include<map>
#include<unordered_map>
#include<sys/time.h>
#include<unistd.h>
#include<algorithm>

using namespace std;

const double micros = 1.0e-6;
double CT()
{
 struct timeval TV;
 struct timezone TZ;
 int RC = gettimeofday(&TV,&TZ);
 if (RC == -1){
 return(-1);
 }
 return ( ((double)TV.tv_sec ) + micros * ((double) TV.tv_usec
));
}

float X;
int t=0;
fstream ifile,ofile;

set<set<string>> itemsets;

int size=0;

vector<set<string>> fsets;
vector<set<string>> csets;
unordered_map<string,int> can1;
map<int,int> itemsets_f;
map<set<string>,int> lmf;


void getMeCandidates()
{
lmf.clear();

double st,en;
int fsize=fsets.size();

for(int a=0;a<fsize-1;a++)
{
for(int b=a+1;b<fsize;b++)
{
set<string> setr;
set<string>::iterator setitr;
for (setitr=fsets[a].begin();setitr!=fsets[a].end();++setitr)
{
setr.insert(*setitr);
}
for (setitr=fsets[b].begin();setitr!=fsets[b].end();++setitr)
{
setr.insert(*setitr);
}

if(setr.size()==size&&lmf.find(setr)==lmf.end())
{
csets.push_back(setr);
lmf[setr]=1;
}

}
}

ifile.clear();
ifile.seekg(0);
string line;
int count=0;
//T starts

while(getline(ifile,line))
{

stringstream line1(line);
string query;
unordered_map<string,int> el;

while(getline(line1,query,' '))
{
el[query]++;
}

for(int i=0;i<csets.size();i++)
{
bool ok=true;
set<string>::iterator i1;
for(i1=csets[i].begin();i1!=csets[i].end();++i1)
{

    if(el.find(*i1)==el.end()){
        ok=false;
        break;
    }
}
if(ok)
{
++itemsets_f[i];
}
}
}
}


int main(int a,char *args[])
{
double st=CT();
string infile=args[1];
string otfile=args[3];
int thr=stoi(args[2]);

X=(float)thr/100.0;

cout<<"Loading data"<<endl;
ifile.open(infile,ios::in);
ofile.open(otfile,ios::out);
cout<<"Data loaded"<<endl;

unordered_map<string,int>::iterator itr;

string line;
while(getline(ifile,line))
{
cout<<t<<endl;
stringstream line1(line);
string query;
while(getline(line1,query,' '))
{
    ++can1[query];
}
++t;
}


for (itr=can1.begin();itr!=can1.end();++itr)
{
if(((float)(itr->second)/(float)t)>=X)
{     set<string> ser;
    ser.insert(itr->first);
    fsets.push_back(ser);
    itemsets.insert(ser);
}
}

size=2;


while(!fsets.empty())
{
cout<<"Itemsets size:"<<size<<endl;
csets.clear();
itemsets_f.clear();
getMeCandidates();
fsets.clear();
int csetsize=csets.size();

for(int i=0;i<csetsize;++i)
{
    if(((float)(itemsets_f[i])/(float)t)>=X){
    fsets.push_back(csets[i]);
    itemsets.insert(csets[i]);
}
}
++size;
}


set<set<string>>::iterator fi;

for(fi=itemsets.begin();fi!=itemsets.end();++fi)
{
set<string> temp=*fi;
set<string>::iterator op;

if(fi!=itemsets.begin()){
  ofile<<"\n";  
}

for(op=temp.begin();op!=temp.end();++op)
{
    if(op!=temp.begin()){
       ofile<<" "; 
    }
ofile<<*op;
}


}

double en=CT();
cout<<"Time:"<<en-st<<endl;
ifile.close();
ofile.close();
return 0;
}
