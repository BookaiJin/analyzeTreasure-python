#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" main """
from file.focusPoint import focusPoint
from file.gcRecord import gcRecord
from file.realTimeUsage import realTimeUsage
from handle.unavailabletime import unavailableTimeAnalyzer

__author__ = 'bokai'

import os
import zipfile
import shutil
import time


# zippath/treas201901.zip


def start_analyze(treasure2analyze_path):
    # shortName treas201901
    zip_file_short_name = str.split(
        str.split(treasure2analyze_path, os.extsep)[0], os.sep)[-1]
    # zippath/result/
    des_result_path = os.sep.join(
        str.split(treasure2analyze_path, os.extsep)[:1]) + 'result'
    start_time = time.time()
    print('start')

    # zippath/result/zip/
    zip_des_result_path = des_result_path + os.sep + 'zip'
    # 读取月数据包里面的日压缩包
    z_file = zipfile.ZipFile(treasure2analyze_path, 'r')
    for dayZip in z_file.namelist():
        if dayZip.endswith('.zip'):
            # 解压出日压缩包，treas20190101.zip、treas20190102.zip、treas20190103.zip...
            z_file.extract(dayZip, zip_des_result_path)

    # 解压出来的gcRecord文件 zippath/result/gclog/gcRecord类文件
    gc_record_files_path = des_result_path + os.sep + 'gclog'
    # 解压出来的focusPoint文件 zippath/result/focuspoint/focuspoint类文件
    focuspoint_files_path = des_result_path + os.sep + 'focuspoint'
    # 解压出来的realTimeUsage文件 zippath/result/realTimeUsage/realTimeUsage类文件
    realtime_usage_files_path = des_result_path + os.sep + 'realtimeusage'
    # 合并后的gc日志 zippath/result/treas201901.gc.log
    gc_file_full_name = des_result_path + os.sep + zip_file_short_name + '.gc.log'
    # 解析focusPoint文件夹 zippath/result/treas201901.focuspoint.log
    focuspoint_file_full_name = des_result_path + os.sep + zip_file_short_name + '.focuspoint'
    # 解析reamTime文件夹 zippath/result/treas201901.reamtime.log
    real_time_usage_file_full_name = des_result_path + os.sep + zip_file_short_name + ".realtime.csv"
    # 解析不可用时长结果
    unavailable_time_file_full_name = des_result_path + os.sep + zip_file_short_name + ".unavailable"

    # 遍历日压缩包
    zip_dic = os.walk(zip_des_result_path)
    # dayZip is one of tuple 0:top文件名 1:dir文件夹 2:nondir文件
    for parent, dic, dayZip in zip_dic:
        # 满足条件时 dayZip是个list,zippath/zip/treas201901/treas20190101.zip
        for single_day_zip in dayZip:
            if single_day_zip.endswith('.zip') and (not single_day_zip.startswith('.')):
                # 解压日压缩包，取出各个需要分析的文件
                day_unzip = zipfile.ZipFile(parent + os.sep + single_day_zip, 'r')
                # 读取文件，分focusPoint和gcRecord两类文件解压
                for dayFile in day_unzip.namelist():
                    # gcRecord文件处理
                    if dayFile.startswith('gcRecord'):
                        day_unzip.extract(dayFile, gc_record_files_path)

                    # focuspoint文件处理
                    if dayFile.startswith('focusPoint'):
                        day_unzip.extract(dayFile, focuspoint_files_path)

                    # realTimeUsage文件处理
                    if dayFile.startswith('realTime'):
                        day_unzip.extract(dayFile, realtime_usage_files_path)

    unzip_end_time = time.time()
    print('unzip time:', (unzip_end_time - start_time) * 1000, 'ms')

    # 删除日压缩包
    shutil.rmtree(zip_des_result_path)

    gc_info_message_node_pid_detail = gcRecord.generate_gc_log_and_get_node_pid_gc_info_list_detail(
        gc_record_files_path, gc_file_full_name)
    realtime_usage_node_pid_list_detail = realTimeUsage.generate_realtime_usage_and_get_node_pid_realtime_info_list_detail(
        realtime_usage_files_path, real_time_usage_file_full_name)
    focuspoint_wrapper = focusPoint.generate_focuspoint_log_and_get_focuspoint_node_pid_list_detail(focuspoint_files_path,
                                                                                                    focuspoint_file_full_name)

    end_time = time.time()
    print('analyze total time:', (end_time - start_time) * 1000, 'ms\n')

    print('不可用时长分析')
    unavailable_start_time = time.time()
    unavailableTimeAnalyzer.analyze_unavailable_time(gc_info_message_node_pid_detail, realtime_usage_node_pid_list_detail,
                                                     focuspoint_wrapper, unavailable_time_file_full_name)
    unavailable_end_time = time.time()
    print('unavailable analyze total time:', (unavailable_end_time - unavailable_start_time) * 1000, 'ms')


if __name__ == '__main__':
    treasure_path = input('输入treasure文件路径: ')
    start_analyze(treasure_path)
