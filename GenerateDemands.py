import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import time
from termcolor import colored


def create_simple_topology():
    g_temp = nx.Graph()
    g_temp.add_edge(0, 1, capacity=1, weight=1)  # add a "capacity" parameter
    g_temp.add_edge(1, 2, capacity=1, weight=1)
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
    g_temp.add_edge(0, 1, capacity=1, weight=1)
    g_temp.add_edge(0, 2, capacity=1, weight=1)
    g_temp.add_edge(0, 7, capacity=1, weight=1)
    g_temp.add_edge(1, 2, capacity=1, weight=1)
    g_temp.add_edge(1, 3, capacity=1, weight=1)
    g_temp.add_edge(2, 5, capacity=1, weight=1)
    g_temp.add_edge(3, 4, capacity=1, weight=1)
    g_temp.add_edge(3, 10, capacity=1, weight=1)
    g_temp.add_edge(4, 5, capacity=1, weight=1)
    g_temp.add_edge(4, 6, capacity=1, weight=1)
    g_temp.add_edge(5, 9, capacity=1, weight=1)
    g_temp.add_edge(5, 12, capacity=1, weight=1)
    g_temp.add_edge(6, 7, capacity=1, weight=1)
    g_temp.add_edge(7, 8, capacity=1, weight=1)
    g_temp.add_edge(8, 9, capacity=1, weight=1)
    g_temp.add_edge(8, 11, capacity=1, weight=1)
    g_temp.add_edge(8, 13, capacity=1, weight=1)
    g_temp.add_edge(10, 11, capacity=1, weight=1)
    g_temp.add_edge(10, 13, capacity=1, weight=1)
    g_temp.add_edge(11, 12, capacity=1, weight=1)
    g_temp.add_edge(12, 13, capacity=1, weight=1)

    # print(g_temp.edges(data=True))
    g = g_temp.to_directed()  # Nice function to produce a directed version
    # print(g.edges(data=True))
    return g


def check_validity(alist, g):
    # This function checks for two things:
    # First: if the summation of cols and rows are less or equal max_flows.
    # Second: if all the numbers in 2D array are greater than 0.

    # max_flows is a maximum a node can send
    # (the summation of capacities of all outgoing links)
    max_flows = [0] * len(g)
    for node in g.nodes():
        for edge in g.edges(node):
            max_flows[node] += g[node][edge[1]]['capacity']
    axis0 = alist.sum(axis=0)
    axis1 = alist.sum(axis=1)
    # print("axis0: ", axis0)
    # print("Difference: ", [axis0[i] - max_flows[i] for i in range(len(max_flows))])
    # print("axis1: ", axis1)
    # print("Difference: ", [axis1[i] - max_flows[i] for i in range(len(max_flows))])
    check0 = all([axis0[i] <= max_flows[i] and
                  axis1[i] <= max_flows[i]
                  for i in range(len(max_flows))])
    check1 = all([alist[i, j] >= 0
                  for i in range(alist.shape[0])
                  for j in range(alist.shape[1])])
    if not check0 or not check1:
        print(colored("Found invalid demands", "green"))
        return False
    return


def build_residual_network_dict(g):
    # dictionary for labeling links that are used for grouping them.
    # to keep track of residual capacity later.
    temp_dict = {}
    accumulated_capacity = {}
    directions = ['outgoing', 'incoming']
    for direction in directions:
        temp_dict[direction] = {}
        for node in g.nodes():
            temp_dict[direction][node] = {}
            edges = g.edges(node)
            # copy to a temp graph
            list_of_group_sets = []
            group_id = 0
            for edge in edges:
                temp_g = g.copy()
                # remove all edges of that node from temp_g
                temp_g.remove_edges_from(edges)
                # now return current edge and calculate descendants.
                temp_g.add_edge(node, edge[1])
                descendants = nx.descendants(temp_g, node)
                if descendants in list_of_group_sets:
                    # adding capacity
                    accumulated_capacity[tuple(descendants)] += g[node][edge[1]]['capacity']
                    temp_dict[direction][node]['group' + str(group_id)]['capacity'] = accumulated_capacity[tuple(descendants)]
                else:
                    accumulated_capacity[tuple(descendants)] = 0
                    accumulated_capacity[tuple(descendants)] += g[node][edge[1]]['capacity']
                    group_id += 1
                    temp_dict[direction][node]['group' + str(group_id)] = {}
                    temp_dict[direction][node]['group' + str(group_id)]['capacity'] = accumulated_capacity[tuple(descendants)]
                    temp_dict[direction][node]['group' + str(group_id)]['used_capacity'] = 0
                    temp_dict[direction][node]['group' + str(group_id)]['reachable_nodes'] = descendants
                    list_of_group_sets.append(set(descendants))
    # dangerous: this will not work! It will update both keys (outgoing, and incoming) with same value!
    #temp_dict = {'outgoing': temp_dict, 'incoming': temp_dict}
    return temp_dict


