#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 按日解析gcRecord生成gclog便于比对 '
import os
import re

from entity.gc.GcInfoMessage import GcInfoMessage
from entity.gc.load.GcLoadInfo import GcLoadInfo

__author__ = 'bokai'


def generate_load_from_gc_log(gc_log_full_name):
    gc_load_file_full_name = gc_log_full_name + '.result.log'
    writer = open(gc_load_file_full_name, 'a+')
    writer.write('No, GcType, young_release, young_promote, old_use_rate, old_release\n')
    reader = open(gc_log_full_name, 'r')
    gc_items_dict = {'gcStartTime': 0, 'gcType': '', 'gcCause': '', 'youngBeforeUsed': 0, 'youngAfterUsed': 0, 'youngAfterCommitted': 0,
                     'oldBeforeUsed': 0, 'oldAfterUsed': 0, 'oldAfterCommitted': 0, 'heapBeforeUsed': 0, 'heapAfterUsed': 0, 'heapAfterCommitted': 0,
                     'duration': 0, 'pid': '', 'node': ''}
    last_gc_info = GcInfoMessage(gc_items_dict)
    current_gc_info = GcInfoMessage(gc_items_dict)
    line_count = 0
    for row in reader.readlines():
        line_count += 1
        if re.match(GcInfoMessage.gc_log_young_reg, row):
            gc_items = re.match(GcInfoMessage.gc_log_young_reg, row).groups()
            gc_items_dict['gcType'] = str(gc_items[1])
            gc_items_dict['gcCause'] = str(gc_items[2])
            gc_items_dict['youngBeforeUsed'] = gc_items[3]
            gc_items_dict['youngAfterUsed'] = gc_items[4]
            gc_items_dict['youngAfterCommitted'] = gc_items[5]
            gc_items_dict['heapBeforeUsed'] = gc_items[6]
            gc_items_dict['heapAfterUsed'] = gc_items[7]
            gc_items_dict['heapAfterCommitted'] = gc_items[8]
            gc_items_dict['duration'] = gc_items[9]
            current_gc_info = GcInfoMessage(gc_items_dict)
        if re.match(GcInfoMessage.gc_log_full_reg, row):
            gc_items = re.match(GcInfoMessage.gc_log_full_reg, row).groups()
            gc_items_dict['gcType'] = str(gc_items[1])
            gc_items_dict['gcCause'] = str(gc_items[2])
            gc_items_dict['youngBeforeUsed'] = gc_items[3]
            gc_items_dict['youngAfterUsed'] = gc_items[4]
            gc_items_dict['youngAfterCommitted'] = gc_items[5]
            gc_items_dict['oldBeforeUsed'] = gc_items[6]
            gc_items_dict['oldAfterUsed'] = gc_items[7]
            gc_items_dict['oldAfterCommitted'] = gc_items[8]
            gc_items_dict['heapBeforeUsed'] = gc_items[9]
            gc_items_dict['heapAfterUsed'] = gc_items[10]
            gc_items_dict['heapAfterCommitted'] = gc_items[11]
            gc_items_dict['duration'] = gc_items[15]
            current_gc_info = GcInfoMessage(gc_items_dict)
        # 当前条gc日志的负载得分
        gc_load_dict = {'gcType': '', 'young_release': 0, 'young_promote': 0, 'old_use_rate': 0.0, 'old_release': 0}
        if current_gc_info.get_gc_type() == 'GC':
            gc_load_dict['gcType'] = 'YGC'
            gc_load_dict['young_promote'] = (current_gc_info.after_heap - current_gc_info.after_young) - (
                    current_gc_info.before_heap - current_gc_info.before_young)
        elif current_gc_info.get_gc_type() == 'Full GC':
            gc_load_dict['gcType'] = 'FGC'
            gc_load_dict['young_promote'] = current_gc_info.before_old - (last_gc_info.after_heap - last_gc_info.after_young)
            gc_load_dict['old_release'] = current_gc_info.before_old - current_gc_info.after_old - int(gc_load_dict['young_promote'])
        gc_load_dict['young_release'] = current_gc_info.before_young - current_gc_info.after_young - int(gc_load_dict['young_promote'])
        gc_load_dict['old_use_rate'] = current_gc_info.after_old / current_gc_info.committed_old
        gc_load_info = GcLoadInfo(gc_load_dict)
        # 写负载得分
        writer.write(str(line_count) + ', ' + gc_load_info.to_load_log() + '\n')
        # 更新
        last_gc_info = current_gc_info


if __name__ == '__main__':
    gc_log_file = input('一天的gcRecord文件: ')
    generate_load_from_gc_log(gc_log_file)
