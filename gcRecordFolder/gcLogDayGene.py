#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 按日解析gcRecord生成gclog便于比对 '

__author__ = 'bokai'

import os
import csv
import gcRecordFolder.gcLogUtils
import analyzeFileUtils.analyzeFileUtils


def generate_day_log(gc_record_file):
    # /Users/bokai/Downloads/永不宕机/衣架/treas202002result/gclog/gcRecord20200204.csv
    result_day_gc_log = gc_record_file + os.extsep + gc_record_file[-6:-4]
    if os.path.exists(result_day_gc_log):
        print(result_day_gc_log, ' - result log file already exists.')
        return
    resultGcLogFile = open(result_day_gc_log, 'w')
    resultGcLogFileHeader = ['log', 'gcStartTime', 'node']
    resultGcLogFileWriter = csv.DictWriter(resultGcLogFile, resultGcLogFileHeader)
    resultGcLogFileWriter.writeheader()

    gcCsvFile = open(gc_record_file, 'r')
    gcFileReader = csv.DictReader(gcCsvFile)
    for row in gcFileReader:
        gcRow = gcRecordFolder.gcLogUtils.generateGcLog(row, resultGcLogFileHeader)
        resultGcLogFileWriter.writerow(gcRow)

    gcCsvFile.close()
    analyzeFileUtils.analyzeFileUtils.sortFileMessage(result_day_gc_log, ['node', 'gcStartTime'])


if __name__ == '__main__':
    gc_record = input('一天的gcRecord文件: ')
    generate_day_log(gc_record)
