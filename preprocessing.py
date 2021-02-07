import os.path as osp
import pickle
import re
from typing import Union

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
            # noinspection PyBroadException
            try:
                true_url = requests.get(url).url  # sometimes .xml will be converted to .html after redirection
                true_url = re.sub(r'(?<=\.)html$', 'xml', true_url)
                profile_in_xml = requests.get(true_url).content
                profile_data[name_list[i]] = xmltodict.parse(profile_in_xml, dict_constructor=dict)
                pbar.update(1)
            except:
                print(f'url {url} not fetched!')
                continue

    with open(osp.join(DATA_PATH, f'{target_pickle_name if target_pickle_name is not None else "profiles"}.pickle'),
              'wb') as f:
        pickle.dump(profile_data, f)

    return profile_data


def _append_co_auther_to_graph(authors: list, pid: str, pid_to_name: dict, faculty_member_name: str, graph) -> None:
    """
    connect nodes or modify the weight of edges based on the co_author relationship
    :param authors:
    :param pid:
    :param pid_to_name:
    :param faculty_member_name:
    :param graph:
    :return:
    """
    for co_auther in authors:
        co_pid = co_auther['@pid']
        if co_pid == pid:
            continue
        elif co_pid in pid_to_name.keys():
            co_name = pid_to_name[co_pid]
            # TODO: make it directional
            if (faculty_member_name, co_name) in list(graph.edges):
                graph[faculty_member_name][co_name]['weight'] += 1
            elif (co_name, faculty_member_name) in list(graph.edges):
                graph[co_name][faculty_member_name]['weight'] += 1
            else:
                graph.add_edge(faculty_member_name, co_name, weight=1)


def _validate_article(article: dict, till_year: Union[int, None]) -> list:
    """
    validate the article by its year and existence of co_authors
    :param article: article to be inspected
    :param till_year: (included) data till witch year that the graph should present
    :return: co_author list; empty when the article is invalid
    """
    if till_year is not None and int(article['year']) > till_year:
        return []
    authors = article['author'] if 'author' in article.keys() else article['editor']
    if type(authors) is not list:
        return []
    return authors


def generate_graph(name_data: pd.DataFrame, profile_data: dict, till_year: int = None,
                   faculty_member_only=True) -> nx.Graph:
    """
    construct a graph from the given faculty list and dblp data
    :param name_data:
    :param profile_data:
    :param till_year: (included) data till witch year that the graph should present
    :param faculty_member_only: True if excluding all other non-SCSE co-authors
    :return: graph
    """
    # TODO: add non-faculty member co_authors
    if not faculty_member_only:
        raise NotImplementedError

    graph = nx.Graph()

    # add nodes
    pid_to_name = dict()
    for name in name_data.Faculty.unique():
        properties = name_data.loc[name_data['Faculty'] == name].drop("Faculty", 1).squeeze().to_dict()
        graph.add_node(name, **properties)
        pid_to_name[profile_data[name]['dblpperson']['@pid']] = name

    print("Constructing Graph...")

    with tqdm(total=len(profile_data.items())) as pbar:
        for k, v in profile_data.items():
            pid = v['dblpperson']['@pid']
            publications = v['dblpperson']['r']
            if type(publications) is not list:
                article = publications[next(iter(publications))]
                authors = _validate_article(article=article, till_year=till_year)
                if len(authors) >= 2:
                    _append_co_auther_to_graph(authors=authors, pid=pid, pid_to_name=pid_to_name, faculty_member_name=k,
                                               graph=graph)
            else:
                for pub in publications:
                    article = pub[next(iter(pub))]
                    authors = _validate_article(article=article, till_year=till_year)
                    if len(authors) >= 2:
                        _append_co_auther_to_graph(authors=authors, pid=pid, pid_to_name=pid_to_name,
                                                   faculty_member_name=k,
                                                   graph=graph)
            pbar.update(1)

    # remove repeated counting (undirected)
    for _, _, a in graph.edges(data=True):
        a['weight'] //= 2

    return graph


def visualize_graph(graph: nx.Graph) -> None:
    """
    Plot networkx graph with plotly. Modified from the internet
    :param graph: graph to be plotted
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
        related_papers = 0
        for prop in adjacencies[1].values():
            related_papers += prop['weight']
        node_total_edge_weight.append(related_papers)
        properties = '<br />'.join(['%s: %s' % (k, v) for (k, v) in graph.nodes[adjacencies[0]].items()])
        node_text.append(
            f'{adjacencies[0]}<br />Degree: {len(adjacencies[1].keys())}<br />'
            f'Related Papers: {related_papers}<br />{properties}')

    node_trace.marker.color = node_total_edge_weight
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace, eweights_trace],
                    layout=go.Layout(
                        title='NTU SCSE Faculty Member Graph',
                        height=900,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    app = dash.Dash(__name__)

    app.layout = html.Div([
        dcc.Graph(id="graph", figure=fig),
    ], style={'height': "100vh"}, )

    app.run_server(debug=False, port=8080)


if __name__ == '__main__':
    auth_name_data = read_faculty()
    auth_profiles = fetch_dblp_profile(auth_name_data=auth_name_data, reuse=True, target_pickle_name='profiles')
    graph = generate_graph(auth_name_data, auth_profiles, till_year=None)
    visualize_graph(graph)
