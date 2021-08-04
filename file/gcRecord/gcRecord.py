#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 解析gc日志 """
from entity.gc.GcInfoMessage import GcInfoMessage
from utils.analyzeFileUtils import analyzeFileUtils

__author__ = 'bokai'

import os
import csv


# 给一个gclog解压后的路径，解析里面的gcRecord文件
# zippath/result/gclog/gcRecord类文件
# 解析后合并的文件名
# zippath/result/treas201901.gc.log


def generate_gc_log_and_get_node_pid_gc_info_list_detail(gc_log_path, gc_log_fullname):
    if not os.path.exists(gc_log_path):
        print('这个版本的treas包没有gcRecord表. fu*k u')
        return
    if os.path.exists(gc_log_fullname):
        print(gc_log_fullname, ' - result gc log file already exist.')
        return
    result_gc_log_file = open(gc_log_fullname, 'w')
    result_gc_log_file_header = ['log', 'gcStartTime', 'node']
    result_gc_log_file_writer = csv.DictWriter(result_gc_log_file, result_gc_log_file_header)
    result_gc_log_file_writer.writeheader()
    #  {'node1':{'pid1':['gc_list']}}
    gc_info_message_list = []
    for parent, dir_name, file_names in os.walk(gc_log_path):
        for filename in file_names:
            if filename.startswith('gcRecord') and filename.endswith('.csv'):
                # 打开每个文件
                gc_csv_file = open(parent + os.sep + filename, 'r')
                gc_file_reader = csv.DictReader((line.replace('\0', '') for line in gc_csv_file))
                try:
                    for row in gc_file_reader:
                        month_gc_info_message = GcInfoMessage(row)
                        gc_info_message_list.append(month_gc_info_message)
                        gc_row = month_gc_info_message.to_print_gc_log()
                        result_gc_log_file_writer.writerow(gc_row)
                except Exception:
                    print("gcRecord row read failed.", filename, 'line:', gc_file_reader.line_num, e)

                gc_csv_file.close()

    result_gc_log_file.close()
    # 先按照节点排序，分隔开之后，在按照时间排序
    analyzeFileUtils.sort_file_message(gc_log_fullname, ['node', 'gcStartTime'])
    gc_info_message_list.sort(key=GcInfoMessage.get_timestamps)
    gc_info_message_node_pid_detail = {}
    for gc_info_message in gc_info_message_list:
        node = gc_info_message.get_node()
        pid = gc_info_message.get_pid()
        if node in gc_info_message_node_pid_detail:
            if pid in gc_info_message_node_pid_detail[node]:
                gc_info_message_node_pid_detail[node][pid].append(gc_info_message)
            else:
                gc_info_message_node_pid_detail[node][pid] = []
                gc_info_message_node_pid_detail[node][pid].append(gc_info_message)
        else:
            gc_info_message_node_pid_detail[node] = {}
            gc_info_message_node_pid_detail[node][pid] = []
            gc_info_message_node_pid_detail[node][pid].append(gc_info_message)
    return gc_info_message_node_pid_detail
