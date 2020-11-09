#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 解析不可用时长 """
import csv

from entity.down.DownInfoBean import DownInfoBean

__author__ = 'bokai'


def analyze_unavailable_time(gc_info_message_node_pid_list_detail, realtime_usage_node_pid_list_detail,
                             focuspoint_wrapper, unavailable_time_file_full_name):
    # 集群也要考虑
    for node in gc_info_message_node_pid_list_detail.keys():
        gc_info_message_pid_list_detail = gc_info_message_node_pid_list_detail[node]
        down_times = len(gc_info_message_pid_list_detail)
        down_info_message_list = []
        pids = [key for key, value in gc_info_message_pid_list_detail.items()]
        for i in range(down_times - 1):
            down_pid = pids[i]
            restart_pid = pids[i + 1]
            down_start_gc_list = gc_info_message_pid_list_detail[down_pid]
            down_end_gc_list = gc_info_message_pid_list_detail[restart_pid]
            down_shutdown_message_item = focuspoint_wrapper.get_shutdown_message_item(node, down_pid)
            restart_shutdown_message_item = focuspoint_wrapper.get_shutdown_message_item(node, restart_pid)
            down_info_message = DownInfoBean(down_start_gc_list, down_end_gc_list, realtime_usage_node_pid_list_detail[node][down_pid],
                                             down_shutdown_message_item, restart_shutdown_message_item)

            down_info_message_list.append(down_info_message)

        unavailable_time_file_node_full_name = unavailable_time_file_full_name + '-' + node + '-节点.log'
        unavailable_time_file = open(unavailable_time_file_node_full_name, 'w')
        unavailable_time_log_header = [
            'No',
            'down-time',
            'restart-time',
            'duration-s',
            'duration-h',
            'down_pid',
            'restart_pid',
            'predict_down_type',
            'down_user_dir',
            'record_down_type'
        ]
        unavailable_time_log_file_writer = csv.DictWriter(unavailable_time_file, unavailable_time_log_header)
        unavailable_time_log_file_writer.writeheader()
        i = 1
        for down_info_message in down_info_message_list:
            duration = down_info_message.get_duration() / 1000
            unavailable_time_log_item = {
                'No': i,
                'down-time': down_info_message.get_down_start_time(),
                'restart-time': down_info_message.get_down_end_time(),
                'duration-s': '%.0f' % duration,
                'duration-h': ('%.5f' % (duration / 3600)),
                'down_pid': down_info_message.get_down_pid(),
                'restart_pid': down_info_message.get_restart_pid(),
                'predict_down_type': down_info_message.get_down_type(),
                'down_user_dir': down_info_message.get_user_dir(),
                'record_down_type': down_info_message.get_signal_name()
            }
            i = i + 1
            unavailable_time_log_file_writer.writerow(unavailable_time_log_item)

        unavailable_time_file.close()
