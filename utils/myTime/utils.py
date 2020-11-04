#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""时间格式处理工具类"""
import datetime

import pytz

__author__ = 'bokai'

import time


def convert_time_to_date(time_str):
    local_time = time.localtime(int(time_str) / 1000)
    return time.strftime('%Y-%m-%dT%H:%M:%S', local_time)


def convert_time2date_timezone(time_str):
    return datetime.datetime.fromtimestamp(int(time_str) / 1000,
                                    pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
