#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" main """
from entity.focuspoint.IntellijReleaseInfoMessage import IntellijReleaseInfoMessage
from entity.focuspoint.InterruptInfoMessage import InterruptInfoMessage
from entity.focuspoint.LimitInfoMessage import LimitInfoMessage
from entity.focuspoint.ShutdownInfoMessage import ShutdownInfoMessage

__author__ = 'bokai'

import os
import csv
import utils.myTime.utils
from utils.analyzeFileUtils import analyzeFileUtils
import pandas as pd


# 给一个focuspoint解压后的路径，解析里面的focusPoint文件
# zippath/result/focusPoint/focusPoint类文件
# 解析后合并的文件名
# zip_path/result/treas201901.focuspoint.csv


def generate_focus_point_log_and_get_focus_point_node_pid_list_detail(focus_point_path, focus_point_full_name):
    if not os.path.exists(focus_point_path):
        print('这个版本的treas包没有FocusPoint表. fu*k u again')
        return
    if os.path.exists(focus_point_full_name):
        print(focus_point_full_name, ' - result gc log file already exist.')
        return

    result_focus_point_file_header = ['id', 'time', 'date', 'node', 'username', 'source', 'text', 'title', 'body']

    # 4002 限制
    focus_point_limit_full_name = focus_point_full_name + '.limit.log'
    focus_point_limit_file = open(focus_point_limit_full_name, 'w')
    focus_point_limit_file_writer = csv.DictWriter(focus_point_limit_file, result_focus_point_file_header)
    focus_point_limit_file_writer.writeheader()

    # 4003 释放
    focus_point_release_full_name = focus_point_full_name + '.release.log'
    focus_point_release_file = open(focus_point_release_full_name, 'w')
    focus_point_release_file_writer = csv.DictWriter(focus_point_release_file, result_focus_point_file_header)
    focus_point_release_file_writer.writeheader()

    # 4004 中止
    focus_point_interrupt_full_name = focus_point_full_name + '.interrupt.log'
    focus_point_interrupt_file = open(focus_point_interrupt_full_name, 'w')
    focus_point_interrupt_file_writer = csv.DictWriter(focus_point_interrupt_file, result_focus_point_file_header)
    focus_point_interrupt_file_writer.writeheader()

    # 5002 服务器启停
    focus_point_shutdown_full_name = focus_point_full_name + '.shutdown.log'
    focus_point_shutdown_file = open(focus_point_shutdown_full_name, 'w')
    focus_point_shutdown_file_writer = csv.DictWriter(focus_point_shutdown_file, result_focus_point_file_header)
    focus_point_shutdown_file_writer.writeheader()

    for parent, dir_name, file_names in os.walk(focus_point_path):
        # filenames是一个list所有focuspoint文件的集合
        for filename in file_names:
            if filename.startswith('focusPoint') and filename.endswith('.csv'):
                # 打开每个文件
                focuspoint_csv_file = open(parent + os.sep + filename, 'r')
                reader = csv.reader(focuspoint_csv_file)

                j = 0
                for i, rows in enumerate(reader):
                    try:
                        if j == i:
                            row = rows
                            row_id = row[0]
                            if row_id.startswith('FR-F4002') or row_id.startswith('FR-F4003') or \
                                    row_id.startswith('FR-F4004') or row_id.startswith('FR-F5002'):
                                row_result_dict = {'id': row_id, 'time': '', 'date': '', 'node': '', 'username': '',
                                                   'source': '', 'text': '', 'title': '', 'body': ''}
                                if row[1] != '':
                                    local_time_to_save = utils.myTime.utils.convert_time_to_date(row[1])
                                    row_result_dict['time'] = row[1]
                                    row_result_dict['date'] = local_time_to_save
                                    row_result_dict['username'] = row[2]
                                    row_result_dict['source'] = row[4]
                                    row_result_dict['text'] = row[5]
                                    row_result_dict['title'] = row[6]
                                    row_result_dict['body'] = row[7]
                                    node = ''
                                    if row[7] != '':
                                        body = pd.json.loads(row[7])
                                        node = body.get('node')
                                        row_result_dict['body'] = body
                                    row_result_dict['node'] = node
                                    if row_id.startswith('FR-F4002'):
                                        focus_point_limit_info_message = LimitInfoMessage(row_result_dict)
                                        focus_point_limit_file_writer.writerow(focus_point_limit_info_message.to_print_focuspoint_log())
                                    if row_id.startswith('FR-F4003'):
                                        focus_point_release_info_message = IntellijReleaseInfoMessage(row_result_dict)
                                        focus_point_release_file_writer.writerow(focus_point_release_info_message.to_print_focuspoint_log())
                                    if row_id.startswith('FR-F4004'):
                                        focus_point_interrupt_info_message = InterruptInfoMessage(row_result_dict)
                                        focus_point_interrupt_file_writer.writerow(focus_point_interrupt_info_message.to_print_focuspoint_log())
                                    if row_id.startswith('FR-F5002'):
                                        focus_point_shutdown_info_message = ShutdownInfoMessage(row_result_dict)
                                        focus_point_shutdown_file_writer.writerow(focus_point_shutdown_info_message.to_print_focuspoint_log())
                    except Exception:
                        print("focusPoint row read failed.", filename, 'line:', reader.line_num)
                    finally:
                        j = j + 1

                focuspoint_csv_file.close()

    focus_point_limit_file.close()
    focus_point_release_file.close()
    focus_point_interrupt_file.close()
    focus_point_shutdown_file.close()
    utils.analyzeFileUtils.analyzeFileUtils.sort_file_message(focus_point_limit_full_name, ['node', 'time'])
    utils.analyzeFileUtils.analyzeFileUtils.sort_file_message(focus_point_release_full_name, ['node', 'time'])
    utils.analyzeFileUtils.analyzeFileUtils.sort_file_message(focus_point_interrupt_full_name, ['node', 'time'])
    utils.analyzeFileUtils.analyzeFileUtils.sort_file_message(focus_point_shutdown_full_name, ['node', 'time'])


if __name__ == '__main__':
    generate_focus_point_log_and_get_focus_point_node_pid_list_detail("/Users/bokai/Work/FR/永不宕机/treas20200910",
                                                                      "/Users/bokai/Work/FR/永不宕机/treas20200910/resultFocusPoint20200910aaa.csv")
