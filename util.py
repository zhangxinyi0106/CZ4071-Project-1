import matplotlib.pyplot as plt
import networkx as nx

def get_avg_degree(graph):
    """
    Return the average degree of a Networkx graph.
    For other basic information, call nx functions directly.
    e.g.  G.number_of_nodes(); G.number_of_edges(); nx.density(G)
    :param graph: a networkx graph object
    :return: a float number
    """
    nnodes = graph.number_of_nodes()
    s = sum(dict(graph.degree()).values())
    return float(s) / float(nnodes)


def get_largest_component_diameter(graph):
    """
    Return the diameter of the largest component of the graph, prevents unconnected exception.
    :param graph: a networkx graph object
    :return: an integer
    """
    # to get the list of components
    components = nx.connected_components(graph)
    # use the max() command to find the largest one:
    largest_component = max(components, key=len)
    # construct a subgraph of largest component
    subgraph = G.subgraph(largest_component)
    diameter = nx.diameter(subgraph)
    return diameter


def get_clustering_coeff(graph):
    """
    Return the clustering coefficient of the graph
    :param graph: a networkx graph object
    :return: a float number
    """
    clust_coeff = nx.average_clustering(graph)
    return clust_coeff


def plot_degree_distribution(graph):
    """
    Plot the log-log degree distribution for the graph.
    :param graph: a networkx graph object
    """
    hist = nx.degree_histogram(graph)
    degrees = [i for i, _ in enumerate(hist)]
    denom = sum(hist)
    probab = []
    for i in hist:
        p = float(i) / float(denom)
        probab.append(p)
    plt.loglog(degrees, probab, 'ro-')
    plt.xlabel("k")
    plt.ylabel("P(k)")
    plt.title("Degree distribution")
    plt.show()


if __name__ == "__main__":
    n = 1000
    p = 0.03
    G = nx.fast_gnp_random_graph(n, p, seed=None, directed=False)
    plot_degree_distribution(G)
