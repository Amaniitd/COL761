import sys
import os
import matplotlib.pyplot as plt
import time

noOfGraphs = 0
labels = {}
currLabel = 0
supportThreshold = [5,10,25,50,95]
gspanTime = []
fsgTime = []
gastonTime = []


def labelIt(token):
    global labels
    global currLabel
    if token not in labels:
        labels[token] = currLabel
        currLabel += 1
    return labels[token]

def generateFiles():
    global noOfGraphs
    InputFileName = sys.argv[1]
    OutputFileNames = ["fsg_.txt", "g_.txt"]
    inputFile = open(InputFileName, "r")
    tokens = inputFile.read().strip().split()
    outputFileF = open(OutputFileNames[0], "w")
    outputFileG = open(OutputFileNames[1], "w")
    i = 0
    while (i < len(tokens)):
        noOfGraphs += 1
        outputFileF.write(f"t # {tokens[i][1:]}\n")
        outputFileG.write(f"t # {tokens[i][1:]}\n")
        i += 1
        n = int(tokens[i])
        i += 1
        for j in range(n):
            outputFileF.write(f"v {j} {labelIt(tokens[i])}\n")
            outputFileG.write(f"v {j} {labelIt(tokens[i])}\n")
            i += 1
        m = int(tokens[i])
        i += 1
        for j in range(m):
            outputFileF.write(f"u {tokens[i]} {tokens[i+1]} {tokens[i+2]}\n")
            outputFileG.write(f"e {tokens[i]} {tokens[i+1]} {tokens[i+2]}\n")
            i += 3
    outputFileF.close()
    outputFileG.close()
    inputFile.close()


def runGspan(support):
    print(f"Running gspan for support {support}")
    currentTime = time.time()
    os.system(f"timeout 1h ./gSpan-64 -s {support/100} -f g_.txt") # We can set timeout to as 1h | 30m etc
    return time.time() - currentTime

def runFsg(support):
    print(f"Running fsg for support {support}")
    currentTime = time.time()
    os.system(f"timeout 1h ./fsg -s {support} fsg_.txt" )
    return time.time() - currentTime

def runGaston(support):
    print(f"Running gaston for support {support}")
    currentTime = time.time()
    os.system(f"timeout 1h ./gaston {support*noOfGraphs/100} g_.txt")
    return time.time() - currentTime

def generatePlot():
    for i in supportThreshold:
        print(f"Support Threshold: {i}")
        gastonTime.append(runGaston(i))
        gspanTime.append(runGspan(i))
        fsgTime.append(runFsg(i))
    plt.plot(supportThreshold, gspanTime, label="gspan")
    plt.plot(supportThreshold, fsgTime, label="fsg")
    plt.plot(supportThreshold, gastonTime, label="gaston")
    plt.xlabel("Support Threshold")
    plt.ylabel("Time")
    plt.legend()
    plt.savefig("Q1.png")


def main():
    generateFiles()
    generatePlot()

main()