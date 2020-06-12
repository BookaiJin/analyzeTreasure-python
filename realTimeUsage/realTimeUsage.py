#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' main '
import csv

__author__ = 'bokai'

import os
import time
import analyzeFileUtils.analyzeFileUtils


def generateRealTimeUsage(realTimeUsagePath, realTimeUsageFullName):
    if not os.path.exists(realTimeUsagePath):
        print('这个版本的treas包没有realTime表. fu*k u again')
        return
    if os.path.exists(realTimeUsageFullName):
        print(realTimeUsageFullName, ' - result gc log file already exist.')
        return
    resultRealTimeUsageLogFile = open(realTimeUsageFullName, 'w')
    resultRealTimeUsageFileHeader = ['date', 'time', 'node', 'cpu', 'memory', 'sessionnum', 'onlinenum', 'pid',
                                     'templateRequest', 'httpRequest', 'sessionRequest', 'fineIO', 'NIO',
                                     'bufferMemUse', 'physicalMemUse', 'physicalMemFree', '']

    resultRealTimeWriter = csv.DictWriter(resultRealTimeUsageLogFile, resultRealTimeUsageFileHeader)
    resultRealTimeWriter.writeheader()
    for parent, dirname, filenames in os.walk(realTimeUsagePath):
        # filenames是一个list所有focuspoint文件的集合
        for filename in filenames:
            if filename.startswith('realTime') and filename.endswith('.csv'):
                # 打开每个文件
                realTimeCsvFile = open(parent + os.sep + filename, 'r')
                reader = csv.DictReader(realTimeCsvFile)

                try:
                    # 按行读取dict格式的数据
                    for row in reader:
                        if '' in row:
                            # 时间戳ms转为s
                            localTime = time.localtime(int(row.get('time')) / 1000)
                            localTimeToSave = time.strftime('%Y-%m-%d %H:%M:%S', localTime)
                            row['date'] = localTimeToSave
                            resultRealTimeWriter.writerow(row)
                    realTimeCsvFile.close()
                except Exception:
                    print('record row error.', )

    resultRealTimeUsageLogFile.close()
    analyzeFileUtils.analyzeFileUtils.sortFileMessage(realTimeUsageFullName, ['time'])
