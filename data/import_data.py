#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import os
from query.category import CATEGORY_NAMES
from query.level import LEVEL_NAMES
from typing import List, Dict

# CSV Header
# 0 Kategori  1 Side  2 Pensum  3 Koreansk  4 Dansk  5 AppearsInTest

# Import Header
# 0 Koreansk  1 Dansk


def list_to_dict(labels: List[str]) -> Dict:
    return {key.lower(): value + 1 for (value, key) in enumerate(labels)}


category_names_dict = list_to_dict(CATEGORY_NAMES)
belt_names_dict = list_to_dict(LEVEL_NAMES)
category_names = set()


def extract_row(row) -> List:
    category_names.add(row[0])
    return [row[3], row[4], category_names_dict.get(row[0].lower(), -1), int(row[2])+1]


def extract_curriculum() -> List[List]:
    with open(os.path.join(os.path.dirname(__file__), 'curriculum_dtaf.csv'), 'r', encoding='utf-8') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')

        return [extract_row(row) for row in csv_reader if row[5] == 'TRUE']


if __name__ == '__main__':

    [print(row) for row in extract_curriculum()]
    print(sorted(category_names))
