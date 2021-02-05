import os.path as osp

import pandas as pd

from data import DATA_PATH


def read_faculty(path=DATA_PATH, filename='Faculty.xlsx', sheet_name='by course'):
    """
    read the faculty member namelist
    :param sheet_name: name of the sheet
    :param filename: filename of the target name list
    :param path: directory of the name list
    :return: pandas dataframe
    """
    target_file = osp.join(path, filename)

    if not osp.exists(target_file):
        raise FileNotFoundError("the appointed faculty name list {} does not exist!".format(target_file))

    name_list = pd.read_excel(target_file, sheet_name=sheet_name)
    assert set(name_list.columns.values).issuperset({'Faculty', 'Position', 'Gender', 'Management', 'DBLP', 'Area'}),\
        'required fields are missing from the sheet!'
    return name_list


def read_top_conferences():
    pass
