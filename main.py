#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" main """

__author__ = 'bokai'

import os
import zipfile
import realTimeUsage.realTimeUsage
import gcRecordFolder.gcRecord
import time

import focusPoint.focusPoint


# zippath/treas201901.zip


def startAnaly(treasurePath):
    # shortName treas201901
    zipFileShortName = str.split(
        str.split(treasurePath, os.extsep)[0], os.sep)[-1]
    # zippath/result/
    desResultPath = os.sep.join(
        str.split(treasurePath, os.extsep)[:1]) + 'result'
    startTime = time.time()
    print('start')

    # zippath/result/zip/
    zipDesResultPath = desResultPath + os.sep + 'zip'
    # 读取月数据包里面的日压缩包
    zFile = zipfile.ZipFile(treasurePath, 'r')
    for dayZip in zFile.namelist():
        if dayZip.endswith('.zip'):
            # 解压出日压缩包，treas20190101.zip、treas20190102.zip、treas20190103.zip...
            zFile.extract(dayZip, zipDesResultPath)

    # 解压出来的gcRecord文件 zippath/result/gclog/gcRecord类文件
    gcRecordFilesPath = desResultPath + os.sep + 'gclog'
    # 解压出来的focusPoint文件 zippath/result/focuspoint/focuspoint类文件
    focuspointFilesPath = desResultPath + os.sep + 'focuspoint'
    # 解压出来的realTimeUsage文件 zippath/result/realTimeUsage/realTimeUsage类文件
    realTimeUsageFilesPath = desResultPath + os.sep + 'realtimeusage'
    # 合并后的gc日志 zippath/result/treas201901.gc.log
    gcFileFullName = desResultPath + os.sep + zipFileShortName + '.gc.log'
    # 解析focusPoint文件夹 zippath/result/treas201901.focuspoint.log
    focuspointFileFullName = desResultPath + os.sep + zipFileShortName + '.focuspoint.csv'
    # 解析reamTime文件夹 zippath/result/treas201901.reamtime.log
    realTimeUsageFileFullName = desResultPath + os.sep + zipFileShortName + ".realtime.csv"

    # 遍历日压缩包
    zipDic = os.walk(zipDesResultPath)
    # dayZip is one of tuple 0:top文件名 1:dir文件夹 2:nondir文件
    for parent, dic, dayZip in zipDic:
        # 满足条件时 dayZip是个list,zippath/zip/treas201901/treas20190101.zip
        for sigleDayZip in dayZip:
            if sigleDayZip.endswith('.zip') and (not sigleDayZip.startswith('.')):
                # 解压日压缩包，取出各个需要分析的文件
                dayUnzip = zipfile.ZipFile(parent + os.sep + sigleDayZip, 'r')
                # 读取文件，分focusPoint和gcRecord两类文件解压
                for dayFile in dayUnzip.namelist():
                    # gcRecord文件处理
                    if dayFile.startswith('gcRecord'):
                        dayUnzip.extract(dayFile, gcRecordFilesPath)

                    # focuspoint文件处理
                    if dayFile.startswith('focusPoint'):
                        dayUnzip.extract(dayFile, focuspointFilesPath)

                    # realTimeUsage文件处理
                    if dayFile.startswith('realTime'):
                        dayUnzip.extract(dayFile, realTimeUsageFilesPath)

    unzipEndTime = time.time()
    print('unzip time:', (unzipEndTime - startTime) * 1000, 'ms')

    gcRecordFolder.gcRecord.generateGclog(gcRecordFilesPath, gcFileFullName)
    focusPoint.focusPoint.generateFocusPointFile(focuspointFilesPath, focuspointFileFullName)
    realTimeUsage.realTimeUsage.generateRealTimeUsage(realTimeUsageFilesPath, realTimeUsageFileFullName)

    endTime = time.time()
    print('total time:', (endTime - startTime) * 1000, 'ms')


if __name__ == '__main__':
    treasurePath = input('输入treasure文件路径: ')
    startAnaly(treasurePath)
