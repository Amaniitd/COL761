import sys, subprocess
import matplotlib.pyplot as plt

inpname = sys.argv[1]
outputFile = sys.argv[2]

sup_list = [5,10,25,50,90]
apriori_list = []
fp_list = []

for x in sup_list:	
	cmd_ap = "./run.o " + inpname + " " + str(x) + " -apriori"
	result_ap = subprocess.check_output(cmd_ap)
	result_ap = float(result_ap)
	apriori_list.append(result_ap)
	cmd_fp = "./run.o " + inpname + " " + str(x) + " -fptree"
	result_fp = subprocess.check_output(cmd_fp)
	result_fp = float(result_fp)
	fp_list.append(result_fp)

plt.plot(sup_list,apriori_list,'r',sup_list,fp_list,'b')
plt.xlabel('Support in percentage')
plt.ylabel('Time taken in seconds')
plt.legend(['Apriori','FP-tree'])
plt.savefig(outputFile+'.png')