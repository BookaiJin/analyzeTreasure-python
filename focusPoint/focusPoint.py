#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' main '

__author__ = 'bokai'

import os
import csv
import time
import pandas as pd
import analyzeFileUtils.analyzeFileUtils


# 给一个focuspoint解压后的路径，解析里面的focusPoint文件
# zippath/result/focusPoint/focusPoint类文件
# 解析后合并的文件名
# zippath/result/treas201901.focuspoint.csv


def generateFocusPointFile(focusPointPath, focusPointFullName):
    if not os.path.exists(focusPointPath):
        print('这个版本的treas包没有FocusPoint表. fu*k u again')
        return
    if os.path.exists(focusPointFullName):
        print(focusPointFullName, ' - result gc log file already exist.')
        return
    # 固化专用
    result_5002_file = open(focusPointFullName + 'solid.log', 'w')
    resultFocusPointLogFile = open(focusPointFullName, 'w')
    resultFocusPointFileHeader = ['', 'id', 'time', 'username', 'source', 'text', 'title', 'body']
    resultFocusPointWriter = csv.DictWriter(resultFocusPointLogFile, resultFocusPointFileHeader)
    resultFocusPointWriter.writeheader()
    result_5002_file_writer = csv.DictWriter(result_5002_file, resultFocusPointFileHeader)
    result_5002_file_writer.writeheader()
    for parent, dirname, filenames in os.walk(focusPointPath):
        # filenames是一个list所有focuspoint文件的集合
        for filename in filenames:
            if filename.startswith('focusPoint') and filename.endswith('.csv'):
                # 打开每个文件
                focuspointCsvFile = open(parent + os.sep + filename, 'r')
                reader = csv.DictReader(focuspointCsvFile)

                try:
                    # 按行读取dict格式的数据
                    for row in reader:
                        if row.get('id').startswith('FR-F4002') or row.get('id').startswith('FR-F4003') or row.get(
                                'id').startswith('FR-F4004'):
                            if '' in row:
                                # 时间戳ms转为s
                                localTime = time.localtime(int(row.get('time')) / 1000)
                                localTimeToSave = time.strftime('%Y-%m-%d %H:%M:%S', localTime)
                                row[''] = localTimeToSave
                                resultFocusPointWriter.writerow(row)
                        if row.get('id').startswith('FR-F5002'):
                            result_5002_file_writer.writerow(row)
                    focuspointCsvFile.close()
                except Exception:
                    print("focusPoint row read failed.", filename, 'line:', reader.line_num)

    resultFocusPointLogFile.close()
    analyzeFileUtils.analyzeFileUtils.sortFileMessage(focusPointFullName, ['time'])
