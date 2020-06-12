#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""gc日志算中止得分balanceScore"""

__author__ = 'bokai'


def get_balance_score(log_path):
    # youngGen解析正则式
    REG_YOUNG_GEN = "[PSYoungGen: (\\d+)K->(\\d+)K\\((\\d+)\\)]"
    # oldGen解析正则式
    REG_OLD_GEN = "[ParOldGen: (\\d+)K->(\\d+)K\\((\\d+)\\)]"
    # heap
    REG_HEAP = '\\)] (\\d+)K->(\\d+)K\\((\\d+)\\),'
    # YoungGen & OldGen解析正则式
    REG_GEN = "\\[PSYoungGen: (\\d+)K->(\\d+)K\\((\\d+)K\\)\\] \\[ParOldGen: (\\d+)K->(\\d+)K\\((\\d+)K\\)\\]"
    log_reader=open(log_path,'r')
    last_old = 0
    last_young = 0
    last_time = 0
    for row in log_reader.readlines():
        if 'Full GC' not in row:
            pass
        else :
            pass


if __name__ == '__main__':
    log_name = input('gc日志名:')
    get_balance_score(log_name)
