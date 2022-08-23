#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <fstream>
#include <queue>
#include <functional>
#include <stack>
#include <map>
#include <unordered_map>
#include <set>
using namespace std;

// node of FPtree
class Node{
    static int unique_id;
public:
    string item;
    int count;
    Node* parent;
    vector<Node*> child;
    int id;
    Node(){
        item = "root";
        count = 0;
        parent = NULL;
        id = unique_id++;
    }
    Node(string item, Node *parent){
       this->item = item;
       count = 1;
       this->parent = parent; 
       id = unique_id++;
    }
    Node(string item, int count, Node *parent){
        this->item = item;
        this->count = count;
        this->parent = parent;
        id = unique_id++;
    }
};
int Node::unique_id = 0;

// FPtree class
class FPTree{

public:
    int support;
    vector<vector<string>> frequent_itemsets;
    Node* root;
    map<string, vector<Node*>> lists;
    
    // checking if item is present in itemset "child"
    int find(vector<Node*> &child, string item){
        for(int i=0; i<child.size(); ++i){
            if(child[i]->item == item){
                return i;
            }
        }
        return -1;
    }

    public:

    FPTree(){
        root = new Node();
    }
    FPTree(int support){
        this->support = support;
        root = new Node();
    }

    // insert "itemset" into the FPtree
    // the "itemset" should be already sorted
    void insert(vector<string> &itemset){ 

        Node *node = root;

        for(int i=0; i<itemset.size(); ++i){
            //cout<<"itemset[i]"<<" ";
            int idx = find(node->child, itemset[i]);

            Node *temp;
            if(idx < 0){
                temp = new Node(itemset[i], node);
                node->child.push_back(temp);

                if(lists.find(temp->item)==lists.end()){
                    lists[temp->item] = vector<Node*>();
                }
                lists[temp->item].push_back(temp);
                
            }else{
                temp = node->child[idx];
                temp->count++;
            }

            node = temp;

        }

    }
    void insert(vector<string> &itemset, int counter)
    {

        Node *node = root;

        for (int i = 0; i < itemset.size(); ++i)
        {
            // cout<<"itemset[i]"<<" ";
            int idx = find(node->child, itemset[i]);

            Node *temp;
            if (idx < 0)
            {
                temp = new Node(itemset[i], counter, node);
                node->child.push_back(temp);

                if (lists.find(temp->item) == lists.end())
                {
                    lists[temp->item] = vector<Node *>();
                }
                lists[temp->item].push_back(temp);
            }
            else
            {
                temp = node->child[idx];
                temp->count += counter;
            }

            node = temp;
        }
    }

    // display nodes with their IDs and parentIDs
    // the ID of root is 0
    void display(){

        queue<Node*> q;
        q.push(root);

        while(!q.empty()){
            Node *node = q.front();
            q.pop();
            // if(node->child.size() > 0){
                cout<<"******"<<endl;
                cout<<"parent id: "<<node->id<<endl;
                for(int i=0; i<node->child.size(); ++i){
                    cout<<"----"<<endl;
                    cout<<"item: "<<node->child[i]->item<<endl;
                    cout<<"count: "<<node->child[i]->count<<endl;
                    cout<<"id: "<<node->child[i]->id<<endl;
                    q.push(node->child[i]);
                    cout<<"----"<<endl;
                }
                cout<<"******"<<endl;
            // }
        }

        for(auto itr: lists){
            cout<<itr.first<<" : ";
            for(auto p: itr.second){
                cout<<p->id<<' ';
            }
            cout<<endl;
        }

    }
};



// split string "line" based on passed delimiter
// each word obtained after splitting is pushed to v
void splitString(string line, char delimiter, vector<string> &v){
    string temp = "";
	for(int i=0;i<line.length();++i){
		
		if(line[i]==delimiter){
			v.push_back(temp);
			temp = "";
		}
		else{
			temp.push_back(line[i]);
		}
		
	}
	v.push_back(temp);
}

// generate 1-itemset
// the 1-itemset are mapped in oIS that is passed as reference
void makeOneItemsetSupport(unordered_map<string, int> &oIS , string filename){
    
    fstream f;
    f.open(filename);

    if(f.is_open()){
        string line;
        while(getline(f, line)){
            vector<string> temp;
            splitString(line, ' ', temp);
            for(int i=0;i<temp.size();++i){
                if(oIS.find(temp[i])==oIS.end()){
                    oIS[temp[i]] = 1;
                }
                else{
                    oIS[temp[i]]++;
                }
            }
        }
    }

    f.close();
}

