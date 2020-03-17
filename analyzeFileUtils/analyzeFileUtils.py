#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 文件按照key排序 '

__author__ = 'bokai'

import pandas as pd


# 写好文件后，排下序


def sortFileMessage(fileFullNameToSort, listToSort):
    data = pd.read_csv(fileFullNameToSort)
    data.sort_values(listToSort, axis=0, ascending=True, inplace=True)
    data.to_csv(fileFullNameToSort)


if __name__ == '__main__':
    sortFileMessage((input('to sorted filename: ')))
