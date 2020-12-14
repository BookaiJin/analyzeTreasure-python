#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 文件按照key排序 """

__author__ = 'bokai'

import pandas as pd


# 写好文件后，排下序


def sort_file_message(file_fullname2sort, list2sort, ascending=True):
    data = pd.read_csv(file_fullname2sort)
    data.sort_values(list2sort, axis=0, ascending=ascending, inplace=True)
    data.to_csv(file_fullname2sort)


if __name__ == '__main__':
    sort_file_message((input('to sorted filename: ')), 'time')