import sys, subprocess
import matplotlib.pyplot as plt

inpname = sys.argv[1]
outputFile = sys.argv[2]

sup_list = [1,5,10,25,50,90]
apriori_list = []
fp_list = []

for x in sup_list:	
	cmd_ap = "./run.o " + inpname + " " + str(x) + " -apriori"
	result_ap = subprocess.check_output(cmd_ap, shell=True)
	# print(result_ap)
	# result_ap = float(result_ap.split()[1])
	# apriori_list.append(result_ap)
	
	# cmd_fp = "./run " + inpname + " " + str(x) + " -fptree"
	# result_fp = subprocess.check_output(cmd_fp, shell=True)
	# result_fp = float(result_fp.split()[1])
	# fp_list.append(result_fp)

# plt.plot(sup_list,apriori_list,'r',sup_list,fp_list,'b')
# plt.xlabel('Support Thresholds (in percentage)')
# plt.ylabel('Running time (in seconds)')
# plt.legend(['Apriori','FP-tree'])
# plt.savefig(outputFile+'.png')