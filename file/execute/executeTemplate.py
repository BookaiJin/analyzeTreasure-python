#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" main """
import csv
import os

from entity.execute.ExecuteTemplateRecord import ExecuteTemplateRecord

__author__ = 'bokai'


def generate_execute_template(execute_path):
    if not os.path.exists(execute_path):
        print('这个版本的treas包没有realTime表. fu*k u again')
        return
    # if os.path.exists(realtime_usage_fullname):
    #     print(realtime_usage_fullname, ' - result gc log file already exist.')
    #     return
    # result_real_time_usage_log_file = open(realtime_usage_fullname, 'w')
    # result_real_time_usage_file_header = ['date', 'time', 'node', 'cpu', 'memory', 'sessionnum', 'onlinenum', 'pid',
    #                                       'templateRequest', 'httpRequest', 'sessionRequest', 'fineIO', 'NIO',
    #                                       'bufferMemUse', 'physicalMemUse', 'physicalMemFree', '']
    #
    # result_real_time_writer = csv.DictWriter(result_real_time_usage_log_file, result_real_time_usage_file_header)
    # result_real_time_writer.writeheader()
    # realtime_usage_list_detail = []
    execute_template_list_detail = []
    for parent, dir_name, file_names in os.walk(execute_path):
        # filenames是一个list所有focuspoint文件的集合
        for filename in file_names:
            if filename.startswith('execute') and filename.endswith('.csv'):
                # 打开每个文件
                execute_template_csv_file = open(parent + os.sep + filename, 'r')
                reader = csv.reader(execute_template_csv_file)

                j = 0
                for i, row in enumerate(reader):
                    if i == j:
                        try:
                            if row[0] != '' and row[0] != 'id':
                                execute_template_message = ExecuteTemplateRecord(row)
                                execute_template_list_detail.append(execute_template_message)
                                # result_real_time_writer.writerow(execute_template_message.to_print_realtime_usage_log())
                        except IOError as e:
                            print("focusPoint row read failed.", filename, 'line:', reader.line_num)
                        finally:
                            j = j + 1

                execute_template_csv_file.close()

    # result_real_time_usage_log_file.close()
    # analyzeFileUtils.sort_file_message(realtime_usage_fullname, ['time'])
    execute_template_list_detail.sort(key=ExecuteTemplateRecord.get_start_time)
    # realtime_usage_node_pid_list_detail = {}
    # for execute_template_message in realtime_usage_list_detail:
    #     node = execute_template_message.get_node()
    #     pid = execute_template_message.get_pid()
    #     if node in realtime_usage_node_pid_list_detail:
    #         if pid in realtime_usage_node_pid_list_detail[node]:
    #             realtime_usage_node_pid_list_detail[node][pid].append(execute_template_message)
    #         else:
    #             realtime_usage_node_pid_list_detail[node][pid] = []
    #             realtime_usage_node_pid_list_detail[node][pid].append(execute_template_message)
    #     else:
    #         realtime_usage_node_pid_list_detail[node] = {}
    #         realtime_usage_node_pid_list_detail[node][pid] = []
    #         realtime_usage_node_pid_list_detail[node][pid].append(execute_template_message)
    return execute_template_list_detail
