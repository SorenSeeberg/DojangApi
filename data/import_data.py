#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import os
from query.category import category_names
from query.belt import belt_names
from typing import List, Dict

# Headers
# Koreansk Dansk Kategori Pensum Kilde Rettet Exporter


def list_to_dict(labels: List[str]) -> Dict:
    return {key.lower(): value + 1 for (value, key) in enumerate(labels)}


category_names_dict = list_to_dict(category_names)
belt_names_dict = list_to_dict(belt_names)


def extract_row(row) -> List:
    return [row[0], row[1], category_names_dict.get(row[2].lower(), -1), belt_names_dict.get(row[3].lower(), -1)]


def extract_info() -> List[List]:
    with open(os.path.join(os.path.dirname(__file__), 'info.csv'), 'r', encoding='utf-8') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')

        return [extract_row(row) for row in csv_reader if row[6] == 'TRUE']


if __name__ == '__main__':

    [print(row) for row in extract_info()]

