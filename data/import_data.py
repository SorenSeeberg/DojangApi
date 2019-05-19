#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import os
from query.category import CATEGORY_NAMES
from query.level import LEVEL_NAMES
from typing import List, Dict

# Headers
# Koreansk Dansk Kategori Pensum Kilde Rettet Exporter


def list_to_dict(labels: List[str]) -> Dict:
    return {key.lower(): value + 1 for (value, key) in enumerate(labels)}


category_names_dict = list_to_dict(CATEGORY_NAMES)
belt_names_dict = list_to_dict(LEVEL_NAMES)
category_names = set()


def extract_row(row) -> List:
    category_names.add(row[2])
    return [row[0], row[1], category_names_dict.get(row[2].lower(), -1), belt_names_dict.get(row[3].lower(), -1)]


def extract_curriculum() -> List[List]:
    with open(os.path.join(os.path.dirname(__file__), 'curriculum.csv'), 'r', encoding='utf-8') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')

        return [extract_row(row) for row in csv_reader if row[6] == 'TRUE']


if __name__ == '__main__':

    [print(row) for row in extract_curriculum()]
    print(category_names)
