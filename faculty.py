import time
from typing import Set
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from preprocessing import *
from pictures import PICTURE_PATH


class Collaborator:
    def __init__(self, pid: str, name: str):
        self.pid = pid
        self.name = name
        self.partner = set()
        self.collab_paper = set()
        self.score = 0


class Analyzer:
    venue_to_booktitle = dict({  # ignore all workshop papers
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
        self.area_to_top_booktitle = self._area_name_to_booktitle()
        self.auth_excellence = self._get_auth_excellence()
        self.external_collaborators = self._get_all_external_collaborators()
        self.external_collaborators_profiles = None
        self.external_collaborators_excellence = None

    def _area_name_to_booktitle(self):
        """
        return the the regular expression code of the top conferences
        :return: dict of area to conference code (book title)
        """
        area_to_code = dict()
        for _, row in self.top_conf_data.iterrows():
            area_name, top_conf = row.Area, row.Venue
            try:
                reg = self._venue_name_to_booktitle(top_conf)
            except Exception as e:
                print(str(e))
                reg = top_conf.lower()
                print(f"Using Name {reg} as Regular Expression...")

            if area_name not in area_to_code:
                area_to_code[area_name] = reg
            else:
                area_to_code[area_name] += '|' + reg

        if "Software Engineering" in area_to_code:
            area_to_code["Software Engg"] = area_to_code["Software Engineering"]

        return area_to_code

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

    def _get_auth_excellence(self, external=False) -> dict:
        """
        count the number of paper published in the respective top conferences
        by each faculty member in the past 10 years (included)
        :return: dictionary. key: faculty number name; value: degree of excellence
        """
        last_ten_year = datetime.datetime.now().year - 10  # in the last 10 years

        general_reg = re.compile(f"({'|'.join([f'({r})' for r in self.area_to_top_booktitle.values()])})$")

        excellence = dict()

        if external:
            profile = self.external_collaborators_profiles
        else:
            profile = self.auth_profiles

        for k, v in profile.items():
            if external:
                reg = general_reg
            else:
                area = self.auth_name_data[self.auth_name_data.Faculty == k].Area.to_string(index=False)
                if area not in self.area_to_top_booktitle:
                    print(f"Unexpected Area {area} Encountered! Matching All Top Conferences Instead...")
                    reg = general_reg
                else:
                    reg = re.compile(f"{self.area_to_top_booktitle[area]}$")  # in his/her respective area

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
        nodes_from_graph = source_graphs[-1] if (type(source_graphs) is list) else source_graphs
        for name, attribute in nodes_from_graph.nodes(data=True):
            if attribute["Position"] in ranks:
                faculty_names.add(name)
        if type(source_graphs) is list:
            return [self._get_subgraph(source_graph=g, node_names=faculty_names) for g in source_graphs]
        else:
            return self._get_subgraph(source_graphs, faculty_names)

    def filter_graph_by_area(self, source_graphs: Union[nx.Graph, List[nx.Graph]],
                             areas: Union[Set[str], List[str]]) -> Union[nx.Graph, List[nx.Graph]]:
        """
        Get subgraph(s) that filter the nodes with the designated areas
        """
        if type(areas) is not set:
            areas = set(areas)
        faculty_names = set()
        nodes_from_graph = source_graphs[-1] if (type(source_graphs) is list) else source_graphs
        for name, attribute in nodes_from_graph.nodes(data=True):
            if attribute["Area"] in areas:
                faculty_names.add(name)
        if type(source_graphs) is list:
            return [self._get_subgraph(source_graph=g, node_names=faculty_names) for g in source_graphs]
        else:
            return self._get_subgraph(source_graphs, faculty_names)

    def filter_graph_by_managerole(self, source_graphs: Union[nx.Graph, List[nx.Graph]],
                             is_management: bool) -> Union[nx.Graph, List[nx.Graph]]:
        """
        Get subgraph(s) that filter the nodes for managerial role faculty
        :param source_graphs: the original complete graph(s)
        :param is_management: specify the subgraoh would only contain management role faculty or not
        :return: networkx graph or list of graphs, depending on the number or source graph passed
        """
        faculty_names = set()
        nodes_from_graph = source_graphs[-1] if (type(source_graphs) is list) else source_graphs
        for name, attribute in nodes_from_graph.nodes(data=True):
            if is_management:
                if attribute["Management"] == 'Y':
                    faculty_names.add(name)
            else:
                if attribute["Management"] == 'N':
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

    @classmethod
    def plot_avg_degree_hist(cls, graphs: List[nx.Graph], tags: List[str], name=None) -> str:
        """
        Plot average degree by year
        :param graphs:
        :param tags: year in sequence
        :param name:
        :return: file name of the saved picture
        """
        fig, ax = plt.subplots()
        y = [cls.get_avg_degree(graph) for graph in graphs]
        x = range(len(tags))
        return cls._plot_line(x, y, tags, "Year", "Average Node Degree", "Average Node Degree by Year",
                              name if name is not None else f'avg_degree_plot_{"{:.5f}".format(time.time())}',
                              ax, plt)

    @classmethod
    def plot_avg_clust_coeff_hist(cls, graphs: List[nx.Graph], tags: List[str], name=None) -> str:
        """
        Plot average clustering coefficient by year
        :param graphs:
        :param tags: year in sequence
        :param name:
        :return: file name of the saved picture
        """
        fig, ax = plt.subplots()
        y = [cls.get_clustering_coeff(graph) for graph in graphs]
        x = range(len(tags))
        return cls._plot_line(x, y, tags, "Year", "Average Clustering Coefficient",
                              "Average Clustering Coefficient by Year",
                              name if name is not None else f'avg_clust_coeff_{"{:.5f}".format(time.time())}',
                              ax, plt)

    @classmethod
    def plot_diameter_hist(cls, graphs: List[nx.Graph], tags: List[str], name=None) -> str:
        """
        Plot the diameter of the largest component of the graph by year
        :param graphs:
        :param tags: year in sequence
        :param name:
        :return: file name of the saved picture
        """
        fig, ax = plt.subplots()
        y = [cls.get_largest_component_diameter(graph) for graph in graphs]
        x = range(len(tags))
        return cls._plot_line(x, y, tags, "Year", "Diameter (Largest Component)",
                              "Diameter (Largest Component) by Year",
                              name if name is not None else f'diameter_{"{:.5f}".format(time.time())}',
                              ax, plt)

    @staticmethod
    def _plot_line(x, y, x_ticks, x_label, y_label, title, figname, ax, plt):
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(x_ticks, rotation='vertical')
        ax.plot(x, y)
        filename = f'{figname}.png'
        plt.savefig(osp.join(PICTURE_PATH, filename))
        return filename

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
            filename = f'degree_distribution_his_{"{:.5f}".format(time.time())}.png'
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
            filename = f'degree_distribution_loglog_{"{:.5f}".format(time.time())}.png'
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

    @staticmethod
    def get_degree_increase(graphs: List[nx.Graph]):
        ptr = 0
        length = len(graphs)
        delta_degrees = []
        while ptr <= length - 2:
            current_graph = graphs[ptr]
            next_graph = graphs[ptr + 1]

            delta_degree = dict()
            for node, degree in current_graph.degree():
                if degree not in delta_degree:
                    delta_degree[degree] = [next_graph.degree(node) - degree]
                else:
                    delta_degree[degree].append(next_graph.degree(node) - degree)

            delta_degrees.append(delta_degree)

            ptr += 1

        return delta_degrees

    @staticmethod
    def detect_preferential_attachment(graphs: List[nx.Graph], average=False):
        ptr = 0
        length = len(graphs)
        delta_degrees = []
        while ptr <= length - 2:
            current_graph = graphs[ptr]
            next_graph = graphs[ptr + 1]

            delta_degree = dict()
            for node, degree in current_graph.degree():
                increased_degree = next_graph.degree(node)
                if degree == 0 and increased_degree != 0:  # this is a newly joined node, check its adj
                    for connected_node in list(next_graph[node].keys()):
                        connected_node_original_degee = current_graph.degree(connected_node)
                        if connected_node_original_degee not in delta_degree:
                            delta_degree[connected_node_original_degee] = 1
                        else:
                            delta_degree[connected_node_original_degee] += 1

            delta_degrees.append(delta_degree)

            ptr += 1

        return delta_degrees

    @staticmethod
    def visualize_degree_increase(delta_degree_dist: dict, name=None):
        fig, ax = plt.subplots()
        y_data = []
        x_data = list(range(0, max(delta_degree_dist.keys()) + 1))
        for i in x_data:
            if i in delta_degree_dist:
                y_data.append(delta_degree_dist[i])
            else:
                y_data.append([0])

        ax.boxplot(y_data, showmeans=True)
        plt.xticks(list(range(1, max(delta_degree_dist.keys()) + 2)), x_data)

        plt.xlabel("Degree")
        plt.ylabel("Delta Degree / Delta Time")
        plt.title("Degree Increase Analysis")
        if name is not None:
            filename = f'{name}.png'
        else:
            filename = f'degree_increase_analysis_{"{:.5f}".format(time.time())}.png'
        plt.savefig(osp.join(PICTURE_PATH, filename))
        return filename

    @staticmethod
    def visualize_preferential_attachment(delta_degree_dist: dict, name=None):
        if not delta_degree_dist:
            raise ValueError('No New Nodes Joint The Collab Graph In That Year')
        fig, ax = plt.subplots()
        y_data = []
        x_data = list(range(0, max(delta_degree_dist.keys()) + 1))
        for i in x_data:
            if i in delta_degree_dist:
                y_data.append(delta_degree_dist[i])
            else:
                y_data.append(0)

        ax.scatter(x_data, y_data)
        plt.xticks(x_data)
        plt.yticks(range(0, max(y_data) + 2))

        plt.xlabel("Degree")
        plt.ylabel("Number Of New Comers Attached")
        plt.title("Preferential Attachment Analysis")
        if name is not None:
            filename = f'{name}.png'
        else:
            filename = f'preferential_attachment_analysis_{"{:.5f}".format(time.time())}.png'
        plt.savefig(osp.join(PICTURE_PATH, filename))
        return filename

    @staticmethod
    def get_colab_properties(graphs: List[nx.Graph]):
        """
        Given a list of graphs, return multiple collaboration related properties
        :param graphs:
        :return: in sequence: number of partners, total number of collab papers, total number of published venues,
         most frequent venues (all graph-wise)
        """
        total_num_of_partners = [graph.number_of_edges() for graph in graphs]
        total_num_of_papers = []
        for graph in graphs:
            total_papers = set()
            for _, _, a in graph.edges(data=True):
                total_papers |= a["paper"]
            total_num_of_papers.append(len(total_papers))
        total_num_of_venues = []
        most_frequent_venues = []
        for graph in graphs:
            total_venues = dict()
            for _, attributes in graph.nodes(data=True):
                total_venues.update(attributes["Colab_Venues"])

            total_num_of_venues.append(len(set(total_venues.values())))
            most_frequent_venues.append(sorted(list(Counter(total_venues.values()).items()), key=lambda x: x[1],
                                               reverse=True))
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

    def get_correlation(self, a: Union[list, dict], b: Union[list, dict], method: str = 'pearson'):
        """
        get the correlation between two criteria (e.g. betweeness centrality v.s. node excellence)
        :param a: sorted list or dictionary by criteria one
        :param b: sorted list or dictionary by criteria two
        :param method: default pearson correlation
        :return: correlation between a and b
        """
        if type(a) is list:
            a = self._convert_sorted_list_to_dict(a)
        if type(b) is list:
            b = self._convert_sorted_list_to_dict(b)

        key_intersection = set(a.keys()).intersection(b.keys())

        df = pd.DataFrame([(a[k], b[k]) for k in key_intersection], columns=['a', 'b'])
        return df.corr(method=method)['a']['b']

    @staticmethod
    def _convert_sorted_list_to_dict(sorted_list: list) -> dict:
        result = dict()
        for pair in sorted_list:
            if pair[0] in result:
                print(f"Duplicated Key {pair[0]} Detected! Overwriting...")
            result[pair[0]] = pair[1]
        return result

    @staticmethod
    def calculate_growth(data: list) -> list:
        """
        return the delta value for each element in the data list with regard to its previous element
        :param data: list to be calculated
        :return: list with the first element as '-'
        """
        return ['{}'.format(data[i] - data[i - 1]) if i >= 1 and data[i - 1] != 0 else '-'
                for i in range(0, len(data))]

    @staticmethod
    def calculate_growth_in_percentage(data: list) -> list:
        """
        return the relative growth in percentage for each element in the data list, comparing with its previous element
        :param data: list to be calculated
        :return: list with the first element as '-'
        """
        return ['{:.2f}%'.format((data[i] - data[i-1]) / data[i-1] * 100) if i >= 1 and data[i-1] != 0 else '-'
                for i in range(0, len(data))]

    def _get_all_external_collaborators(self) -> list:
        """
        get the name list of all external collaborators of faculty members
        :return: sorted list of Collaborators object based on the hard-coded algorithm
        """
        faculty_pids = set({v['dblpperson']['@pid'] for v in self.auth_profiles.values()})

        collaborator_list = dict()

        for k, v in self.auth_profiles.items():
            publications = v['dblpperson']['r']
            if type(publications) is not list:
                publications = [publications]

            for pub in publications:
                article = pub[next(iter(pub))]
                authors = article['author'] if 'author' in article.keys() else article['editor']

                if type(authors) is not list:
                    continue

                for co_auther in authors:
                    co_pid = co_auther['@pid']
                    if co_pid in faculty_pids:
                        continue
                    else:
                        if co_pid not in collaborator_list:
                            collaborator_list[co_pid] = Collaborator(co_pid, co_auther["#text"])

                        collaborator_list[co_pid].partner.add(k)
                        collaborator_list[co_pid].collab_paper.add(article["@key"])

        avg_paper_per_partner = sum([len(c.collab_paper) / len(c.partner) for c in collaborator_list.values()]) \
                                / len(collaborator_list)

        for c in collaborator_list.values():
            c.score = len(c.collab_paper) + avg_paper_per_partner * len(c.partner)

        return sorted(collaborator_list.values(), key=lambda e: e.score, reverse=True)

    def _get_external_collaborators_profile(self, top: int, reuse: bool, target_pickle_name: str) -> dict:
        """
        fetch the candidate collaborator profiles from dblp
        :param top: number of top candidates to be fetched
        :param reuse: reusing old ceche data
        :param target_pickle_name: target cache data name
        :return: external collaborator profiles in dictionary format; the same as faculty profile
        """
        if top is not None:
            assert top > 0, 'Invalid Cut-off!'
            candidate_collaborators = self.external_collaborators[:top]
        else:
            candidate_collaborators = self.external_collaborators

        name_data = []
        for c in candidate_collaborators:
            name_data.append([c.name, f"http://dblp.org/pid/{c.pid}.xml"])
        name_data = pd.DataFrame(name_data, columns=["Faculty", "DBLP"])
        profile_data = fetch_dblp_profile(auth_name_data=name_data, reuse=reuse, target_pickle_name=target_pickle_name)

        return profile_data

    def use_external_collaborators_profiles(self, top=2000, reuse=True, target_pickle_name="external_profiles"):
        """
        load the external collaborators profiles; used when the adding new faculty member function is needed
        :param top: number of top candidates to be fetched
        :param reuse: reusing old ceche data
        :param target_pickle_name: target cache data name
        :return: None; stored in the analyzer object
        """
        assert top >= 1000, "At least 1000 is required!"

        if self.external_collaborators_profiles is None:
            self.external_collaborators_profiles = self._get_external_collaborators_profile(top, reuse,
                                                                                            target_pickle_name)
        if self.external_collaborators_excellence is None:
            self.external_collaborators_excellence = self._get_auth_excellence(external=True)

    def get_new_member_profile(self, based_on_excellece=True):
        """
        get the profiles of the chosen 1000 new faculty candidates
        :param based_on_excellece: True if to consider the new member's excellence
        :return: external collaborator profiles in dictionary format; the same as faculty profile
        """
        assert self.external_collaborators_profiles is not None, \
            "Please call use_external_collaborators_profiles first to load the profiles!"

        if based_on_excellece:
            name_list = [k for k, _ in sorted(self.external_collaborators_excellence.items(),
                                              key=lambda item: item[1], reverse=True)][:1000]
        else:
            name_list = [c.name for c in self.external_collaborators[:1000]]

        return {n: self.external_collaborators_profiles[n] for n in name_list}


if __name__ == '__main__':
    """
    This is just for quick testing and not supposed to be run cons
    """
    analyzer = Analyzer()
    analyzer.use_external_collaborators_profiles(top=2000)
    external_profiles = analyzer.get_new_member_profile(based_on_excellece=True)
    G_new = generate_graph(name_data=analyzer.auth_name_data, profile_data=analyzer.auth_profiles,
                           external_profile_data=external_profiles)
    visualize_graph(G_new)

    # print(analyzer.auth_excellence)
    G = generate_graph(name_data=analyzer.auth_name_data, profile_data=analyzer.auth_profiles, by_year=2021)
    # visualize_graph(G)
    closeness_centrality = analyzer.analyze_centrality_of_main_component(G)["closeness_centrality"]
    print(analyzer.get_correlation(closeness_centrality, analyzer.auth_excellence))
    # G_test = analyzer.filter_graph_by_area(G, ['AI/ML', 'Computer Vision'])
    # visualize_graph(G_test, port=get_free_port())
    # for i in range(1999, 2021):
    #     G = generate_graph(name_data=analyzer.auth_name_data, profile_data=analyzer.auth_profiles, by_year=i)
    #     print("year: ", i)
    #     print("average degree:", analyzer.get_avg_degree(G))
    #     print("diameter:", analyzer.get_largest_component_diameter(G))
    #     print("clustering coeff:", analyzer.get_clustering_coeff(G))

    # analyzer.plot_degree_distribution_hist(G)
    # filename = analyzer.plot_degree_distribution_loglog(G, normalized=False)
    # print("filename:", filename)
    # T, G = generate_graphs(name_data=analyzer.auth_name_data, profile_data=analyzer.auth_profiles)
    # analyzer.get_colab_properties(G)
    # analyzer.plot_avg_degree_hist(G, T)
    # analyzer.plot_avg_clust_coeff_hist(G, T)
    # analyzer.plot_diameter_hist(G, T)
    # new_attachment_by_degree_data = analyzer.detect_preferential_attachment(G)
    # for i in range(0, len(new_attachment_by_degree_data)):
    #     try:
    #         analyzer.visualize_preferential_attachment(new_attachment_by_degree_data[i])
    #     except ValueError as e:
    #         print(str(e) + f' {i}')

    # delta_k_data = analyzer.get_degree_increase(G)
    # for i in range(0, len(delta_k_data)):
    #     analyzer.visualize_degree_increase(delta_k_data[i])

    # sub_G = analyzer.filter_graph_by_rank(G, {'Professor', "Associate Professor"})
    # relative_weight = analyzer.get_relative_colab_weight(sub_G, G)
    # print(relative_weight[0])  # num of partners / total num of partners
    # total_num_of_papers = analyzer.get_colab_properties(graphs=G)[1]
    # print(analyzer.calculate_growth_in_percentage(total_num_of_papers))
    # subgraphs = analyzer.filter_graph_by_names(G, ['Miao Chunyan', 'Tan Rui', 'Wen Yonggang', 'AAAA'])
    # subgraphs = analyzer.filter_graph_by_rank(G, {'Professor','Lecturer'})
    # visualize_graphs(tags=T, graphs=subgraphs, port=get_free_port())
