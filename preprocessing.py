import datetime
import os.path as osp
import pickle
import re
import socket
from typing import Union, List, Tuple

import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import requests
import xmltodict
from tqdm import tqdm

from data import DATA_PATH


def get_free_port():
    """
    get an unused port on the localhost
    :return: port number in integer format
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def _read_xlsx_file(path, filename, sheet_name, required_fields: set) -> pd.DataFrame:
    target_file = osp.join(path, filename)

    if not osp.exists(target_file):
        raise FileNotFoundError("the appointed file {} does not exist!".format(target_file))

    name_list = pd.read_excel(target_file, sheet_name=sheet_name)
    assert set(name_list.columns.values).issuperset(required_fields), \
        'Necessary fields are missing from the sheet!'

    # remove empty columns
    cols = [c for c in name_list.columns if not re.match('Unnamed', c)]
    name_list = name_list[cols]

    return name_list


def read_faculty(path=DATA_PATH, filename='Faculty.xlsx', sheet_name='by course') -> pd.DataFrame:
    """
    read the faculty member namelist
    :param sheet_name: name of the sheet
    :param filename: filename of the target name list
    :param path: directory of the name list
    :return: pandas dataframe
    """
    return _read_xlsx_file(path, filename, sheet_name,
                           required_fields={'Faculty', 'Position', 'Gender', 'Management', 'DBLP', 'Area'})


def read_top_conferences(path=DATA_PATH, filename='Top.xlsx', sheet_name='Sheet1') -> pd.DataFrame:
    """
    read the top conference namelist
    :param sheet_name: name of the sheet
    :param filename: filename of the target name list
    :param path: directory of the name list
    :return: pandas dataframe
    """
    return _read_xlsx_file(path, filename, sheet_name,
                           required_fields={'Area', 'Venue', 'Comments'})


def fetch_dblp_profile(auth_name_data, reuse=False, target_pickle_name=None) -> dict:
    """
    Fetch dblp personal profiles given a name list
    :param auth_name_data: a name list containing urls with faculty information
    :param reuse: True if to read from pickle directly
    :param target_pickle_name: target pickle, used when reuse == True
    :return: dictionary with name as key
    """
    if reuse:
        assert target_pickle_name is not None, 'Please specify a pickle to use'
        try:
            with open(osp.join(DATA_PATH, f'{target_pickle_name}.pickle'), 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("Target pickle not found! Re-retrieving data...")

    url_list = list(auth_name_data['DBLP'])
    name_list = list(auth_name_data['Faculty'])
    assert len(set(name_list)) == len(name_list), 'Duplicated names found!'

    profile_data = dict()
    with tqdm(total=len(url_list)) as pbar:
        for i, url in enumerate(url_list):
            try:
                true_url = requests.get(url).url  # sometimes .xml will be converted to .html after redirection
                true_url = re.sub(r'(?<=\.)html$', 'xml', true_url)
                profile_in_xml = requests.get(true_url).content
                profile_data[name_list[i]] = xmltodict.parse(profile_in_xml, dict_constructor=dict)
                pbar.update(1)
            except Exception as e:
                print(f'url {url} not fetched! {str(e)}')
                continue

    with open(osp.join(DATA_PATH, f'{target_pickle_name if target_pickle_name is not None else "profiles"}.pickle'),
              'wb') as f:
        pickle.dump(profile_data, f)

    return profile_data


def _append_co_auther_to_graph(authors: list, pid: str, pid_to_name: dict, faculty_member_name: str, graph, article) -> None:
    """
    connect nodes or modify the weight of edges based on the co_author relationship
    :param authors:
    :param pid:
    :param pid_to_name:
    :param faculty_member_name:
    :param graph:
    :return:
    """
    if "booktitle" in article:
        venue = article["booktitle"]
    elif "journal" in article:
        venue = article["journal"]
    else:
        venue = "Others"

    for co_auther in authors:
        co_pid = co_auther['@pid']
        if co_pid == pid:  # excluding himself
            continue
        elif co_pid in pid_to_name.keys():
            co_name = pid_to_name[co_pid]

            # duplicated paper will be overwrited
            if (faculty_member_name, co_name) in list(graph.edges):
                graph[faculty_member_name][co_name]['paper'][article["@key"]] = venue
            elif (co_name, faculty_member_name) in list(graph.edges):
                graph[co_name][faculty_member_name]['paper'][article["@key"]] = venue
            else:
                graph.add_edge(faculty_member_name, co_name, paper={article["@key"]: venue})


def _validate_article(article: dict, by_year: Union[int, None]) -> list:
    """
    validate the article by its year and existence of co_authors
    :param article: article to be inspected
    :param by_year: (included) data till witch year that the graph should present
    :return: co_author list; empty when the article is invalid
    """
    if by_year is not None and int(article['year']) > by_year:
        return []
    authors = article['author'] if 'author' in article.keys() else article['editor']
    if type(authors) is not list:
        return []
    return authors


def generate_graph(name_data: pd.DataFrame, profile_data: dict, by_year: int = None,
                   external_profile_data=None) -> nx.Graph:
    """
    construct a single graph from the given faculty list and dblp data with the appointed year
    :param name_data:
    :param profile_data:
    :param by_year: (included) data till witch year that the graph should present
    :param external_profile_data: (optional)profiles of all other non-SCSE co-authors
    :return: graph
    """
    graph = nx.Graph()

    # add nodes
    pid_to_name = dict()

    for name in name_data.Faculty.unique():
        properties = name_data.loc[name_data['Faculty'] == name].drop("Faculty", 1).squeeze().to_dict()
        graph.add_node(name, **properties)
        pid_to_name[profile_data[name]['dblpperson']['@pid']] = name

    if external_profile_data is not None:
        for name in external_profile_data.keys():
            properties = dict(External=True)
            graph.add_node(name, **properties)
            pid_to_name[external_profile_data[name]['dblpperson']['@pid']] = name
        profile_data = {**profile_data, **external_profile_data}

    print("Constructing Graph...")

    with tqdm(total=len(profile_data.items())) as pbar:
        for k, v in profile_data.items():
            pid = v['dblpperson']['@pid']
            publications = v['dblpperson']['r']
            if type(publications) is not list:
                article = publications[next(iter(publications))]
                authors = _validate_article(article=article, by_year=by_year)
                if len(authors) >= 2:
                    _append_co_auther_to_graph(authors=authors, pid=pid, pid_to_name=pid_to_name, faculty_member_name=k,
                                               graph=graph, article=article)
            else:
                for pub in publications:
                    article = pub[next(iter(pub))]
                    authors = _validate_article(article=article, by_year=by_year)
                    if len(authors) >= 2:
                        _append_co_auther_to_graph(authors=authors, pid=pid, pid_to_name=pid_to_name,
                                                   faculty_member_name=k,
                                                   graph=graph, article=article)
            pbar.update(1)

    # remove repeated counting (undirected)
    for _, _, a in graph.edges(data=True):
        a['weight'] = len(a['paper'])

    return graph


def generate_graphs(name_data: pd.DataFrame, profile_data: dict, till_year: int = None,
                    external_profile_data=None) -> Tuple[List[str], List[nx.Graph]]:
    """
    construct a list of graphs in sequence of years (e.g. [graph by 2000, graph by 2001 ..., graph by till_year])
    from the given faculty list and dblp data
    :param name_data:
    :param profile_data:
    :param till_year: (included) data till witch year that the graph should present. Default till the latest year.
    :param external_profile_data: (optional)profiles of all other non-SCSE co-authors
    :return: list of graphs
    """
    if till_year is None:
        till_year = datetime.datetime.now().year

    tags = []
    graphs = []
    for year in range(2000, till_year):
        tags.append(str(year))
        graphs.append(generate_graph(name_data=name_data, profile_data=profile_data,
                                     by_year=year, external_profile_data=external_profile_data))

    return tags, graphs


def visualize_graph(graph: nx.Graph, port: int = 8080) -> None:
    """
    Plot networkx graph with plotly. Modified from the internet
    :param graph: graph to be plotted
    :param port: port number for the server to be run, default 8080
    :return:
    """
    fig = _prepare_figure(graph)

    app = dash.Dash(__name__)

    app.layout = html.Div([
        dcc.Graph(id="graph", figure=fig, style={'height': '90vh'}),
    ], style={'height': "100%"}, )

    app.run_server(debug=False, port=port)


def visualize_graphs(tags: List[str], graphs: List[nx.Graph], port: int = 8080) -> None:
    """
    Plot networkx graph with plotly. Modified from the internet
    :param tags: name of the tags
    :param graphs: graph to be plotted
    :param port: port number for the server to be run, default 8080
    :return:
    """
    figs = []
    for graph in graphs:
        figs.append(_prepare_figure(graph))

    app = dash.Dash(__name__)

    app.layout = html.Div(html.Div([
        dcc.Tabs(
            [dcc.Tab(label=tag, children=[dcc.Graph(id=tag, figure=fig, style={'height': '90vh'})]) for tag, fig in
             zip(tags, figs)],
        )
    ]), style={'height': "100%"}, )

    app.run_server(debug=False, port=port)


def _prepare_figure(graph: nx.Graph) -> go.Figure:
    """
    Prepare plotly figure using the given graph
    :param graph:
    :return:
    """
    pos = nx.spring_layout(graph)
    edge_x = []
    edge_y = []
    etext = [f'{k[0]} - {k[1]}: {v} Related Paper(s)' for (k, v) in nx.get_edge_attributes(graph, 'weight').items()]
    xtext = []
    ytext = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        xtext.append((x0 + x1) / 2)
        ytext.append((y0 + y1) / 2)
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo=None,
        mode='lines')

    eweights_trace = go.Scatter(x=xtext, y=ytext,
                                mode='markers',
                                text=etext,
                                hovertemplate='%{text}<extra></extra>')

    node_x = []
    node_y = []
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Related Papers',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_total_edge_weight = []
    node_text = []
    for _, adjacencies in enumerate(graph.adjacency()):
        related_papers = set()
        for prop in adjacencies[1].values():
            related_papers |= set(prop['paper'].keys())
        node_total_edge_weight.append(len(related_papers))
        node_property_display = ['%s: %s' % (k, v) for k, v in graph.nodes[adjacencies[0]].items()]
        properties = '<br />'.join(node_property_display)
        node_text.append(
            f'{adjacencies[0]}<br />Degree: {len(adjacencies[1].keys())}<br />'
            f'Related Papers: {len(related_papers)}<br />{properties}')

    node_trace.marker.color = node_total_edge_weight
    node_trace.text = node_text

    return go.Figure(data=[edge_trace, node_trace, eweights_trace],
                     layout=go.Layout(
                         title='NTU SCSE Faculty Member Graph',
                         showlegend=False,
                         hovermode='closest',
                         margin=dict(b=20, l=5, r=5, t=40),
                         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                     )


if __name__ == '__main__':
    process_list = []

    try:
        from multiprocessing import Process

        auth_name_data = read_faculty()
        auth_profiles = fetch_dblp_profile(auth_name_data=auth_name_data, reuse=True, target_pickle_name='profiles')
        G1 = generate_graph(auth_name_data, auth_profiles)
        target_port_1 = get_free_port()
        p1 = Process(target=visualize_graph, kwargs={
            'graph': G1,
            'port': target_port_1,
        })
        process_list.append(p1)
        p1.start()

        T, G2 = generate_graphs(auth_name_data, auth_profiles)
        target_port_2 = get_free_port()
        p2 = Process(target=visualize_graphs, kwargs={
            'tags': T,
            'graphs': G2,
            'port': target_port_2,
        })
        process_list.append(p2)
        p2.start()

        p1.join()  # this two lines will hang cuz server won't stop by itself
        p2.join()
    except KeyboardInterrupt:
        for p in process_list:
            p.close()
