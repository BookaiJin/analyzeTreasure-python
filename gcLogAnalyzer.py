#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" main """
# 传入一个月的gc日志文件夹/path/gcLogs解析出宕机了几次，每次宕机的相关信息，输出到文件/path/gcDownTimeResult.log

import os

__author__ = 'bokai'


def analyze_gc_log_path(gc_log_path):
    gc_downtime_result = gc_log_path + os.sep + 'gcDownTimeResult.log'
    gc_downtime_result_result = open(gc_downtime_result)


if __name__ == '__main__':
    gc_log_path = input('输出gc日志的文件夹名:')
    analyze_gc_log_path(gc_log_path)