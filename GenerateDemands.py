import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import time


def create_simple_topology():
    g_temp = nx.Graph()
    # Don't need to add nodes separately.
    g_temp.add_edge(0, 1, capacity=1, weight=1)  # add a "capacity" parameter
    g_temp.add_edge(1, 2, capacity=1, weight=1)  # can have any name you like
    g_temp.add_edge(0, 3, capacity=1, weight=1)
    g_temp.add_edge(1, 3, capacity=1, weight=1)
    g_temp.add_edge(3, 2, capacity=1, weight=1)
    g_temp.add_edge(3, 4, capacity=1, weight=1)

    # print(g_temp.edges(data=True))
    g = g_temp.to_directed()  # Nice function to produce a directed version
    # print(g.edges(data=True))

    return g


def create_nsf_topology():
    g_temp = nx.Graph()
    # Don't need to add nodes separately.
    g_temp.add_edge(1, 2, capacity=1, weight=1)  # add a "capacity" parameter
    g_temp.add_edge(1, 3, capacity=1, weight=1)  # can have any name you like
    g_temp.add_edge(1, 8, capacity=1, weight=1)
    g_temp.add_edge(2, 3, capacity=1, weight=1)
    g_temp.add_edge(2, 4, capacity=1, weight=1)
    g_temp.add_edge(3, 6, capacity=1, weight=1)
    g_temp.add_edge(4, 5, capacity=1, weight=1)
    g_temp.add_edge(4, 11, capacity=1, weight=1)
    g_temp.add_edge(5, 6, capacity=1, weight=1)
    g_temp.add_edge(5, 7, capacity=1, weight=1)
    g_temp.add_edge(6, 10, capacity=1, weight=1)
    g_temp.add_edge(6, 13, capacity=1, weight=1)
    g_temp.add_edge(7, 8, capacity=1, weight=1)
    g_temp.add_edge(8, 9, capacity=1, weight=1)
    g_temp.add_edge(9, 10, capacity=1, weight=1)
    g_temp.add_edge(9, 12, capacity=1, weight=1)
    g_temp.add_edge(9, 14, capacity=1, weight=1)
    g_temp.add_edge(11, 12, capacity=1, weight=1)
    g_temp.add_edge(11, 14, capacity=1, weight=1)
    g_temp.add_edge(12, 13, capacity=1, weight=1)
    g_temp.add_edge(13, 14, capacity=1, weight=1)

    # print(g_temp.edges(data=True))
    g = g_temp.to_directed()  # Nice function to produce a directed version
    # print(g.edges(data=True))
    return g

