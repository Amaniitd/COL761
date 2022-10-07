
import sys
import matplotlib.pyplot as plt
import random

def ReadDataset(filename):
    dataset = []
    with open(filename) as file_in:
        for line in file_in:
            temp = line.split()
            dataset.append([float(x) for x in temp])
    return dataset

def dist(A, B, d):
    sum = 0.0
    for i in range(d):
        sum = sum + pow(A[i]-B[i], 2)
    return sum

def main():

    d = int(sys.argv[2]) # dimension
    filename = sys.argv[1] # dataset

    dataset = ReadDataset(filename) # n x d
    K = [i+1 for i in range(15)]
    
    n = len(dataset) # number of points in dataset

    Variance = []

    for k in K:

        variance_within_cluster = [0 for i in range(k)]
        k_centers = [random.choice(dataset) for i in range(k)]

        while True:
            
            number_of_nodes_in_cluster = [0 for i in range(k)]
            new_center = [[0.0 for i in range(d)] for j in range(k)]
            variance_within_cluster_next = [0 for i in range(k)]

            for i in range(n):

                min_dist = sys.float_info.max
                min_idx = -1
                for j in range(k):
                    distance = dist(dataset[i], k_centers[j], d)
                    if distance < min_dist:
                        min_dist = distance
                        min_idx = j
                variance_within_cluster_next[min_idx] = variance_within_cluster_next[min_idx] + min_dist 
                number_of_nodes_in_cluster[min_idx] = number_of_nodes_in_cluster[min_idx] + 1
                
                for p in range(d):
                    new_center[min_idx][p] = new_center[min_idx][p] + dataset[i][p]
            
            for i in range(k):
                if number_of_nodes_in_cluster[i] == 0:
                    variance_within_cluster_next[i] = 0
                    new_center[i] = k_centers[i]
                    continue
                variance_within_cluster_next[i] = variance_within_cluster_next[i] / number_of_nodes_in_cluster[i]
                for p in range(d):
                    new_center[i][p] = new_center[i][p] / number_of_nodes_in_cluster[i]
            
            k_centers = new_center

            prev_var = sum(variance_within_cluster) / k
            new_var = sum(variance_within_cluster_next) / k
            

            if abs(prev_var - new_var) < 1e-10:
                break

            variance_within_cluster = variance_within_cluster_next


        # plot the data to see if algorithm is working correctly
        # colors = ['red','blue','green','orange','purple','silver','brown','gray', 'pink', 'maroon', 'violet', 'magenta', 'gold', 'coral', 'rust', 'cyan']
        # for i in range(n):
        #     min_dist = sys.float_info.max
        #     min_idx = -1
        #     for j in range(k):
        #         distance = dist(dataset[i], k_centers[j], d)
        #         if distance < min_dist:
        #             min_dist = distance
        #             min_idx = j
        #     if min_idx != -1:
        #         plt.scatter(dataset[i][0],dataset[i][1], color=colors[min_idx])
        # for j in range(k):
        #     circle1 = plt.Circle((k_centers[j][0], k_centers[j][1]), 0.1, color=colors[j], alpha = 0.2)
        #     plt.gca().add_patch(circle1)    
        #     #plt.scatter(k_centers[j][0], k_centers[j][1], color = 'black', alpha=0.5)
        # plt.savefig(f"{k}.png")
        # plt.clf()


        Variance.append(new_var)

    plt.plot(K, Variance)
    plt.xlabel("k")
    plt.ylabel("Variance within Class")
    plt.savefig(sys.argv[3])







if __name__ == "__main__":
    main()
