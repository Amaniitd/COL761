import sys

labels = {}

currLabel = 0

def labelIt(token):
    global labels
    global currLabel
    if token not in labels:
        labels[token] = currLabel
        currLabel += 1
    return labels[token]

InputFileName = sys.argv[1]
OutputFileName = sys.argv[2]
GraphType = sys.argv[3]
inputFile = open(InputFileName, "r")
tokens = inputFile.read().strip().split()
outputFile = open(OutputFileName, "w")
i = 0;
while(i < len(tokens)):
    outputFile.write(f"t # {tokens[i][1:]}\n")
    i+=1
    n = int(tokens[i])
    i+=1
    for j in range(n):
        outputFile.write(f"v {j} {labelIt(tokens[i])}\n")
        i+=1
    m = int(tokens[i])
    i+=1
    for j in range(m):
        gtype = "e"
        if GraphType == "fsg":
            gtype = "u"
        outputFile.write(f"{gtype} {tokens[i]} {tokens[i+1]} {tokens[i+2]}\n")
        i+=3
outputFile.close()
inputFile.close()

