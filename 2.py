import csv
import os
import torch
import math
import numpy as np
from torch import nn
from torch.nn import functional as F
import time
import sys

nodes=0
emb_dim=12
firstline=[]
inputdata=[]
adjmatrix=[]
timestamp=[]
data=sys.argv[1]
adj=sys.argv[2]
nlist=sys.argv[3]
p=int(sys.argv[4])
f=int(sys.argv[5])

print("Loading Data....");
file=open(data)
afile=open(adj)
line=file.readline()
myline=line.split(',')
nodes=len(myline)-1
for i in range(1,len(myline)):
	firstline.append(int(myline[i].strip()))
line=file.readline()

while True:
	if not line:
		break;
	s=line.split(',')
	ls=[]
	for i in range(1,len(s)):
		ls.append(float(s[i].strip()));
	timestamp.append(s[0])
	inputdata.append(ls)
	line=file.readline()
file.close()

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
lines=len(inputdata)
print("Rows:",lines)
print("Nodes:",nodes)


class Node:
	def __init__(self):
		self.pos=0
		self.w=0

print("Creating Adjacancy lists")
print("Training....")

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


splits=np.load(nlist)
trainn=splits["train_node_ids"]

status=[False]*nodes

for i in range(0,len(trainn)):
	for j in range(0,nodes):
		if firstline[j]==trainn[i]:
			status[j]=True
			break

valn=splits["val_node_ids"]
testn=splits["test_node_ids"]

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


model=MLP(p,f)
lossfunction=nn.MSELoss();
optimizer=torch.optim.SGD(model.parameters(),lr=0.0005)
prevt=[0.0]*nodes
model.adjpath=adj

start=time.time()

for epoch in range(0,3):
	for i in range(0,lines):
		print("Epoch:",epoch,"Sample:",i)
		en=i-1;
		st=en-p+1
		if(st<0):
			st=0;
		if(en<0):
			en=0;
		myebd=[[0]*p for i in range(nodes)]

		for k in range(0,nodes):
			for j in range(0,p):
				myebd[k][j]=inputdata[st+j][k]

		for j in range(0,nodes):
				agg=[0]*p
				cadjlist=adlists[j]
				for l in range(len(cadjlist)):
					for o in range(0,p):
						agg[o]=agg[o]+myebd[cadjlist[l].pos][o]
				cated=myebd[j]+agg
				inputtoml=model.getRNNNE(torch.Tensor(cated),torch.Tensor(myebd[j])).detach().numpy()
				if status[j]:
					optimizer.zero_grad()
					outputs=model(torch.Tensor(inputtoml))
					actual=[0]*f
					index=0;
					endf=i+f
					if endf>=lines:
						endf=lines
					for lp in range(i,endf):
						actual[index]=inputdata[lp][j]
						index=index+1
					loss=lossfunction(outputs,torch.Tensor(actual))
					loss.backward()
					optimizer.step()
				
end=time.time()
print(end-start)
torch.save(model,"mymodel.model")