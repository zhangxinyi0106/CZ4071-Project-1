import os.path as osp
import re
import json
import pickle

import requests
import xmltodict
from tqdm import tqdm
import pandas as pd

from data import DATA_PATH


def _read_xlsx_file(path, filename, sheet_name, required_fields: set):
    target_file = osp.join(path, filename)

    if not osp.exists(target_file):
        raise FileNotFoundError("the appointed file {} does not exist!".format(target_file))

    name_list = pd.read_excel(target_file, sheet_name=sheet_name)
    assert set(name_list.columns.values).issuperset(required_fields),\
        'required fields are missing from the sheet!'
    return name_list


def read_faculty(path=DATA_PATH, filename='Faculty.xlsx', sheet_name='by course'):
    """
    read the faculty member namelist
    :param sheet_name: name of the sheet
    :param filename: filename of the target name list
    :param path: directory of the name list
    :return: pandas dataframe
    """
    return _read_xlsx_file(path, filename, sheet_name,
                           required_fields={'Faculty', 'Position', 'Gender', 'Management', 'DBLP', 'Area'})


def read_top_conferences(path=DATA_PATH, filename='Top.xlsx', sheet_name='Sheet1'):
    """
    read the top conference namelist
    :param sheet_name: name of the sheet
    :param filename: filename of the target name list
    :param path: directory of the name list
    :return: pandas dataframe
    """
    return _read_xlsx_file(path, filename, sheet_name,
                           required_fields={'Area', 'Venue', 'Comments'})


def fetch_dblp_profile(auth_name_list, reuse=False, target_pickle_name=None):
    """
    Fetch dblp personal profiles given a name list
    :param auth_name_list: a name list containing urls
    :param reuse: True if to read from pickle directly
    :param target_pickle_name: target pickle, used when reuse == True
    :return: list of dict
    """
    if reuse:
        assert target_pickle_name is not None, 'Please specify a pickle to use'
        try:
            with open(osp.join(DATA_PATH, f'{target_pickle_name}.pickle'), 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("Target pickle not found! Re-retrieving data...")

    url_list = list(auth_name_list['DBLP'])
    profile_list = []
    with tqdm(total=len(url_list)) as pbar:
        for url in url_list:
            # noinspection PyBroadException
            try:
                true_url = requests.get(url).url  # sometimes .xml will be converted to .html after redirection
                true_url = re.sub(r'(?<=\.)html$', 'xml', true_url)
                profile_in_xml = requests.get(true_url).content
                profile_list.append(xmltodict.parse(profile_in_xml, dict_constructor=dict))
                pbar.update(1)
            except:
                print(f'url {url} not fetched!')
                continue

    with open(osp.join(DATA_PATH, f'{target_pickle_name if target_pickle_name is not None else "profiles"}.pickle'),
              'wb') as f:
        pickle.dump(profile_list, f)

    return profile_list


def generate_graph(year=None):
    pass


if __name__ == '__main__':
    auth_name_list = read_faculty()
    auth_profiles = fetch_dblp_profile(auth_name_list=auth_name_list, reuse=True, target_pickle_name='profiles')

