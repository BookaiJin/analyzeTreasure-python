#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 解析不可用时长 """
from entity.down.DownInfoBean import DownInfoBean

__author__ = 'bokai'


def analyze_unavailable_time(gc_info_message_node_pid_list_detail, realtime_usage_node_pid_list_detail, unavailable_time_file_full_name):
    if len(gc_info_message_node_pid_list_detail) == 1:
        gc_info_message_pid_list_detail = gc_info_message_node_pid_list_detail['']
        down_times = len(gc_info_message_pid_list_detail)
        down_info_message_list = []
        pids = [key for key, value in gc_info_message_pid_list_detail.items()]
        for i in range(down_times - 1):
            down_start_gc_list = gc_info_message_pid_list_detail[pids[i]]
            down_end_gc_list = gc_info_message_pid_list_detail[pids[i + 1]]
            down_info_message = DownInfoBean(down_start_gc_list, down_end_gc_list)

            down_info_message_list.append(down_info_message)

        unavailable_time_file = open(unavailable_time_file_full_name, "w")
        unavailable_time_file.write("重启总次数: " + str(len(down_info_message_list)) + "\n")
        log_header = ['No', 'duration-秒', 'duration-时', 'down_type']
        log_format = "<15"
        for string in log_header:
            unavailable_time_file.write(format(string, log_format))
        unavailable_time_file.write("\n")
        i = 1
        for down_info_message in down_info_message_list:
            duration = down_info_message.get_duration() / 1000
            log_item = [i, '%.0f' % duration, ('%.5f' % (duration / 3600)), down_info_message.get_down_type()]
            i = i + 1
            for string in log_item:
                unavailable_time_file.write(format(string, log_format))
            unavailable_time_file.write("\n")

        unavailable_time_file.close()

    else:
        # 集群怎么说
        pass
