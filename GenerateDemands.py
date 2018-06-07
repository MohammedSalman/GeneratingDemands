import networkx as nx
import matplotlib.pyplot as plt


def create_topology():
    g_temp = nx.Graph()
    # Don't need to add nodes separately.
    g_temp.add_edge(1, 2, capacity=1000, weight=1)  # add a "capacity" parameter
    g_temp.add_edge(1, 3, capacity=1, weight=1)  # can have any name you like
    g_temp.add_edge(2, 3, capacity=1, weight=1)
    g_temp.add_edge(2, 4, capacity=1, weight=1)
    g_temp.add_edge(4, 5, capacity=1, weight=1)
    g_temp.add_edge(1, 6, capacity=1, weight=1)

    # print(g_temp.edges(data=True))
    g = g_temp.to_directed()  # Nice function to produce a directed version
    # print(g.edges(data=True))

    return (g)


if __name__ == "__main__":
    g = create_topology()

    outdeg = g.edges
    # print(outdeg)

    outdeg = g.out_degree()
    print(outdeg)
    flow_value = nx.maximum_flow_value(g, 1, 2)
    print(flow_value)
    flow_value = nx.maximum_flow_value(g, 3, 1)
    print(flow_value)
    flow_value = nx.maximum_flow_value(g, 2, 5)
    print(flow_value)
    flow_value = nx.maximum_flow_value(g, 6, 2)
    print(flow_value)
    flow_value = nx.maximum_flow_value(g, 1, 5)
    print(flow_value)
    # to_remove = [n for n in outdeg if outdeg[n] == 1]
    # g.remove_nodes_from(to_remove)

    nx.draw(g, with_labels=True)
    plt.draw()
    plt.show()

    '''outdeg = G.out_degree()
    to_remove = [n for n in outdeg if outdeg[n] == 1]
    Removing is then:

    G.remove_nodes_from(to_remove)
    If you prefer to create a new graph instead of modifying the existing graph in place, create a subgraph:

    to_keep = [n for n in outdeg if outdeg[n] != 1]
    G.subgraph(to_keep)'''