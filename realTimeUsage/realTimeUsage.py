#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' main '
import csv

__author__ = 'bokai'

import os
import myTime.utils
import analyzeFileUtils.analyzeFileUtils


def generate_realtime_usage(realtime_usage_path, realtime_usage_fullname):
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
    for parent, dirname, filenames in os.walk(realtime_usage_path):
        # filenames是一个list所有focuspoint文件的集合
        for filename in filenames:
            if filename.startswith('realTime') and filename.endswith('.csv'):
                # 打开每个文件
                real_time_csv_file = open(parent + os.sep + filename, 'r')
                reader = csv.reader(real_time_csv_file)

                j = 0
                for i, row in enumerate(reader):
                    if i == j:
                        try:
                            if row[0] != '' and row[0] != 'time':
                                row_result_dict = {'date': '', 'time': '', 'node': '', 'cpu': '', 'memory': '',
                                                   'sessionnum': '', 'onlinenum': '', 'pid': '', 'templateRequest': '',
                                                   'httpRequest': '', 'sessionRequest': '', 'fineIO': '', 'NIO': '',
                                                   'bufferMemUse': '', 'physicalMemUse': '', 'physicalMemFree': ''}
                                local_time_to_save = myTime.utils.convert_time_to_date(row[0])
                                row_result_dict['date'] = local_time_to_save
                                fill_result_dict_from_row(row_result_dict, row)
                                result_real_time_writer.writerow(row_result_dict)
                        except Exception as e:
                            print("focusPoint row read failed.", filename, 'line:', reader.line_num)
                        finally:
                            j = j + 1

                real_time_csv_file.close()

    result_real_time_usage_log_file.close()
    analyzeFileUtils.analyzeFileUtils.sortFileMessage(realtime_usage_fullname, ['time'])


def fill_result_dict_from_row(row_result_dict, row):
    row_result_dict['time'] = row[0]
    row_result_dict['node'] = row[1]
    row_result_dict['cpu'] = row[2]
    row_result_dict['memory'] = row[3]
    row_result_dict['sessionnum'] = row[4]
    row_result_dict['onlinenum'] = row[5]
    row_result_dict['pid'] = row[6]
    row_result_dict['templateRequest'] = row[7]
    row_result_dict['httpRequest'] = row[8]
    row_result_dict['sessionRequest'] = row[9]
    if len(row) > 11:
        row_result_dict['fineIO'] = row[10]
        row_result_dict['NIO'] = row[11]
        row_result_dict['bufferMemUse'] = row[12]
        row_result_dict['physicalMemUse'] = row[13]
        row_result_dict['physicalMemFree'] = row[14]


if __name__ == '__main__':
    realTimeUsagePath = input('realTimeUsagePath文件夹: ')
    realTimeUsageFullName = input('realTimeUsageFullName文件名: ')
    generate_realtime_usage(realTimeUsagePath, realTimeUsageFullName)
