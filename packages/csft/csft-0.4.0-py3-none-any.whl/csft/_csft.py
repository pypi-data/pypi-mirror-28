# -*- coding:utf-8 -*-

"""
The implementations of csft.
"""

import sys
from collections import OrderedDict, namedtuple
from os.path import getsize, islink, join, split, splitext
from pathlib import Path

from pandas import DataFrame, Series

if sys.version < '3.5':
    from scandir import walk
else:
    from os import walk

_Column = namedtuple('Column', ['PATH', 'SIZE', 'TYPE'])
column = _Column(PATH='path', SIZE='size', TYPE='type')


def make_file_list(path):
    if isinstance(path, Path):
        path = str(path)

    paths = []
    for parent, _, files in walk(path):
        for name in files:
            file_path = join(parent, name)
            if not islink(file_path):
                paths.append(file_path)
    return paths


def type_of_file(path):
    _, name = split(path)
    _, file_type = splitext(name)
    return file_type


def make_raw_data(paths):
    data = DataFrame({
        column.PATH: Series(paths),
        column.SIZE: Series([getsize(path) for path in paths]),
    })
    data[column.TYPE] = data[column.PATH].map(type_of_file)
    return data


def _type_size_sum(data, types):
    sizes = []
    for file_type in types:
        type_data = data[data[column.TYPE] == file_type]
        sizes.append(type_data[column.SIZE].sum())
    return Series(sizes)


def sum_data_by_type(data):
    types = set(file_type for file_type in data[column.TYPE])
    types = Series(tuple(types))
    sizes = _type_size_sum(data, types)

    type_size = OrderedDict()
    type_size[column.TYPE] = types
    type_size[column.SIZE] = sizes
    return DataFrame(type_size)


def sort_data_frame(data, by):
    sorted_data = data.sort_values(by, ascending=False)
    return sorted_data.reset_index(drop=True)


def csft2data(path):
    paths = make_file_list(path)
    raw_data = make_raw_data(paths)
    type_data = sum_data_by_type(raw_data)
    sorted_data = sort_data_frame(type_data, column.SIZE)
    return sorted_data
