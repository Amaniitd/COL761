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
  def __init__(self):
    super().__init__()
    self.stodim=torch.nn.Linear(1,12)
    self.vtov=torch.nn.Linear(12,1)
    self.layer1=torch.nn.Linear(12,1)
    self.myrelu=nn.ReLU()
    self.myrelu1=nn.ReLU()
    self.adjpath=""
    self.rnn=nn.RNNCell(24,12)
  def getRNNNE(self,inputs,hidden):
  	return self.rnn(inputs,hidden)		 
  def forward(self, x):
    return self.myrelu(self.layer1(x))
  	
nodes=0
emb_dim=12
firstline=[]
inputdata=[]
adjmatrix=[]
timestamp=[]
data=sys.argv[1]
outputfile=sys.argv[2]
modelfile=sys.argv[3]
model=torch.load(modelfile)
adj=model.adjpath

output=open(outputfile,"w+")

print("Loading Data....");
file=open(data)
afile=open(adj)
line=file.readline()
output.write(line)
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

prevt=[0.0]*nodes

start=time.time()
for i in range(0,lines):
	actual=[]
	myout=[]
	for j in range(len(inputdata[i])):
		actual.append(inputdata[i][j])
	for j in range(0,nodes):
		agg=[0]*22
		cadjlist=adlists[j]
		for k in range(len(cadjlist)):
			dim=model.vtov(torch.Tensor([prevt[cadjlist[k].pos]])).detach().numpy()
			for o in range(0,10):
				agg[o]=agg[o]+dim[o]
			for o in range(10,22):
				agg[o]=agg[o]+onf[cadjlist[k].pos][o-10]
		if (len(cadjlist))!=0:
			for o in range(0,12):
				agg[o]=agg[o]/len(cadjlist)
		tnf=[0]*12
		for p in range(0,12):
			tnf[p]=onf[j][p]
		cated=tnf+agg
		inputtoml=model.getRNNNE(torch.Tensor(cated),torch.Tensor(tnf)).detach().numpy()
		for p in range(0,12):
			nf[j][p]=inputtoml[p]
	
	for j in range(0,nodes):
		finput=[0]*12
		for k in range(12):
			finput[k]=nf[j][k]
		outputs=model(torch.Tensor(finput))
		myout.append(outputs.detach().numpy()[0])
	finalstr=timestamp[i]+","
	for op in range(0,nodes):
		if op==(nodes-1):
			finalstr=finalstr+str(myout[op])
		else:
			finalstr=finalstr+str(myout[op])+","
	output.write(finalstr)
	output.write("\n")

	for lop in range(0,nodes):
		prevt[lop]=actual[lop]
	for lop in range(0,nodes):
		for pop in range(0,12):
			onf[lop][pop]=nf[lop][pop]

	print("ROW",(i))
end=time.time()
print(end-start)