// sort itemset based on their frequency in 1-itemset
bool SORT_ITEMSET(string a, string b, unordered_map<string,int> &oIS){
    if(oIS[a]==oIS[b]){
        return a > b;
    }
    return oIS[a] > oIS[b];
}

// generate FPTree using 1-itemset
FPTree* generateFPTree(unordered_map<string, int> &oIS, vector<pair<string, int>> &oISList, string filename){
    FPTree *tree = new FPTree();
    fstream f;
    f.open(filename);

    if(f.is_open()){
        string line;
        while(getline(f, line)){
            vector<string> temp;
            splitString(line, ' ', temp);
            
            sort(temp.begin(), temp.end(), bind(SORT_ITEMSET,std::placeholders::_1,std::placeholders::_2, oIS));
            // for(int i=0;i<temp.size();++i){
            //     cout<<temp[i]<<"-";
            // }
            // cout<<endl;
            tree->insert(temp);
        }
    }

    f.close();

    return tree;
}


bool _IsSinglePath(Node *node){
    if(!node)
        return true;
    if (node->child.size() > 1)
    {
        return false;
    }
    return _IsSinglePath(node->child[0]);
}

bool _IsSinglePath(FPTree* tree){
    return _IsSinglePath(tree->root);
}


vector<vector<string>> PowerSet(vector<string> &v){
    vector<vector<string>> result;
    int n = v.size();
    int power = 1 << n;
    for(int i=0;i<power;++i){
        vector<string> temp;
        for(int j=0;j<n;++j){
            if((i & (1 << j))){
                temp.push_back(v[j]);
            }
        }
        if(temp.size()){
            result.push_back(temp);
        }
    }
    return result;
}

vector<string> _getPath(Node *node)
{
    vector<string> result;
    node = node->parent;
    while (node->parent != NULL)
    {
        result.push_back(node->item);
        node = node->parent;
    }
    reverse(result.begin(), result.end());
    return result;
}

void FPgrowth(FPTree *fptree)
{
    if (fptree == NULL || fptree->root == NULL || fptree->root->child.size() == 0)
    {
        return;
    }
    if (_IsSinglePath(fptree))
    {
        vector<string> transaction;
        Node* node = fptree->root;
        while(node->child.size()){
            node = node->child[0];
            if(node->count > fptree->support){
                transaction.push_back(node->item);
            }else{
                break;
            }
        }
        fptree->frequent_itemsets = PowerSet(transaction);
        return;
    }

    for (auto itr : fptree->lists)
    {
        const string& Item = itr.first;
        vector<Node*>& nodes = itr.second;
        if (nodes[0]->count < fptree->support)
        {
            continue;
        }
        fptree->frequent_itemsets.push_back({Item});
        FPTree *subTree = new FPTree(fptree->support);
        for (auto node : nodes)
        {
            vector<string> transaction = _getPath(node);
            subTree->insert(transaction, node->count);
        }
        FPgrowth(subTree);
        vector<vector<string>> &frequent_itemsets_Subtree = subTree->frequent_itemsets;
        for (auto &itemset : frequent_itemsets_Subtree)
        {
            itemset.emplace_back(Item);
        }
        fptree->frequent_itemsets.insert(fptree->frequent_itemsets.end(), frequent_itemsets_Subtree.begin(), frequent_itemsets_Subtree.end());
    }
}

int main(){
    
    string filename = "test.txt";
    FPTree *tree;
    
    unordered_map<string, int> oIS; 
    // makeOneItemsetSupport stores the 1-itemset in oIS
    makeOneItemsetSupport(oIS, filename);

    // push pair of <itemset, frequecy> in oISList
    vector<pair<string, int>> oISList;
    for(auto itr: oIS){
        oISList.push_back(make_pair(itr.first, itr.second));
    }

    // sort oISList by descending order of frequency
    sort(oISList.begin(), oISList.end(), [&](pair<string, int> a, pair<string, int> b){
        return a.second > b.second;
    });

    // generateFPTree
    tree = generateFPTree(oIS, oISList, filename);

    tree->display();
    // for(auto itr: oISList){
    //     cout<<itr.first<<' '<<itr.second<<endl;
    // }


}