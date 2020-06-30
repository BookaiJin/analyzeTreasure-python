#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' main '

__author__ = 'bokai'

import os
import csv
import time
import analyzeFileUtils.analyzeFileUtils
import pandas as pd


# 给一个focuspoint解压后的路径，解析里面的focusPoint文件
# zippath/result/focusPoint/focusPoint类文件
# 解析后合并的文件名
# zippath/result/treas201901.focuspoint.csv


def generateFocusPointFile(focus_point_path, focus_point_full_name):
    if not os.path.exists(focus_point_path):
        print('这个版本的treas包没有FocusPoint表. fu*k u again')
        return
    if os.path.exists(focus_point_full_name):
        print(focus_point_full_name, ' - result gc log file already exist.')
        return
    # 固化专用
    focus_point_shutdown_full_name = focus_point_full_name + '.shutdown.log'
    result_5002_file = open(focus_point_shutdown_full_name, 'w')
    result_focus_point_log_file = open(focus_point_full_name, 'w')
    result_focus_point_file_header = ['', 'id', 'time', 'node', 'username', 'source', 'text', 'title', 'body']
    result_focus_point_writer = csv.DictWriter(result_focus_point_log_file, result_focus_point_file_header)
    result_focus_point_writer.writeheader()
    result_5002_file_writer = csv.DictWriter(result_5002_file, result_focus_point_file_header)
    result_5002_file_writer.writeheader()
    for parent, dirname, filenames in os.walk(focus_point_path):
        # filenames是一个list所有focuspoint文件的集合
        for filename in filenames:
            if filename.startswith('focusPoint') and filename.endswith('.csv'):
                # 打开每个文件
                focuspointCsvFile = open(parent + os.sep + filename, 'r')
                reader = csv.DictReader(focuspointCsvFile)

                try:
                    # 按行读取dict格式的数据
                    for row in reader:
                        row_id = row.get('id')
                        if row_id.startswith('FR-F4002') or row_id.startswith('FR-F4003') or \
                                row.get('id').startswith('FR-F4004') or row_id.startswith('FR-F5002'):
                            if '' in row:
                                # 时间戳ms转为s
                                local_time = time.localtime(int(row.get('time')) / 1000)
                                local_time_to_save = time.strftime('%Y-%m-%dT%H:%M:%S', local_time)
                                row[''] = local_time_to_save
                                node = ''
                                if row.get('body') != '':
                                    body = pd.json.loads(row.get('body'))
                                    node = body.get('node')
                                row['node'] = node
                                if row_id.startswith('FR-F4002') or row_id.startswith('FR-F4003') or \
                                        row.get('id').startswith('FR-F4004'):
                                    result_focus_point_writer.writerow(row)
                                if row_id.startswith('FR-F5002'):
                                    result_5002_file_writer.writerow(row)
                    focuspointCsvFile.close()
                except Exception:
                    print("focusPoint row read failed.", filename, 'line:', reader.line_num)

    result_focus_point_log_file.close()
    result_5002_file.close()
    analyzeFileUtils.analyzeFileUtils.sortFileMessage(focus_point_full_name, ['node', 'time'])
    analyzeFileUtils.analyzeFileUtils.sortFileMessage(focus_point_shutdown_full_name, ['node', 'time'])
