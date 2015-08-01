# -*- coding: utf-8 -*-
from __future__ import absolute_import

import csv
import os

from items.models import Item

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    file_loc = os.path.join(BASE_DIR, 'data', 'invTypes.csv')
    with open(file_loc, 'r') as f:
        reader = csv.reader(f)
        for num, row in enumerate(reader):
            if num:
                try:
                    Item.objects.create(
                        type_id=row[0],
                        type_name=unicode(row[2]).encode('utf-8').strip()
                    )
                except UnicodeDecodeError as e:
                    print('{} --- LINE NO.: {}'.format(e, num))
                    raise
