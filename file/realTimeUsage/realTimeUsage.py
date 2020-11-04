#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" main """
import csv

from entity.realtimeusage.RealtimeUsage import RealtimeUsage
from utils.analyzeFileUtils import analyzeFileUtils

__author__ = 'bokai'

import os
from utils.myTime import utils


def generate_realtime_usage_and_get_node_pid_realtime_info_list_detail(realtime_usage_path, realtime_usage_fullname):
    if not os.path.exists(realtime_usage_path):
        print('这个版本的treas包没有realTime表. fu*k u again')
        return
    if os.path.exists(realtime_usage_fullname):
        print(realtime_usage_fullname, ' - result gc log file already exist.')
        return
    result_real_time_usage_log_file = open(realtime_usage_fullname, 'w')
    result_real_time_usage_file_header = ['date', 'time', 'node', 'cpu', 'memory', 'sessionnum', 'onlinenum', 'pid',
                                          'templateRequest', 'httpRequest', 'sessionRequest', 'fineIO', 'NIO',
                                          'bufferMemUse', 'physicalMemUse', 'physicalMemFree', '']

    result_real_time_writer = csv.DictWriter(result_real_time_usage_log_file, result_real_time_usage_file_header)
    result_real_time_writer.writeheader()
    realtime_usage_list_detail = []
    for parent, dir_name, file_names in os.walk(realtime_usage_path):
        # filenames是一个list所有focuspoint文件的集合
        for filename in file_names:
            if filename.startswith('realTime') and filename.endswith('.csv'):
                # 打开每个文件
                real_time_csv_file = open(parent + os.sep + filename, 'r')
                reader = csv.reader(real_time_csv_file)

                j = 0
                for i, row in enumerate(reader):
                    if i == j:
                        try:
                            if row[0] != '' and row[0] != 'time':
                                realtime_usage_message = RealtimeUsage(row)
                                realtime_usage_list_detail.append(realtime_usage_message)
                                result_real_time_writer.writerow(realtime_usage_message.to_print_realtime_usage_log())
                        except Exception as e:
                            print("focusPoint row read failed.", filename, 'line:', reader.line_num)
                        finally:
                            j = j + 1

                real_time_csv_file.close()

    result_real_time_usage_log_file.close()
    analyzeFileUtils.sort_file_message(realtime_usage_fullname, ['time'])
    realtime_usage_list_detail.sort(key=RealtimeUsage.get_timestamps)
    realtime_usage_node_pid_list_detail = {}
    for realtime_usage_message in realtime_usage_list_detail:
        node = realtime_usage_message.get_node()
        pid = realtime_usage_message.get_pid()
        if node in realtime_usage_node_pid_list_detail:
            if pid in realtime_usage_node_pid_list_detail[node]:
                realtime_usage_node_pid_list_detail[node][pid].append(realtime_usage_message)
            else:
                realtime_usage_node_pid_list_detail[node][pid] = []
                realtime_usage_node_pid_list_detail[node][pid].append(realtime_usage_message)
        else:
            realtime_usage_node_pid_list_detail[node] = {}
            realtime_usage_node_pid_list_detail[node][pid] = []
            realtime_usage_node_pid_list_detail[node][pid].append(realtime_usage_message)
    return realtime_usage_node_pid_list_detail


if __name__ == '__main__':
    realTimeUsagePath = input('realTimeUsagePath文件夹: ')
    realTimeUsageFullName = input('realTimeUsageFullName文件名: ')
    generate_realtime_usage_and_get_node_pid_realtime_info_list_detail(realTimeUsagePath, realTimeUsageFullName)
