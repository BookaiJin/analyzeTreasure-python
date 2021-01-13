#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 按日解析gcRecord生成gclog便于比对 '
import os
import re

from entity.gc.GcInfoMessage import GcInfoMessage

__author__ = 'bokai'


def generate_load_from_gc_log(gc_log_full_name):
    gc_load_file_full_name = gc_log_full_name + os.sep + 'result' + os.sep + 'log'
    writer = open(gc_load_file_full_name, 'a+')
    reader = open(gc_log_full_name, 'r')
    last_gc_info = GcInfoMessage('')
    current_gc_info = GcInfoMessage('')
    gc_items_dict = {'gcStartTime': 0, 'gcType': '', 'gcCause': '', 'youngBeforeUsed': 0, 'youngAfterUsed': 0, 'youngAfterCommitted': 0,
                     'oldBeforeUsed': 0, 'oldAfterUsed': 0, 'oldAfterCommitted': 0, 'heapBeforeUsed': 0, 'heapAfterUsed': 0, 'heapAfterCommitted': 0,
                     'duration': 0, 'pid': '', 'node': ''}
    for row in reader.readlines():
        if re.match(GcInfoMessage.gc_log_young_reg, row):
            gc_items = re.match(GcInfoMessage.gc_log_young_reg, row).groups()
            gc_items_dict = gc_items[0]
        if re.match(GcInfoMessage.gc_log_full_reg, row):
            gc_items = re.match(GcInfoMessage.gc_log_full_reg, row).groups()
            gc_items_dict = gc_items[0]
            current_gc_info = GcInfoMessage('')
        # 当前条gc日志的负载得分

        # 写负载得分
        writer.write()
        # 更新
        last_gc_info = current_gc_info


if __name__ == '__main__':
    gc_log_file = input('一天的gcRecord文件: ')
    generate_load_from_gc_log(gc_log_file)
