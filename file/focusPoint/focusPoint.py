#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" main """
from entity.focuspoint.box.FocuspointWrapper import FocuspointWrapper
from entity.focuspoint.message.IntellijReleaseInfoMessage import IntellijReleaseInfoMessage
from entity.focuspoint.message.InterruptInfoMessage import InterruptInfoMessage
from entity.focuspoint.message.LimitInfoMessage import LimitInfoMessage
from entity.focuspoint.message.LoadGroupMessage import LoadGroupMessage
from entity.focuspoint.message.ServerInfoMessage import ServerInfoMessage
from entity.focuspoint.message.ShutdownInfoMessage import ShutdownInfoMessage

__author__ = 'bokai'

import os
import csv
import utils.myTime.utils
from utils.analyzeFileUtils import analyzeFileUtils
import pandas as pd
import json


# 给一个focuspoint解压后的路径，解析里面的focusPoint文件
# zippath/result/focusPoint/focusPoint类文件
# 解析后合并的文件名
# zip_path/result/treas201901.focuspoint.csv


def generate_focuspoint_log_and_get_focuspoint_node_pid_list_detail(focuspoint_path, focuspoint_full_name):
    if not os.path.exists(focuspoint_path):
        print('这个版本的treas包没有FocusPoint表. fu*k u again')
        return
    if os.path.exists(focuspoint_full_name):
        print(focuspoint_full_name, ' - result gc log file already exist.')
        return

    result_focuspoint_file_header = ['id', 'time', 'date', 'node', 'username', 'source', 'text', 'title', 'body']

    # 4002 限制
    focuspoint_limit_full_name = focuspoint_full_name + '.limit.log'
    focuspoint_limit_file = open(focuspoint_limit_full_name, 'w')
    focuspoint_limit_file_writer = csv.DictWriter(focuspoint_limit_file, result_focuspoint_file_header)
    focuspoint_limit_file_writer.writeheader()
    focuspoint_limit_info_message_list = []

    # 4003 释放
    focuspoint_release_full_name = focuspoint_full_name + '.release.log'
    focuspoint_release_file = open(focuspoint_release_full_name, 'w')
    focuspoint_release_file_writer = csv.DictWriter(focuspoint_release_file, result_focuspoint_file_header)
    focuspoint_release_file_writer.writeheader()
    focuspoint_release_info_message_list = []

    # 4004 中止
    focuspoint_interrupt_full_name = focuspoint_full_name + '.interrupt.log'
    focuspoint_interrupt_file = open(focuspoint_interrupt_full_name, 'w')
    focuspoint_interrupt_file_writer = csv.DictWriter(focuspoint_interrupt_file, result_focuspoint_file_header)
    focuspoint_interrupt_file_writer.writeheader()
    focuspoint_interrupt_info_message_list = []

    # 5002 服务器启停
    focuspoint_shutdown_full_name = focuspoint_full_name + '.shutdown.log'
    focuspoint_shutdown_file = open(focuspoint_shutdown_full_name, 'w')
    focuspoint_shutdown_file_writer = csv.DictWriter(focuspoint_shutdown_file, result_focuspoint_file_header)
    focuspoint_shutdown_file_writer.writeheader()
    focuspoint_shutdown_info_message_list = []

    load_group_message = LoadGroupMessage()

    for parent, dir_name, file_names in os.walk(focuspoint_path):
        # filenames是一个list所有focuspoint文件的集合
        for filename in file_names:
            if filename.startswith('focusPoint') and filename.endswith('.csv'):
                # 打开每个文件
                focuspoint_csv_file = open(parent + os.sep + filename, 'r')
                reader = csv.reader((line.replace('\0', '') for line in focuspoint_csv_file))

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
                                        body = json.loads(row[7])
                                        node = body.get('node')
                                        row_result_dict['body'] = body
                                    row_result_dict['node'] = node
                                    # 模板限制
                                    if row_id.startswith('FR-F4002'):
                                        focuspoint_limit_info_message = LimitInfoMessage(row_result_dict)
                                        focuspoint_limit_info_message_list.append(focuspoint_limit_info_message)
                                        focuspoint_limit_file_writer.writerow(focuspoint_limit_info_message.to_print_focuspoint_log())
                                        if not row_result_dict['title'].startswith('life cycle'):
                                            load_group_message.add_limit_detail(row_result_dict)
                                    # 智能释放
                                    if row_id.startswith('FR-F4003'):
                                        focuspoint_release_info_message = IntellijReleaseInfoMessage(row_result_dict)
                                        focuspoint_release_info_message_list.append(focuspoint_release_info_message)
                                        focuspoint_release_file_writer.writerow(focuspoint_release_info_message.to_print_focuspoint_log())
                                        load_group_message.add_release_detail(row_result_dict)
                                    # 引擎中止
                                    if row_id.startswith('FR-F4004'):
                                        focuspoint_interrupt_info_message = InterruptInfoMessage(row_result_dict)
                                        focuspoint_interrupt_info_message_list.append(focuspoint_interrupt_info_message)
                                        focuspoint_interrupt_file_writer.writerow(focuspoint_interrupt_info_message.to_print_focuspoint_log())
                                        if 'trigger' in row_result_dict['body'] and row_result_dict['body']['trigger']:
                                            load_group_message.add_interrupt_detail(row_result_dict)
                                    if row_id.startswith('FR-F5002'):
                                        focuspoint_shutdown_info_message = ShutdownInfoMessage(row_result_dict)
                                        focuspoint_shutdown_info_message_list.append(focuspoint_shutdown_info_message)
                                        focuspoint_shutdown_file_writer.writerow(focuspoint_shutdown_info_message.to_print_focuspoint_log())
                                    if row_id.startswith('FR-F5003'):
                                        focuspoint_server_info_message = ServerInfoMessage(row_result_dict)
                    except Exception as e:
                        print("focusPoint row read failed.", filename, 'line:', reader.line_num, e)
                    finally:
                        j = j + 1

                focuspoint_csv_file.close()

    focuspoint_limit_file.close()
    focuspoint_release_file.close()
    focuspoint_interrupt_file.close()
    focuspoint_shutdown_file.close()
    utils.analyzeFileUtils.analyzeFileUtils.sort_file_message(focuspoint_limit_full_name, ['node', 'time'])
    utils.analyzeFileUtils.analyzeFileUtils.sort_file_message(focuspoint_release_full_name, ['node', 'time'])
    utils.analyzeFileUtils.analyzeFileUtils.sort_file_message(focuspoint_interrupt_full_name, ['node', 'time'])
    utils.analyzeFileUtils.analyzeFileUtils.sort_file_message(focuspoint_shutdown_full_name, ['node', 'time'])

    focuspoint_limit_info_message_list.sort(key=LimitInfoMessage.get_time)
    focuspoint_release_info_message_list.sort(key=IntellijReleaseInfoMessage.get_time)
    focuspoint_interrupt_info_message_list.sort(key=InterruptInfoMessage.get_time)
    focuspoint_shutdown_info_message_list.sort(key=ShutdownInfoMessage.get_time)

    focuspoint_limit_info_message_node_list_detail = {}
    for focuspoint_limit_info_message in focuspoint_limit_info_message_list:
        node = focuspoint_limit_info_message.get_node()
        if node in focuspoint_limit_info_message_node_list_detail:
            focuspoint_limit_info_message_node_list_detail[node].append(focuspoint_limit_info_message)
        else:
            focuspoint_limit_info_message_node_list_detail[node] = []

    focuspoint_release_info_message_node_list_detail = {}
    for focuspoint_release_info_message in focuspoint_release_info_message_list:
        node = focuspoint_release_info_message.get_node()
        if node in focuspoint_release_info_message_node_list_detail:
            focuspoint_release_info_message_node_list_detail[node].append(focuspoint_release_info_message)
        else:
            focuspoint_release_info_message_node_list_detail[node] = []

    focuspoint_interrupt_info_message_node_list_detail = {}
    for focuspoint_interrupt_info_message in focuspoint_interrupt_info_message_list:
        node = focuspoint_interrupt_info_message.get_node()
        if node in focuspoint_interrupt_info_message_node_list_detail:
            focuspoint_interrupt_info_message_node_list_detail[node].append(focuspoint_interrupt_info_message)
        else:
            focuspoint_interrupt_info_message_node_list_detail[node] = []

    focuspoint_shutdown_info_message_node_pid_item = {}
    for focuspoint_shutdown_info_message in focuspoint_shutdown_info_message_list:
        node = focuspoint_shutdown_info_message.get_node()
        pid = focuspoint_shutdown_info_message.get_pid()
        if node in focuspoint_shutdown_info_message_node_pid_item:
            focuspoint_shutdown_info_message_node_pid_item[node][pid] = focuspoint_shutdown_info_message
        else:
            focuspoint_shutdown_info_message_node_pid_item[node] = {}

    focuspoint_wrapper = FocuspointWrapper(focuspoint_limit_info_message_node_list_detail,
                                           focuspoint_release_info_message_node_list_detail,
                                           focuspoint_interrupt_info_message_node_list_detail,
                                           focuspoint_shutdown_info_message_node_pid_item,
                                           load_group_message)
    return focuspoint_wrapper


if __name__ == '__main__':
    pass
    # generate_focuspoint_log_and_get_focuspoint_node_pid_list_detail("/Users/bokai/Work/FR/永不宕机/treas20200910",
    #                                                                 "/Users/bokai/Work/FR/永不宕机/treas20200910/resultFocusPoint20200910aaa.csv")
