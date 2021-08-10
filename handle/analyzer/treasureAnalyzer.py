#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" main """
from entity.company.CompanyInfo import CompanyInfo
from file.execute import executeTemplate, executeSql
from file.focusPoint import focusPoint
from file.gcRecord import gcRecord
from file.realTimeUsage import realTimeUsage
from handle.load import loadGroupAnalyzer
from handle.unavailabletime import unavailableTimeAnalyzer

__author__ = 'bokai'

import os
import json
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
        if dayZip.endswith('.zip') or dayZip.endswith('.json'):
            # 解压出日压缩包，treas20190101.zip、treas20190102.zip、treas20190103.zip...
            z_file.extract(dayZip, zip_des_result_path)

    # 解压出来的gcRecord文件 zippath/result/gclog/gcRecord类文件
    gc_record_files_path = des_result_path + os.sep + 'gclog'
    # 解压出来的focusPoint文件 zippath/result/focuspoint/focuspoint类文件
    focuspoint_files_path = des_result_path + os.sep + 'focuspoint'
    # 解压出来的realTimeUsage文件 zippath/result/realTimeUsage/realTimeUsage类文件
    realtime_usage_files_path = des_result_path + os.sep + 'realtimeusage'
    # 解压出来的execute文件 zippath/result/execute/execute类文件
    execute_files_path = des_result_path + os.sep + 'execute'
    # 解压出来的executeSql文件 zippath/result/executeSql/executeSql类文件
    execute_sql_files_path = des_result_path + os.sep + 'executesql'
    # 合并后的gc日志 zippath/result/treas201901.gc.log
    gc_file_full_name = des_result_path + os.sep + zip_file_short_name + '.gc.log'
    # 解析focusPoint文件夹 zippath/result/treas201901.focuspoint.log
    focuspoint_file_full_name = des_result_path + os.sep + zip_file_short_name + '.focuspoint'
    # 解析reamTime文件夹 zippath/result/treas201901.reamtime.log
    real_time_usage_file_full_name = des_result_path + os.sep + zip_file_short_name + ".realtime.csv"
    # 解析不可用时长结果
    unavailable_time_file_full_name = des_result_path + os.sep + zip_file_short_name + ".unavailable"
    # 解析template执行时间
    execute_file_full_name = des_result_path + os.sep + zip_file_short_name + '.execute.csv'
    # 解析sql执行时间
    execute_sql_file_full_name = des_result_path + os.sep + zip_file_short_name + '.executeSql.csv'
    # 解析sql执行的时间汇总
    execute_sql_file_full_cal_name = des_result_path + os.sep + zip_file_short_name + '.executeSqlCalTotal.csv'

    # 当前treasure包的appId
    company_info = None

    # 遍历日压缩包
    zip_dic = os.walk(zip_des_result_path)
    # dayZip is one of tuple 0:top文件名 1:dir文件夹 2:nondir文件
    for parent, dic, dayZip in zip_dic:
        # 满足条件时 dayZip是个list,zippath/zip/treas201901/treas20190101.zip
        for single_day_zip in dayZip:
            # 获取 appId
            if single_day_zip.endswith('.json') and (not single_day_zip.startswith('.')):
                with open(parent + os.sep + single_day_zip, 'r') as load_f:
                    load_dict = json.load(load_f)
                company_info = CompanyInfo(str(load_dict['appId']), str(load_dict['time']))
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

                    # execute文件处理
                    if dayFile.startswith('execute') and not dayFile.startswith('executeSql'):
                        day_unzip.extract(dayFile, execute_files_path)

                    # executeSql文件处理
                    if dayFile.startswith('executeSql'):
                        day_unzip.extract(dayFile, execute_sql_files_path)

                    dayFile = None

    unzip_end_time = time.time()
    print(treasure2analyze_path + 'unzip time:', (unzip_end_time - start_time) * 1000, 'ms')

    # executeSql.generate_execute_sql(company_info, execute_sql_files_path, execute_sql_file_full_name, execute_sql_file_full_cal_name)
    cal_sql_end_time = time.time()
    print(treasure2analyze_path + 'cal sql time:', (cal_sql_end_time - start_time) * 1000, 'ms')
    # executeTemplate.generate_execute_template(execute_files_path, execute_sql_record_wrapper, execute_file_full_name)

    gc_info_message_node_pid_detail = gcRecord.generate_gc_log_and_get_node_pid_gc_info_list_detail(
        gc_record_files_path, gc_file_full_name)
    realtime_usage_node_pid_list_detail = realTimeUsage.generate_realtime_usage_and_get_node_pid_realtime_info_list_detail(
        realtime_usage_files_path, real_time_usage_file_full_name)
    focuspoint_wrapper = focusPoint.generate_focuspoint_log_and_get_focuspoint_node_pid_list_detail(focuspoint_files_path,
                                                                                                    focuspoint_file_full_name)

    end_time = time.time()
    print('analyze total time:', (end_time - start_time) * 1000, 'ms\n')

    loadGroupAnalyzer.analyze_load_detail(focuspoint_wrapper.load_group_message, focuspoint_file_full_name)

    print('不可用时长分析')
    unavailable_start_time = time.time()
    unavailableTimeAnalyzer.analyze_unavailable_time(gc_info_message_node_pid_detail, realtime_usage_node_pid_list_detail,
                                                     focuspoint_wrapper, unavailable_time_file_full_name)
    unavailable_end_time = time.time()
    print('unavailable analyze total time:', (unavailable_end_time - unavailable_start_time) * 1000, 'ms')

    # 删除日压缩包
    shutil.rmtree(zip_des_result_path)
    shutil.rmtree(execute_files_path)
    shutil.rmtree(execute_sql_files_path)
    shutil.rmtree(focuspoint_files_path)
    shutil.rmtree(gc_record_files_path)
    shutil.rmtree(realtime_usage_files_path)


if __name__ == '__main__':
    treasure_path = input('输入treasure文件路径(目前只支持单个月zip格式数据包解析「如treas202011.zip」): ')
    start_analyze(treasure_path)
    # input('Please input any key to exit')
