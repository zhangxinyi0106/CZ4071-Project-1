from typing import Set

from preprocessing import *


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

    @staticmethod
    def _get_subgraph(source_graph: nx.Graph, node_names: Set[str]) -> nx.Graph:
        unexpected_names = node_names - set(source_graph.nodes)
        if len(unexpected_names) != 0:
            print(f"Unexpected Name(s) {unexpected_names} Encountered: No Such Node(s) in the Source Graph")
        return nx.subgraph(source_graph, node_names)


if __name__ == '__main__':
    analyzer = Analyzer()
    T, G = generate_graphs(name_data=analyzer.auth_name_data, profile_data=analyzer.auth_profiles)
    subgraphs = analyzer.filter_graph_by_names(G, ['Miao Chunyan', 'Tan Rui', 'Wen Yonggang', 'AAAA'])
    visualize_graphs(tags=T, graphs=subgraphs, port=get_free_port())
