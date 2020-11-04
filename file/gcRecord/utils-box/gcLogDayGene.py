#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 按日解析gcRecord生成gclog便于比对 '

__author__ = 'bokai'

import os
import csv
import file.gcRecordFolder.utils.gcLogUtils


def generate_day_log(gc_record_file):
    # /Users/bokai/Downloads/永不宕机/衣架/treas202002result/gclog/gcRecord20200204.csv
    result_day_gc_log = gc_record_file + os.extsep + gc_record_file[-6:-4]
    if os.path.exists(result_day_gc_log):
        print(result_day_gc_log, ' - result log file already exists.')
        return
    result_gc_log_file = open(result_day_gc_log, 'w')
    result_gc_log_file_header = ['log', 'gcStartTime', 'node']
    result_gc_log_file_writer = csv.DictWriter(result_gc_log_file, result_gc_log_file_header)
    result_gc_log_file_writer.writeheader()

    gc_csv_file = open(gc_record_file, 'r')
    gc_file_reader = csv.DictReader(gc_csv_file)
    for row in gc_file_reader:
        gcRow = file.gcRecordFolder.utils.gcLogUtils.generate_gc_log(row)
        result_gc_log_file_writer.writerow(gcRow)

    gc_csv_file.close()
    utils.analyzeFileUtils.analyzeFileUtils.sortFileMessage(result_day_gc_log, ['node', 'gcStartTime'])


if __name__ == '__main__':
    gc_record = input('一天的gcRecord文件: ')
    generate_day_log(gc_record)
