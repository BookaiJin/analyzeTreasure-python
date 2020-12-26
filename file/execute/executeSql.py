#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" main """
import csv
import os

from entity.execute.ExecuteSqlRecord import ExecuteSqlRecord

__author__ = 'bokai'

from entity.execute.wrapper.ExecuteSqlRecordWrapper import ExecuteSqlRecordWrapper
from utils.analyzeFileUtils import analyzeFileUtils


def generate_execute_sql(execute_sql_path, execute_sql_full_name):
    if not os.path.exists(execute_sql_path):
        print('这个版本的treas包没有realTime表. >.<')
        return
    # if os.path.exists(realtime_usage_fullname):
    #     print(realtime_usage_fullname, ' - result gc log file already exist.')
    #     return
    # execute_sql_log_file = open(realtime_usage_fullname, 'w')
    # execute_sql_file_header = ['date', 'time', 'node', 'cpu', 'memory', 'sessionnum', 'onlinenum', 'pid',
    #                                       'templateRequest', 'httpRequest', 'sessionRequest', 'fineIO', 'NIO',
    #                                       'bufferMemUse', 'physicalMemUse', 'physicalMemFree', '']
    #
    # result_real_time_writer = csv.DictWriter(execute_sql_log_file, execute_sql_file_header)
    # result_real_time_writer.writeheader()
    # realtime_usage_list_detail = []
    execute_sql_list_detail = []
    execute_sql_time_list_detail = {}
    execute_sql_id_list_detail = {}
    execute_sql_count_detail = {}
    for parent, dir_name, file_names in os.walk(execute_sql_path):
        # filenames是一个list所有focuspoint文件的集合
        for filename in file_names:
            if filename.startswith('executeSql') and filename.endswith('.csv'):
                # 打开每个文件
                real_time_csv_file = open(parent + os.sep + filename, 'r', encoding='UTF-8')
                reader = csv.reader(real_time_csv_file)

                j = 0
                try:
                    for i, row in enumerate(reader):
                        if i == j:
                            try:
                                if row[0] != '' and row[0] != 'time':
                                    execute_sql_message = ExecuteSqlRecord(row)
                                    execute_sql_list_detail.append(execute_sql_message)

                                    time_spend = int(execute_sql_message.get_sql_time() / 1000)
                                    if time_spend in execute_sql_time_list_detail:
                                        execute_sql_time_list_detail[time_spend].append(execute_sql_message)
                                        execute_sql_count_detail[time_spend] += 1
                                    else:
                                        execute_sql_time_list_detail[time_spend] = [execute_sql_message]
                                        execute_sql_count_detail[time_spend] = 1

                                    id = execute_sql_message.get_id()
                                    if id in execute_sql_id_list_detail:
                                        execute_sql_id_list_detail[id].append(execute_sql_message)
                                    else:
                                        execute_sql_id_list_detail[id] = [execute_sql_message]
                                    # realtime_usage_list_detail.append(execute_sql_message)
                                    # result_real_time_writer.writerow(execute_sql_message.to_print_realtime_usage_log())
                            except IOError as e:
                                print("focusPoint row read failed.", filename, 'line:', reader.line_num)
                            finally:
                                j = j + 1
                except Exception as e:
                    print("focusPoint row read failed.", filename)

                real_time_csv_file.close()

    # execute_sql_log_file.close()
    # analyzeFileUtils.sort_file_message(realtime_usage_fullname, ['time'])

    # execute_sql_list_detail.sort(key=ExecuteSqlRecord.get_timestamp)
    sorted_execute_sql_time_list_detail = {}
    for k in sorted(execute_sql_time_list_detail.keys()):
        sorted_execute_sql_time_list_detail[k] = execute_sql_time_list_detail[k]
    sorted_execute_sql_count_detail = {}
    for k in sorted(execute_sql_count_detail.keys()):
        sorted_execute_sql_count_detail[k] = execute_sql_count_detail[k]
    execute_sql_log_file = open(execute_sql_full_name, 'w')
    execute_sql_file_header = ['sql_span', 'count']
    result_real_time_writer = csv.DictWriter(execute_sql_log_file, execute_sql_file_header)
    result_real_time_writer.writeheader()
    for key,value in sorted_execute_sql_count_detail.items():
        row = {'sql_span': key, 'count': value}
        result_real_time_writer.writerow(row)
    execute_sql_log_file.close()
    analyzeFileUtils.sort_file_message(execute_sql_full_name, ['count'], False)
    # realtime_usage_node_pid_list_detail = {}
    # for execute_sql_message in realtime_usage_list_detail:
    #     node = execute_sql_message.get_node()
    #     pid = execute_sql_message.get_pid()
    #     if node in realtime_usage_node_pid_list_detail:
    #         if pid in realtime_usage_node_pid_list_detail[node]:
    #             realtime_usage_node_pid_list_detail[node][pid].append(execute_sql_message)
    #         else:
    #             realtime_usage_node_pid_list_detail[node][pid] = []
    #             realtime_usage_node_pid_list_detail[node][pid].append(execute_sql_message)
    #     else:
    #         realtime_usage_node_pid_list_detail[node] = {}
    #         realtime_usage_node_pid_list_detail[node][pid] = []
    #         realtime_usage_node_pid_list_detail[node][pid].append(execute_sql_message)
    return ExecuteSqlRecordWrapper(execute_sql_id_list_detail, sorted_execute_sql_time_list_detail)
