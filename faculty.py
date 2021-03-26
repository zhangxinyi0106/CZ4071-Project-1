import time
from typing import Set

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from preprocessing import *
from pictures import PICTURE_PATH


class Analyzer:
    venue_to_booktitle = dict({
        'ACM SIGMOD': r'SIGMOD Conference',
        'ACM KDD': r'KDD',
        'ACM SIGIR': r'SIGIR',
        'CVPR': r'CVPR',
        'NeurIPS': r'N(eur)?IPS',
        'ACM SIGCOMM': 'SIGCOMM',
        'ACM CCS': 'CCS',
        'ACM/IEEE International Conference on Software Engineering': r'ICSE',
        'ISCA': r'ISCA',
        'ACM CHI': r'CHI',
        'PODC': r'PODC',
        'ACM SIGGRAPH ': r'SIGGRAPH\ *',
        'ACM RECOMB': r'RECOMB',
        'ACM MM': r'ACM Multimedia'
    })

    def __init__(self,
                 data_path=DATA_PATH,
                 faculty_filename='Faculty.xlsx',
                 faculty_sheet_name='by course',
                 top_conf_filename='Top.xlsx',
                 top_conf_sheet_name='Sheet1',
                 reuse_cache=True,
                 target_cache_name='profiles',
                 ):
        self.data_path = data_path
        self.faculty_filename = faculty_filename
        self.faculty_sheet_name = faculty_sheet_name
        self.top_conf_filename = top_conf_filename
        self.top_conf_sheet_name = top_conf_sheet_name
        self.reuse_cache = reuse_cache
        self.target_cache_name = target_cache_name
        self.auth_name_data = read_faculty(path=self.data_path,
                                           filename=self.faculty_filename,
                                           sheet_name=self.faculty_sheet_name)
        self.auth_profiles = fetch_dblp_profile(auth_name_data=self.auth_name_data,
                                                reuse=self.reuse_cache,
                                                target_pickle_name=self.target_cache_name)
        self.top_conf_data = read_top_conferences(path=self.data_path,
                                                  filename=self.top_conf_filename,
                                                  sheet_name=self.top_conf_sheet_name)
        self.auth_excellence = self._get_auth_excellence()

    @classmethod
    def _venue_name_to_booktitle(cls, venue_name: str) -> str:
        """
        return the searching requirements of conferences
        :param venue_name: Human-readable conference name
        :return: conference code, book title,
        """
        if venue_name in cls.venue_to_booktitle:
            return cls.venue_to_booktitle[venue_name]
        else:
            raise ValueError(f'Unexpected Conference Name {venue_name} Encountered!')

    def _get_auth_excellence(self) -> dict:
        """
        count the number of paper published in the respective top conferences
        by each faculty member in the past 10 years (included)
        :return: dictionary. key: faculty number name; value: degree of excellence
        """
        last_ten_year = datetime.datetime.now().year - 10
        regs = []
        for _, v in self.top_conf_data.Venue.items():
            regs.append(self._venue_name_to_booktitle(v))
        reg = re.compile(f"({'|'.join([f'({r})' for r in regs])})$")
        excellence = dict()
        for k, v in self.auth_profiles.items():
            excellence[k] = 0
            publications = v['dblpperson']['r']
            if type(publications) is not list:
                article = publications[next(iter(publications))]
                if hasattr(article, 'booktitle') and reg.match(article.booktitle) and article.year >= last_ten_year:
                    excellence[k] += 1
            else:
                for pub in publications:
                    article = pub[next(iter(pub))]
                    if 'booktitle' in article and reg.match(article['booktitle']) and int(
                            article['year']) >= last_ten_year:
                        excellence[k] += 1
        return excellence

    def _get_names_in_rank(cls, rank_str: str) -> set:
        """
        return the names in a particular rank(position)
        :return: a set of faculty names
        """
        names = set()
        for index, row in cls.auth_name_data.iterrows():
            if row['Position'] == rank_str:
                names.add(row['Faculty'])
        if len(names) == 0:
            raise ValueError(f'Unexpected Rank Name {rank_str} Encountered!')
        return names

    @classmethod
    def filter_graph_by_names(cls, source_graphs: Union[nx.Graph, List[nx.Graph]],
                              faculty_names: Union[Set[str], List[str]]) -> Union[nx.Graph, List[nx.Graph]]:
        """
        Get subgraph(s) with the appointed nodes from the original graph(s)
        :param source_graphs: the original complete graph(s)
        :param faculty_names: list of the faculty member names
        :return: networkx graph or list of graphs, depending on the number or source graph passed
        """
        if type(faculty_names) is not set:
            faculty_names = set(faculty_names)

        if type(source_graphs) is list:
            return [cls._get_subgraph(source_graph=g, node_names=faculty_names) for g in source_graphs]
        else:
            return cls._get_subgraph(source_graphs, faculty_names)

    def filter_graph_by_rank(self, source_graphs: Union[nx.Graph, List[nx.Graph]],
                             ranks: Union[Set[str], List[str]]) -> Union[nx.Graph, List[nx.Graph]]:
        """
        Get subgraph(s) that filter the nodes with the designated ranks
        :param source_graphs: the original complete graph(s)
        :param ranks: list of the faculty ranks, e.g.["Professor", "Assistant Professor"]
        :return: networkx graph or list of graphs, depending on the number or source graph passed
        """
        if type(ranks) is not set:
            ranks = set(ranks)
        faculty_names = set()
        for rank in ranks:
            faculty_names.update(self._get_names_in_rank(rank_str=rank))
        if type(source_graphs) is list:
            return [self._get_subgraph(source_graph=g, node_names=faculty_names) for g in source_graphs]
        else:
            return self._get_subgraph(source_graphs, faculty_names)

    @staticmethod
    def _get_subgraph(source_graph: nx.Graph, node_names: Set[str]) -> nx.Graph:
        unexpected_names = node_names - set(source_graph.nodes)
        if len(unexpected_names) != 0:
            print(f"Unexpected Name(s) {unexpected_names} Encountered: No Such Node(s) in the Source Graph")
        return nx.subgraph(source_graph, node_names)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def get_clustering_coeff(graph):
        """
        Return the clustering coefficient of the graph
        :param graph: a networkx graph object
        :return: a float number
        """
        clust_coeff = nx.average_clustering(graph)
        return clust_coeff

    @staticmethod
    def plot_degree_distribution_hist(g: nx.Graph, name=None) -> str:
        """
        Plot the degree distribution histogram for the graph.
        :param name: (optional) appoint a name to the generated image
        :param g: a networkx graph object
        :return file name of the saved picture
        """
        degrees = [g.degree(n) for n in g.nodes()]
        plt.hist(degrees)
        plt.xlabel("Degree")
        plt.ylabel("Number of People")
        plt.title("Degree Distribution Histogram")
        if name is not None:
            filename = f'{name}.png'
        else:
            filename = f'degree_distribution_his_{int(time.time())}.png'
        plt.savefig(osp.join(PICTURE_PATH, filename))
        return filename

    @staticmethod
    def plot_degree_distribution_loglog(g: nx.Graph, normalized=True, name=None) -> str:
        """
        Plot the log-log degree distribution for the graph.
        In this case, number of nodes are too small to show a beautiful plot.
        :param name: optional) appoint a name to the generated image
        :param g: a networkx graph object
        :param normalized: default true
        :return file name of the saved picture
        """
        aux_y = nx.degree_histogram(g)
        aux_x = np.arange(0, len(aux_y)).tolist()
        n_nodes = g.number_of_nodes()
        if normalized:
            for i in range(len(aux_y)):
                aux_y[i] = aux_y[i] / n_nodes
        plt.loglog(aux_x, aux_y)
        plt.xlabel("k")
        plt.ylabel("P(k)")
        plt.title("Degree Distribution Loglog")
        if name is not None:
            filename = f'{name}.png'
        else:
            filename = f'degree_distribution_loglog_{int(time.time())}.png'
        plt.savefig(osp.join(PICTURE_PATH, filename))
        return filename

    @staticmethod
    def _highest_centrality(cent_dict: dict):
        """
        Returns a tuple (node,value) with the node
        with largest value from Networkx centrality dictionary.
        """
        # Create ordered tuple of centrality data
        cent_items = [(b, a) for (a, b) in cent_dict.items()]
        # Sort in descending order
        cent_items.sort()
        cent_items.reverse()
        return tuple(reversed(cent_items[0]))

    def analyze_centrality_of_main_component(self, g: nx.Graph):
        """
        Compute node centrality measures after
        extracting the main connected component.
        :param g: graph
        :return:
        """
        g_ud = g.to_undirected()
        components = nx.connected_components(g_ud)
        max_component = max(components, key=len)
        graph_mc = g_ud.subgraph(max_component)
        # bet_cen = {}
        # Betweenness centrality
        bet_cen = nx.betweenness_centrality(graph_mc)
        print("Node with highest betweenness centrality: ",
              self._highest_centrality(bet_cen))
        # Closeness centrality
        clo_cen = nx.closeness_centrality(graph_mc)
        print("Node with highest closeness centrality: ",
              self._highest_centrality(clo_cen))
        # Eigenvector centrality
        eig_cen = nx.eigenvector_centrality(graph_mc)
        print("Node with highest eigenvector centrality: ",
              self._highest_centrality(eig_cen))


if __name__ == '__main__':
    analyzer = Analyzer()
    G = generate_graph(name_data=analyzer.auth_name_data, profile_data=analyzer.auth_profiles)
    analyzer.plot_degree_distribution_loglog(G, normalized=True)
    # analyzer.analyze_centrality_of_main_component(G[10])
    # analyzer.plot_degree_distribution_hist(G[5])
    # subgraphs = analyzer.filter_graph_by_names(G, ['Miao Chunyan', 'Tan Rui', 'Wen Yonggang', 'AAAA'])
    # subgraphs = analyzer.filter_graph_by_rank(G, {'Professor','Lecturer'})
    # visualize_graphs(tags=T, graphs=subgraphs, port=get_free_port())
