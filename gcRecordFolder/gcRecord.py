#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 解析gc日志 """

__author__ = 'bokai'

import os
import csv
import gcRecordFolder.gcLogUtils
import analyzeFileUtils.analyzeFileUtils


# 给一个gclog解压后的路径，解析里面的gcRecord文件
# zippath/result/gclog/gcRecord类文件
# 解析后合并的文件名
# zippath/result/treas201901.gc.log


def generateGclog(gclogPath, gclogFullName):
    if not os.path.exists(gclogPath):
        print('这个版本的treas包没有gcRecord表. fu*k u')
        return
    if os.path.exists(gclogFullName):
        print(gclogFullName, ' - result gc log file already exist.')
        return
    resultGcLogFile = open(gclogFullName, 'w')
    resultGcLogFileHeader = ['log', 'gcStartTime', 'node']
    resultGcLogFileWriter = csv.DictWriter(resultGcLogFile, resultGcLogFileHeader)
    resultGcLogFileWriter.writeheader()
    for parent, dirname, filenames in os.walk(gclogPath):
        for filename in filenames:
            if filename.startswith('gcRecord') and filename.endswith('.csv'):
                # 打开每个文件
                gcCsvFile = open(parent + os.sep + filename, 'r')
                gcFileReader = csv.DictReader(gcCsvFile)
                try:
                    for row in gcFileReader:
                        gcRow = gcRecordFolder.gcLogUtils.generateGcLog(row, resultGcLogFileHeader)
                        resultGcLogFileWriter.writerow(gcRow)
                except Exception:
                    print("gcRecord row read failed.", filename, 'line:', gcFileReader.line_num)

                gcCsvFile.close()

    # 先按照节点排序，分隔开之后，在按照时间排序
    analyzeFileUtils.analyzeFileUtils.sortFileMessage(gclogFullName, ['node', 'gcStartTime'])
