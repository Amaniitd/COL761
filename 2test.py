import csv
import os
import torch
import math
import numpy as np
from torch import nn
from torch.nn import functional as F
import time
import sys

class MLP(nn.Module):
  def __init__(self,p,f):
    super().__init__()
    self.stodim=torch.nn.Linear(1,12)
    self.layer=torch.nn.Linear(24,12)
    self.myrelu=nn.ReLU()
    self.myrelu1=nn.ReLU()
    self.adjpath=""
    self.p=p
    self.f=f
    self.layer1=torch.nn.Linear(12,self.f)
    self.rnn=nn.RNNCell(24,12)
    self.rnn1=nn.RNNCell(12,12)
  def getRNNNE(self,inputs,hidden):
  	output_emb=self.rnn(inputs,hidden)		
  	return F.normalize(output_emb,dim=0) 
  def forward(self, x):
    return self.layer1(x)

nodes=0
emb_dim=12
firstline=[]
adjmatrix=[]
timestamp=[]
data=sys.argv[1]
outputfilename=sys.argv[2]
modelname=sys.argv[3]
p=int(sys.argv[4])
f=int(sys.argv[5])
model=torch.load(modelname)
adj=model.adjpath

afile=open(adj)
print("Loading Data....");

test_data=np.load(data)
print(test_data['x'].shape)
test_data=test_data['x']
nodes=len(test_data[0][0])
print(nodes)


print("Loading Adjacancey....")
line=afile.readline()
line=afile.readline()
while True:
	if not line:
		break;
	s=line.split(',')
	ls=[]
	for i in range(1,len(s)):
		ls.append(float(s[i].strip()));
	adjmatrix.append(ls);
	line=afile.readline()
afile.close()
print("Nodes:",nodes)


class Node:
	def __init__(self):
		self.pos=0
		self.w=0

print("Creating Adjacancy lists")
print("Testing....")

adlists=[]
for i in range(0,nodes):
	myls=[]
	for j in range(0,nodes):
		if adjmatrix[i][j]!=0:
			mynode=Node()
			mynode.pos=j
			mynode.w=adjmatrix[i][j]
			myls.append(mynode);
	adlists.append(myls)

nf=[[0]*12 for i in range(nodes)]
onf=[[0]*12 for i in range(nodes)]



winsiz=len(test_data)
finalout=[]

for i in range(0,winsiz):
	print(i)
	data=test_data[i]
	myebd=[[0]*p for i in range(nodes)]

	outs=[[0]*nodes for i in range(f)]

	for k in range(0,nodes):
		for j in range(0,p):
			myebd[k][j]=data[j][k]

	for j in range(0,nodes):
			agg=[0]*p
			cadjlist=adlists[j]
			for l in range(len(cadjlist)):
				for o in range(0,p):
					agg[o]=agg[o]+myebd[cadjlist[l].pos][o]
			cated=myebd[j]+agg
			inputtoml=model.getRNNNE(torch.Tensor(cated),torch.Tensor(myebd[j])).detach().numpy()
			index=0;
			outputs=model(torch.Tensor(inputtoml))
			outputs=outputs.detach().numpy()
			out=[0]*f
			for op in range(0,f):
				outs[op][j]=outputs[op]
	finalout.append(outs)
np.savez(outputfilename,y=finalout)


