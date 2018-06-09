import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import time


def create_topology():
    g_temp = nx.Graph()
    # Don't need to add nodes separately.
    g_temp.add_edge(1, 2, capacity=1, weight=1)  # add a "capacity" parameter
    g_temp.add_edge(1, 3, capacity=1, weight=1)  # can have any name you like
    g_temp.add_edge(2, 3, capacity=1, weight=1)
    g_temp.add_edge(2, 4, capacity=1, weight=1)
    g_temp.add_edge(4, 5, capacity=1, weight=1)
    g_temp.add_edge(1, 6, capacity=1, weight=1)

    # print(g_temp.edges(data=True))
    g = g_temp.to_directed()  # Nice function to produce a directed version
    # print(g.edges(data=True))

    return (g)


def check_validity(alist):
    #This function checks for two things:
    #First: if the summation of cols and rows are less or equal max_flows.
    #Secnd: if all the numbers in 2D array are greater than 0.
    axis0 = alist.sum(axis=0)
    axis1 = alist.sum(axis=1)
    check0 = all([axis0[i] <= max_flows[i] and
                  axis1[i] <= max_flows[i]
                  for i in range(len(max_flows))])
    check1 = all([alist[i, j] >= 0
              for i in range(alist.shape[0])
              for j in range(alist.shape[1])])
    if not check0 or not check1:
        print("Found invalid demands")
        return False
    return


if __name__ == "__main__":
    g = create_topology()

    outdeg = g.edges
    # print(outdeg)

    outdeg = g.out_degree()
    # print(outdeg)
    flow_value = nx.maximum_flow_value(g, 1, 2)
    # print(flow_value)
    flow_value = nx.maximum_flow_value(g, 3, 1)
    # print(flow_value)
    flow_value = nx.maximum_flow_value(g, 2, 5)
    # print(flow_value)
    flow_value = nx.maximum_flow_value(g, 6, 2)
    # print(flow_value)
    flow_value = nx.maximum_flow_value(g, 1, 5)
    # print(flow_value)
    # to_remove = [n for n in outdeg if outdeg[n] == 1]
    # g.remove_nodes_from(to_remove)

    nx.draw(g, with_labels=True)
    plt.draw()
    # plt.show()

    n_nodes = 14
    alist = np.zeros([n_nodes, n_nodes])
    max_flows = [1] * n_nodes

    tic = time.time()
    for t in range(1):
        alist1DnoZeros = []
        for i in range(alist.shape[0]):
            for j in range(alist.shape[1]):
                if i == j:
                    continue
                alist[i, j] = random.uniform(0.0,
                                             min(max_flows[j] - np.sum(alist[:i, j]),
                                                 max_flows[i] - np.sum(alist[i, :j])))
                alist1DnoZeros.append(alist[i, j])
        #print(alist)
        #print("************************")
        print(list(alist1DnoZeros))
        check_validity(alist)
    print("Required time: ", time.time() - tic)
