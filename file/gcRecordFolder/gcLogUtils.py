#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 解析gc日志 """
# 弃用，溯源用
from entity.gc.GcInfoMessage import GcInfoMessage

__author__ = 'bokai'

import datetime
import pytz


# 给个dict，和表头[logStr日志内容,gcStartTime用于排序]，返回一个str


def generate_gc_log(gc_record_dict):
    gc_start_timestamp = gc_record_dict.get('gcStartTime')
    # 时间戳ms转为s
    gc_start_time = datetime.datetime.fromtimestamp(int(gc_start_timestamp) / 1000,
                                                    pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    gc_start_time = gc_start_time[:23] + gc_start_time[26:]

    young_result_str_temp = '{}: [{} ({}) [PSYoungGen: {}K->{}K({}K)] {}K->{}K({}K), {} secs] [Times: real={} secs] [pid:{}]'
    # {}: [{} ({}) [PSYoungGen: {}K->{}K({}K)] {}K->{}K({}K), {} secs] [Times: real={} secs]
    # 2019-12-05T01:43:05.435+0800: 60637.045: [GC (Allocation Failure) [PSYoungGen: 1028864K->1984K(1006080K)] 2712558K->1685718K(4730368K), 0.022 secs] [Times: real=0.022 secs]

    full_result_str_temp = '{}: [{} ({}) [PSYoungGen: {}K->{}K({}K)] [ParOldGen: {}K->{}K({}K)] {}K->{}K({}K), [Metaspace: {}K->{}K({}K)], {} secs] [Times: real={} secs] [pid:{}]'
    # {}: [{} ({}) [PSYoungGen: {}K->{}K({}K)] [ParOldGen: {}K->{}K({}K)] {}K->{}K({}K), [Metaspace: {}K->{}K({}K)], {} secs] [Times: real={} secs]
    # 2019-12-05T09:01:33.354+0800: 86944.964: [Full GC (System.gc()) [PSYoungGen: 96K->0K(3393536K)] [ParOldGen: 341136K->341075K(3211776K)] 341232K->341075K(6605312K), [Metaspace: 150304K->150304K(154008K)], 0.295 secs] [Times: real=0.295 secs]

    result_str = ''
    if gc_record_dict['gcType'] == 'GC':
        result_str = young_result_str_temp.format(gc_start_time, gc_record_dict.get('gcType'),
                                                  gc_record_dict.get('gcCause'),
                                                  gc_record_dict.get('youngBeforeUsed'),
                                                  gc_record_dict.get('youngAfterUsed'),
                                                  gc_record_dict.get('youngAfterCommitted'),
                                                  gc_record_dict.get('heapBeforeUsed'),
                                                  gc_record_dict.get('heapAfterUsed'),
                                                  gc_record_dict.get('heapAfterCommitted'),
                                                  int(gc_record_dict.get('duration')) / 1000,
                                                  int(gc_record_dict.get('duration')) / 1000,
                                                  gc_record_dict.get('pid'))

    if gc_record_dict['gcType'] == 'Full GC':
        result_str = full_result_str_temp.format(gc_start_time, gc_record_dict.get('gcType'),
                                                 gc_record_dict.get('gcCause'),
                                                 gc_record_dict.get('youngBeforeUsed'),
                                                 gc_record_dict.get('youngAfterUsed'),
                                                 gc_record_dict.get('youngAfterCommitted'),
                                                 gc_record_dict.get('oldBeforeUsed'),
                                                 gc_record_dict.get('oldAfterUsed'),
                                                 gc_record_dict.get('oldAfterCommitted'),
                                                 gc_record_dict.get('heapBeforeUsed'),
                                                 gc_record_dict.get('heapAfterUsed'),
                                                 gc_record_dict.get('heapAfterCommitted'),
                                                 gc_record_dict.get('metaspaceBeforeUsed'),
                                                 gc_record_dict.get('metaspaceAfterUsed'),
                                                 gc_record_dict.get('metaspaceAfterCommitted'),
                                                 int(gc_record_dict.get('duration')) / 1000,
                                                 int(gc_record_dict.get('duration')) / 1000,
                                                 gc_record_dict.get('pid'))

    result = {'log': result_str, 'gcStartTime': gc_start_timestamp, 'node': gc_record_dict.get('node')}
    return result


def generate_gc_obj(gc_record_dict):
    gc_obj = GcInfoMessage(gc_record_dict)
    return gc_obj


if __name__ == '__main__':
    timeStamp = input('输入时间戳:')
    # gcStartTime = datetime.datetime.strftime(
    #     datetime.datetime.fromtimestamp(int(timeStamp)/1000), '%Y-%m-%dT%H:%M:%S.%f%z')
    gcStartTime = datetime.datetime.fromtimestamp(int(timeStamp) / 1000,
                                                  pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    print(gcStartTime)
