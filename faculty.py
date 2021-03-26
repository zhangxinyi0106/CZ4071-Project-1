import time
from typing import Set
from collections import Counter
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
        for name, attribute in source_graphs[-1].nodes(data=True):
            if attribute["Position"] in ranks:
                faculty_names.add(name)
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
    def get_largest_component_diameter(graph: nx.Graph):
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
        subgraph = graph.subgraph(largest_component)
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
        fig, ax = plt.subplots()
        degrees = [d for _, d in g.degree()]
        ax.hist(degrees, bins=np.arange(max(degrees) + 2) - 0.5, density=False)

        for rect in ax.patches:
            height = rect.get_height()
            ax.annotate(f'{int(height)}', xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2), textcoords='offset points', ha='center', va='bottom', fontsize=6)

        plt.xlabel("Degree")
        plt.ylabel("Number of People")
        plt.xticks(range(0, max(degrees) + 1))
        plt.title("Degree Distribution Histogram")
        if name is not None:
            filename = f'{name}.png'
        else:
            filename = f'degree_distribution_his_{int(time.time())}.png'
        plt.savefig(osp.join(PICTURE_PATH, filename))
        return filename

    @staticmethod
    def plot_degree_distribution_loglog(g: nx.Graph, normalized=False, name=None) -> str:
        """
        Plot the log-log degree distribution for the graph.
        In this case, number of nodes are too small to show a beautiful plot.
        :param name: optional) appoint a name to the generated image
        :param g: a networkx graph object
        :param normalized: default False
        :return file name of the saved picture
        """
        aux_y = nx.degree_histogram(g)
        aux_x = np.arange(0, len(aux_y)).tolist()
        n_nodes = g.number_of_nodes()
        if normalized:
            for i in range(len(aux_y)):
                aux_y[i] = aux_y[i] / n_nodes
        plt.figure()
        ax = plt.gca()
        ax.plot(aux_x, aux_y, marker='o', linewidth=0)
        ax.set_yscale('log')
        ax.set_xscale('log')
        plt.xlabel("k")
        plt.ylabel("P(k)")
        plt.title("Degree Distribution Log-log Plot")
        if name is not None:
            filename = f'{name}.png'
        else:
            filename = f'degree_distribution_loglog_{int(time.time())}.png'
        plt.savefig(osp.join(PICTURE_PATH, filename))
        return filename

    @staticmethod
    def _sort_centrality(cent_dict: dict):
        """
        Returns a tuple (node,value) with the node
        with largest value from Networkx centrality dictionary.
        """
        # Create ordered tuple of centrality data
        return sorted(list(cent_dict.items()), key=lambda x: x[1], reverse=True)

    def analyze_centrality_of_main_component(self, g: nx.Graph) -> dict:
        """
        Compute node centrality measures after extracting the main connected component.
        :param g: graph
        :return: dictionary with type of centrality as key and sorted result as value
        """
        g_ud = g.to_undirected()
        components = nx.connected_components(g_ud)
        max_component = max(components, key=len)
        graph_mc = g_ud.subgraph(max_component)

        # Betweenness centrality
        bet_cen = nx.betweenness_centrality(graph_mc)
        # Closeness centrality
        clo_cen = nx.closeness_centrality(graph_mc)
        # Eigenvector centrality
        eig_cen = nx.eigenvector_centrality(graph_mc)

        return dict(
            betweenness_centrality=self._sort_centrality(bet_cen),
            closeness_centrality=self._sort_centrality(clo_cen),
            eigenvector_centrality=self._sort_centrality(eig_cen),
        )

    def detect_preferential_attachment(self, graphs: List[nx.Graph]):
        # TODO: use formulas presented in W5 slides
        pass

    @staticmethod
    def get_colab_properties(graphs: List[nx.Graph]):
        """
        Given a list of graphs, return multiple collaboration related properties
        :param graphs:
        :return: in sequence: number of partners, total number of collab papers, total number of published venues,
         most frequent venues (all graph-wise)
        """
        total_num_of_partners = [graph.number_of_edges() for graph in graphs]
        total_num_of_papers = [int(graph.size(weight="weight")) for graph in graphs]
        total_num_of_venues = []
        most_frequent_venues = []
        for graph in graphs:
            total_venues = []
            for _, attributes in graph.nodes(data=True):
                total_venues += (list(attributes["Colab_Venues"]))

            total_num_of_venues.append(len(set(total_venues)))
            most_frequent_venues.append(sorted([(venue, frequency // 2) for (venue, frequency)
                                                in Counter(total_venues).items()], key=lambda x: x[1], reverse=True))
        return total_num_of_partners, total_num_of_papers, total_num_of_venues, most_frequent_venues

    @classmethod
    def get_relative_colab_weight(cls, sub_graphs: List[nx.Graph], complete_graphs: List[nx.Graph]):
        """
        Given a list of sub-graphs and complete graphs, return the weight of sub-graphs
         in complete graphs on multiple collaboration related properties
        :param complete_graphs:
        :param sub_graphs:
        :return: in sequence: relative number of partners, relative number of collab papers,
         relative number of published venues
        """
        sub_graphs_colab_properties = cls.get_colab_properties(sub_graphs)
        complete_graphs_colab_properties = cls.get_colab_properties(complete_graphs)

        return [[sub / total for sub, total in zip(sub_graphs_colab_properties[i],
                                                   complete_graphs_colab_properties[i])] for i in range(0, 3)]


if __name__ == '__main__':
    analyzer = Analyzer()

    # G = generate_graph(name_data=analyzer.auth_name_data, profile_data=analyzer.auth_profiles)
    # analyzer.plot_degree_distribution_hist(G)
    # analyzer.plot_degree_distribution_loglog(G, normalized=False)

    _, G = generate_graphs(name_data=analyzer.auth_name_data, profile_data=analyzer.auth_profiles)
    sub_G = analyzer.filter_graph_by_rank(G, {'Professor'})
    relative_weight = analyzer.get_relative_colab_weight(sub_G, G)
    print(relative_weight[0])  # num of partners / total num of partners
    # betweenness_centrality = analyzer.analyze_centrality_of_main_component(G)["betweenness_centrality"]
    # print(betweenness_centrality)
    # analyzer.get_colab_properties(graphs=G)
    # subgraphs = analyzer.filter_graph_by_names(G, ['Miao Chunyan', 'Tan Rui', 'Wen Yonggang', 'AAAA'])
    # subgraphs = analyzer.filter_graph_by_rank(G, {'Professor','Lecturer'})
    # visualize_graphs(tags=T, graphs=subgraphs, port=get_free_port())
