#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""时间格式处理工具类"""

__author__ = 'bokai'

import time

def convert_time_to_date(time_str):
    local_time = time.localtime(int(time_str) / 1000)
    return time.strftime('%Y-%m-%dT%H:%M:%S', local_time)
