import sys, subprocess
import matplotlib.pyplot as plt

inpname = sys.argv[1]
outputFile = sys.argv[2]

sup_list = [90, 50, 25, 20, 15]
apriori_list = []
fp_list = []
fp_sup_list = []
ap_sup_list = []
for x in sup_list:	
	# print("Running for support = " + str(x))
	if (x > 15):
		cmd_ap = "./run.o " + inpname + " " + str(x) + " -apriori"
		result_ap = subprocess.check_output(cmd_ap, shell=True)
		result_ap = float(result_ap)
		apriori_list.append(result_ap)
		ap_sup_list.append(x)
	
	cmd_fp = "./run.o " + inpname + " " + str(x) + " -fptree"
	result_fp = subprocess.check_output(cmd_fp, shell=True)
	result_fp = float(result_fp)
	fp_list.append(result_fp)
	fp_sup_list.append(x)


fig, ax = plt.subplots()
ax.plot(ap_sup_list, apriori_list, label='Apriori', color='blue')
ax.plot(fp_sup_list, fp_list, label='FP-Tree', color='red')
plt.xlabel('Support in percentage')
plt.ylabel('Time taken in seconds')
plt.legend(['Apriori','FP-tree'])
plt.savefig(outputFile+'.png')