def get_group_name(src, node):
    for group in residual_network['outgoing'][src].keys():
        if node_reachable(src, node, group):
            return group
    # raise "node should be reachable in one of the groups"


def get_available_capacity(src, dst, direction):
    group = get_group_name(src, dst)
    # print(src, dst, group)
    return residual_network[direction][src][group]['capacity'] - \
           residual_network[direction][src][group]['used_capacity']


def update_used_capacity(src, dst, value):
    #print(src, dst)
    for direction in residual_network.keys():
        if direction == 'outgoing':
            group = get_group_name(src, dst)
            used_capacity = residual_network[direction][src][group]['used_capacity']
            residual_network[direction][src][group]['used_capacity'] = used_capacity + value

        if direction == 'incoming':
            group = get_group_name(dst, src)
            used_capacity = residual_network[direction][dst][group]['used_capacity']
            residual_network[direction][dst][group]['used_capacity'] = used_capacity + value
    #print(residual_network)
        # print(group)
        # capacity = residual_network[direction][src][group]['capacity']


def node_reachable(src, node, group):
    return node in residual_network['outgoing'][src][group]['reachable_nodes']


def build_max_flows_dict(g):
    global i, j
    for i in g.nodes():
        for j in g.nodes():
            if i == j:
                continue
            # nice function in networkX to find the
            # maximum flow in a single-commodity flow.
            max_flows_dict[(i, j)] = nx.maximum_flow_value(g, i, j)
    return max_flows_dict


def create_demand(g, scaler):
    n_nodes = len(g)
    demand2D = np.zeros([n_nodes, n_nodes])
    demand1D = []
    for i in range(demand2D.shape[0]):
        for j in range(demand2D.shape[1]):
            if i == j:
                continue
            min_cap_both_directions = min(get_available_capacity(i, j, 'outgoing'),
                                          get_available_capacity(j, i, 'incoming'))
            if max_flows_dict[(i, j)] <= min_cap_both_directions:
                demand2D[i, j] = random.uniform(0.0, max_flows_dict[i, j] * scaler)
            else:
                demand2D[i, j] = random.uniform(0.0, min_cap_both_directions * scaler)

            # now update the used_capacity in both directions.
            # this function will handle the both directions.
            update_used_capacity(i, j, demand2D[i, j])
            # get a 1D version with no zeros (no diagonal)
            demand1D.append(demand2D[i, j])
    check_validity(demand2D, g)
    return demand1D


def draw_graph(g):
    nx.draw(g, with_labels=True)
    plt.draw()
    plt.show() #enable to show a graph of the network


if __name__ == "__main__":

    g = create_simple_topology()
    #g = create_nsf_topology()
    #scaler = 0.60  # generate random up to 60% of the available unused capacity.
    #scalers = [1] * 1
    list_of_summed_or_averaged_demands = []
    n_scalers = 1000
    scalers = [(0 + i) / n_scalers for i in range(1, n_scalers)]
    for scaler in scalers:
        residual_network = build_residual_network_dict(g)


        # Find max_flow between all pairs:
        max_flows_dict = {}
        max_flows_dict = build_max_flows_dict(g)
        # print(max_flows_dict)

        #draw_graph(g)

        #print(scaler)
        demands = create_demand(g, scaler)
        #print(residual_network)
        # (demands) is a list of demands that we need to store in a file
        print(demands)
        print(scaler, np.mean(demands))
        list_of_summed_or_averaged_demands.append(np.mean(demands))
    plt.plot(scalers, list_of_summed_or_averaged_demands)
    plt.xlabel('Scaler')
    plt.ylabel('Random generated number (average of demands)')
    plt.show()


###########################################################
# THIS IS AN EXAMPLE OF HOW THE DICTIONARY SHOULD LOOK LIKE
'''
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
'''
