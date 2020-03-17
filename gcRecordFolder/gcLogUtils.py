#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 解析gc日志 '

__author__ = 'bokai'

import datetime
import pytz


# 给个dict，和表头[logStr日志内容,gcStartTime用于排序]，返回一个str


def generateGcLog(gcRecordDict, headerList):
    gcStartTimestamp = gcRecordDict.get('gcStartTime')
    # 时间戳ms转为s
    gcStartTime = datetime.datetime.fromtimestamp(int(gcStartTimestamp) / 1000,
                                                  pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    gcStartTime = gcStartTime[:23] + gcStartTime[26:]

    youngResultStrTemp = '{}: [{} ({}) [PSYoungGen: {}K->{}K({}K)] {}K->{}K({}K), {} secs] [Times: real={} secs] [pid:{}]'
    # {}: [{} ({}) [PSYoungGen: {}K->{}K({}K)] {}K->{}K({}K), {} secs] [Times: real={} secs]
    # 2019-12-05T01:43:05.435+0800: 60637.045: [GC (Allocation Failure) [PSYoungGen: 1028864K->1984K(1006080K)] 2712558K->1685718K(4730368K), 0.022 secs] [Times: real=0.022 secs]

    fullResultStrTemp = '{}: [{} ({}) [PSYoungGen: {}K->{}K({}K)] [ParOldGen: {}K->{}K({}K)] {}K->{}K({}K), [Metaspace: {}K->{}K({}K)], {} secs] [Times: real={} secs] [pid:{}]'
    # {}: [{} ({}) [PSYoungGen: {}K->{}K({}K)] [ParOldGen: {}K->{}K({}K)] {}K->{}K({}K), [Metaspace: {}K->{}K({}K)], {} secs] [Times: real={} secs]
    # 2019-12-05T09:01:33.354+0800: 86944.964: [Full GC (System.gc()) [PSYoungGen: 96K->0K(3393536K)] [ParOldGen: 341136K->341075K(3211776K)] 341232K->341075K(6605312K), [Metaspace: 150304K->150304K(154008K)], 0.295 secs] [Times: real=0.295 secs]

    if gcRecordDict['gcType'] == 'GC':
        resultStr = youngResultStrTemp.format(gcStartTime, gcRecordDict.get('gcType'), gcRecordDict.get('gcCause'),
                                              gcRecordDict.get('youngBeforeUsed'), gcRecordDict.get('youngAfterUsed'),
                                              gcRecordDict.get('youngAfterCommitted'),
                                              gcRecordDict.get('heapBeforeUsed'),
                                              gcRecordDict.get('heapAfterUsed'),
                                              gcRecordDict.get('heapAfterCommitted'),
                                              int(gcRecordDict.get('duration')) / 1000,
                                              int(gcRecordDict.get('duration')) / 1000,
                                              gcRecordDict.get('pid'))

    if gcRecordDict['gcType'] == 'Full GC':
        resultStr = fullResultStrTemp.format(gcStartTime, gcRecordDict.get('gcType'), gcRecordDict.get('gcCause'),
                                             gcRecordDict.get('youngBeforeUsed'), gcRecordDict.get('youngAfterUsed'),
                                             gcRecordDict.get('youngAfterCommitted'), gcRecordDict.get('oldBeforeUsed'),
                                             gcRecordDict.get('oldAfterUsed'), gcRecordDict.get('oldAfterCommitted'),
                                             gcRecordDict.get('heapBeforeUsed'),
                                             gcRecordDict.get('heapAfterUsed'),
                                             gcRecordDict.get('heapAfterCommitted'),
                                             gcRecordDict.get('metaspaceBeforeUsed'),
                                             gcRecordDict.get('metaspaceAfterUsed'),
                                             gcRecordDict.get('metaspaceAfterCommitted'),
                                             int(gcRecordDict.get('duration')) / 1000,
                                             int(gcRecordDict.get('duration')) / 1000,
                                             gcRecordDict.get('pid'))

    result = {'log': resultStr, 'gcStartTime': gcStartTimestamp, 'node': gcRecordDict.get('node')}
    return result


if __name__ == '__main__':
    timeStamp = input('输入时间戳:')
    # gcStartTime = datetime.datetime.strftime(
    #     datetime.datetime.fromtimestamp(int(timeStamp)/1000), '%Y-%m-%dT%H:%M:%S.%f%z')
    gcStartTime = datetime.datetime.fromtimestamp(int(timeStamp) / 1000,
                                                  pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    print(gcStartTime)