def check_validity(alist):
    #This function checks for two things:
    #First: if the summation of cols and rows are less or equal max_flows.
    #Secnd: if all the numbers in 2D array are greater than 0.
    max_flows = [2, 3, 2, 4, 1]
    axis0 = alist.sum(axis=0)

    axis1 = alist.sum(axis=1)
    print("axis0: ", axis0)
    print("Difference: ", [axis0[i] - max_flows[i] for i in range(len(max_flows))])
    print("axis1: ", axis1)
    print("Difference: ", [axis1[i] - max_flows[i] for i in range(len(max_flows))])
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

    g = create_simple_topology()
    n_nodes = len(g)
    print(n_nodes)
    max_flows_dict = {}

    #Find max_flow between all pairs:
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i == j:
                continue
            max_flows_dict[(i, j)] = nx.maximum_flow_value(g, i, j)
    print(max_flows_dict)
    #for i in range(no_of_nodes)



    #dictionary for labeling links that are used for grouping them.
    #to keep track of residual capacity.
    #TODO: This dictionary should be automatically computed (not hardcoded!).
    residual_network = {
        'outgoing': {
            0: {
                'group1': {
                    'reachable_nodes': [1, 2, 3, 4],
                    'capacity': 2,
                    'used_capacity': 0
                }
            },
            1: {
                'group1': {
                    'reachable_nodes': [0, 2, 3, 4],
                    'capacity': 3,
                    'used_capacity': 0
                }
            },
            2: {
                'group1': {
                    'reachable_nodes': [0, 1, 3, 4],
                    'capacity': 2,
                    'used_capacity': 0
                }
            },
            3: {
                'group1': {
                    'reachable_nodes': [0, 1, 2],
                    'capacity': 3,
                    'used_capacity': 0
                },
                'group2': {
                    'reachable_nodes': [4],
                    'capacity': 1,
                    'used_capacity': 0
                }
            },
            4: {
                'group1': {
                    'reachable_nodes': [0, 1, 2, 3],
                    'capacity': 1,
                    'used_capacity': 0
                }
            },
        },
        'incoming': {
            0: {
                'group1': {
                    'reachable_nodes': [1, 2, 3, 4],
                    'capacity': 2,
                    'used_capacity': 0
                }
            },
            1: {
                'group1': {
                    'reachable_nodes': [0, 2, 3, 4],
                    'capacity': 3,
                    'used_capacity': 0
                }
            },
            2: {
                'group1': {
                    'reachable_nodes': [0, 1, 3, 4],
                    'capacity': 2,
                    'used_capacity': 0
                }
            },
            3: {
                'group1': {
                    'reachable_nodes': [0, 1, 2],
                    'capacity': 3,
                    'used_capacity': 0
                },
                'group2': {
                    'reachable_nodes': [4],
                    'capacity': 1,
                    'used_capacity': 0
                }
            },
            4: {
                'group1': {
                    'reachable_nodes': [0, 1, 2, 3],
                    'capacity': 1,
                    'used_capacity': 0
                }
            }
        }
    }

    def return_capacity(node, direction):
        return residual_network[direction][node]['group1']['capacity']

    def get_group_name(src, node):
        for group in residual_network['outgoing'][src].keys():
            if node_reachable(src, node, group):
                return group
        #raise "node should be reachable in one of the groups"

        #return node in residual_network['outgoing'][src][group]['reachable_nodes']
    def get_available_capacity(src, dst, direction):
        group = get_group_name(src, dst)
        #print(src, dst, group)
        return residual_network[direction][src][group]['capacity'] - \
               residual_network[direction][src][group]['used_capacity']
    def update_used_capacity(src, dst, value):
        for direction in residual_network.keys():
            #print(direction)
            group = get_group_name(src, dst)
            #print(group)
            used_capacity = residual_network[direction][src][group]['used_capacity']
            capacity = residual_network[direction][src][group]['capacity']
            residual_network[direction][src][group]['used_capacity'] = used_capacity + value



    print("returned capacity:", return_capacity(0, 'outgoing'))
    def node_reachable(src, node, group):
        return node in residual_network['outgoing'][src][group]['reachable_nodes']
    print("Checking if node 1 is reachable from 0: ", node_reachable(0, 1, 'group1'))



    nx.draw(g, with_labels=True)
    plt.draw()
    #plt.show()

    alist = np.zeros([n_nodes, n_nodes])


    tic = time.time()
    for t in range(1):
        alist1DnoZeros = []
        for i in range(alist.shape[0]):
            for j in range(alist.shape[1]):
                if i == j:
                    continue
                min_cap_both_directions = min(get_available_capacity(i, j, 'outgoing'),
                                              get_available_capacity(j, i, 'incoming'))
                if max_flows_dict[(i, j)] <= min_cap_both_directions:
                    alist[i, j] = random.uniform(0.0, max_flows_dict[i, j])
                else:
                    alist[i, j] = random.uniform(0.0, min_cap_both_directions)

                #now update the used_capacity in both directions
                update_used_capacity(i, j, alist[i, j])
                '''alist[i, j] = \
                    random.uniform(0.0,
                                             min(max_flows[j] - np.sum(alist[:i, j]),
                                                 max_flows[i] - np.sum(alist[i, :j])))'''
                alist1DnoZeros.append(alist[i, j])
        print(alist)
        check_validity(alist)
        #if check_validity(alist):
        #   print(alist1DnoZeros)
        #print("************************")
        #print(list(alist1DnoZeros))

    print("Required time: ", time.time() - tic)
