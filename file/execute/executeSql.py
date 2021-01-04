#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" main """
import csv
import os

from entity.execute.ExecuteSqlRecord import ExecuteSqlRecord

__author__ = 'bokai'

from entity.execute.wrapper.ExecuteSqlRecordWrapper import ExecuteSqlRecordWrapper
from utils.analyzeFileUtils import analyzeFileUtils


def generate_execute_sql(company_info, execute_sql_path, execute_sql_full_name, execute_sql_full_cal_name):
    # execute_sql_list_detail = []
    # execute_sql_time_list_detail = {}
    # execute_sql_id_list_detail = {}
    execute_sql_count_detail = {}
    execute_sql_total_count = 0
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
                                    # execute_sql_list_detail.append(execute_sql_message)
                                    execute_sql_total_count += 1
                                    time_spend = int(execute_sql_message.get_sql_time() / 1000)
                                    # if time_spend in execute_sql_time_list_detail:
                                    if time_spend in execute_sql_count_detail:
                                        # execute_sql_time_list_detail[time_spend].append(execute_sql_message)
                                        execute_sql_count_detail[time_spend] += 1
                                    else:
                                        # execute_sql_time_list_detail[time_spend] = [execute_sql_message]
                                        execute_sql_count_detail[time_spend] = 1

                                    # id = execute_sql_message.get_id()
                                    # if id in execute_sql_id_list_detail:
                                    #     execute_sql_id_list_detail[id].append(execute_sql_message)
                                    # else:
                                    #     execute_sql_id_list_detail[id] = [execute_sql_message]
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
    # sorted_execute_sql_time_list_detail = {}
    # for k in sorted(execute_sql_time_list_detail.keys()):
    #     sorted_execute_sql_time_list_detail[k] = execute_sql_time_list_detail[k]
    sorted_execute_sql_count_detail = {}
    for k in sorted(execute_sql_count_detail.keys(), reverse=True):
        sorted_execute_sql_count_detail[k] = execute_sql_count_detail[k]
    execute_sql_log_file = open(execute_sql_full_name, 'w')
    execute_sql_total_cal_file = open(execute_sql_full_cal_name, 'w')
    execute_sql_file_header = ['sql_span', 'count', "大于等于当前sql耗时总次数", "小于当前耗时占比%", "total_SQL_count", "白天8小时每秒SQL数量", '99.99%的SQL时长', '大于180s的次数', '大于99.99的次数']
    result_real_time_writer = csv.DictWriter(execute_sql_log_file, execute_sql_file_header)
    result_real_time_writer.writeheader()
    now_count = 0
    now_count_up_99_key = 0
    value_over_180_count = 0
    value_over_99_count = 0
    execute_sql_total_cal_row = ''
    for key, value in sorted_execute_sql_count_detail.items():
        now_count += value
        now_count_percent = 100 - (now_count / execute_sql_total_count * 100)
        if now_count_percent <= 99.99 and now_count_up_99_key == 0:
            value_over_99_count += value
            now_count_up_99_key = key
            execute_sql_total_cal_row = company_info.app_id + ',' + company_info.year_month + ',' + str(now_count_up_99_key) + ',' + \
                                        str(execute_sql_total_count) + ',' + \
                                        str(execute_sql_total_count / 20 / 8 / 60 / 60)
        if value >= key:
            value_over_180_count += value

        row = {'sql_span': key, 'count': value, '大于等于当前sql耗时总次数': now_count, '小于当前耗时占比%': now_count_percent,
               "total_SQL_count": execute_sql_total_count,
               "白天8小时每秒SQL数量": execute_sql_total_count / 20 / 8 / 60 / 60,
               '99.99%的SQL时长': now_count_up_99_key,
               '大于180s的次数': value_over_180_count,
               '大于99.99的次数': value_over_99_count
        }
        result_real_time_writer.writerow(row)
    execute_sql_total_cal_file.write(execute_sql_total_cal_row)

    execute_sql_log_file.close()
    execute_sql_total_cal_file.close()
    analyzeFileUtils.sort_file_message(execute_sql_full_name, ['sql_span'])
    # return ExecuteSqlRecordWrapper(execute_sql_id_list_detail, sorted_execute_sql_time_list_detail)
