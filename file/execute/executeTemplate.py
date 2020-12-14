#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" main """
import csv
import os

from entity.execute.ExecuteTemplateRecord import ExecuteTemplateRecord

__author__ = 'bokai'

from utils.analyzeFileUtils import analyzeFileUtils


def generate_execute_template(execute_path, execute_sql_record_wrapper, execute_template_file_full_name):
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
    # execute_template_writer = csv.DictWriter(result_real_time_usage_log_file, result_real_time_usage_file_header)
    # execute_template_writer.writeheader()
    # realtime_usage_list_detail = []
    execute_template_list_detail = []
    execute_template_sql_span_list_detail = {}
    execute_template_consume_list_detail = {}
    execute_template_consume_count_detail = {}
    for parent, dir_name, file_names in os.walk(execute_path):
        # filenames是一个list所有focuspoint文件的集合
        for filename in file_names:
            if filename.startswith('execute') and filename.endswith('.csv'):
                # 打开每个文件
                execute_template_csv_file = open(parent + os.sep + filename, 'r', encoding='UTF-8')
                reader = csv.reader(execute_template_csv_file)

                j = 0
                for i, row in enumerate(reader):
                    if i == j:
                        try:
                            if row[0] != '' and row[0] != 'id':
                                execute_template_message = ExecuteTemplateRecord(row)
                                execute_template_list_detail.append(execute_template_message)
                                # 模板计算时间分组
                                consume = int(execute_template_message.get_consume() / 1000)
                                if consume in execute_template_list_detail:
                                    execute_template_consume_list_detail[consume].append(execute_template_message)
                                    execute_template_consume_count_detail[consume] += 1
                                else:
                                    execute_template_consume_list_detail[consume] = [execute_template_message]
                                    execute_template_consume_count_detail[consume] = 1

                                # 模板sql计算时间分组
                                sql_span = int(execute_template_message.get_sql_time() / 1000)
                                if sql_span in execute_template_sql_span_list_detail:
                                    execute_template_sql_span_list_detail[sql_span].append(execute_template_message)
                                else:
                                    execute_template_sql_span_list_detail[sql_span] = [execute_template_message]

                                # execute_template_writer.writerow(execute_template_message.to_print_realtime_usage_log())
                        except IOError as e:
                            print("focusPoint row read failed.", filename, 'line:', reader.line_num)
                        finally:
                            j = j + 1

                execute_template_csv_file.close()

    # result_real_time_usage_log_file.close()
    # analyzeFileUtils.sort_file_message(realtime_usage_fullname, ['time'])
    # execute_template_list_detail.sort(key=ExecuteTemplateRecord.get_start_time)
    sorted_execute_template_consume_list_detail = {}
    for k in sorted(execute_template_consume_list_detail.keys()):
        sorted_execute_template_consume_list_detail[k] = execute_template_consume_list_detail[k]
    sorted_execute_template_sql_span_list_detail = {}
    for k in sorted(execute_template_sql_span_list_detail.keys()):
        sorted_execute_template_sql_span_list_detail[k] = execute_template_sql_span_list_detail[k]
    # execute_template_consume_count_detail = {}
    execute_template_log_file = open(execute_template_file_full_name, 'w')
    execute_template_file_header = ['sql_span', 'count']
    execute_template_writer = csv.DictWriter(execute_template_log_file, execute_template_file_header)
    execute_template_writer.writeheader()
    for key,value in execute_template_consume_count_detail.items():
        row = {'sql_span': key, 'count': value}
        execute_template_writer.writerow(row)
    execute_template_log_file.close()
    analyzeFileUtils.sort_file_message(execute_template_file_full_name, ['count'], False)
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
    return execute_template_consume_list_detail
