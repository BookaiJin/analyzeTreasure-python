#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from entity.focuspoint.message.LoadGroupMessage import LoadGroupMessage

""" main """

__author__ = 'bokai'


def analyze_load_detail(load_group_message, focuspoint_full_name):
    focuspoint_summary_full_name = focuspoint_full_name + '.summary.json'
    focuspoint_summary_file = open(focuspoint_summary_full_name, 'w')

    release_rec = sorted(load_group_message.release_detail,key=lambda e:e.__getitem__('time'))
    interrupt_rec = load_group_message.interrupt_detail
    limit_rec = load_group_message.limit_detail

    """
    {
        "release_times":20,
        "limit_times":10,
        "interrupt_times":20,
        "high":
        {"times":3, "interrupt_times":1, "limit_times":2, "details":[{"date":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]},{"date":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]},{"date":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]}]},
        "terrible": 
        {"times":5, "interrupt_times":1, "limit_times":2,  "details":[{"date":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]},{"date":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]},{"date":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]},{"date":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]},{"date":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]}]},
        "endanger": 
        {"times":2, "interrupt_times":1, "limit_times":2,  "details":[{"date":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]},{"date":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]}]}
    }
    FR-F4003,1620615433112,2021-05-10T10:57:13,,,1,,release record,"{'killCountCell': '2', 'gcStartTime': '1620615409600', 'node': '', 'load': 'TERRIBLE', 'killCountTime': '796', 'sessionCount': '2518', 'type': 'TERRIBLEKill', 'killCountSum': '798'}"
    FR-F4004,1620874315362,2021-05-13T10:51:55,iZuf6gp5n4j4os5gxhiozpZ,68830aef4dbfad181162f9251a1da51b,4,customer/customer_move.cpt,,"{'number': 0, 'node': 'iZuf6gp5n4j4os5gxhiozpZ', 'metric': 1, 'serial': 4992, 'trigger': False, 'scene': 'WRITE_CARTESIAN'}"
    FR-F4002,1620304402365,2021-05-06T20:33:22,,,1,service/update_IMCC_quesstatus.cpt,template restriction,"{'reason': 'limit', 'node': '', 'cellNum': '0', 'load': 'LOW', 'sessionid': '4dc2e4c4-475e-4fa2-b59d-798c4edf0010', 'detail': 'SQL_TIME'}"
    """
    result = {
        "release_times": len(release_rec), "interrupt_times": len(interrupt_rec), "limit_times": len(limit_rec),
        "HIGH": {"times": 0, "interrupt_times": 0, "limit_times": 0, "details": []},
        "TERRIBLE": {"times": 0, "interrupt_times": 0, "limit_times": 0, "details": []},
        "ENDANGER": {"times": 0, "interrupt_times": 0, "limit_times": 0, "details": []}
    }

    i = 0
    j = 1
    while i < len(release_rec):
        current_release = release_rec[i]
        current_release_time = int(current_release['time'])

        next_release_time = sys.maxsize
        if j < len(release_rec):
            next_release = release_rec[j]
            next_release_time = int(next_release['time'])

        try:
            if current_release['body'] != '':
                result[current_release['body']['load']]['times'] += 1
        except TypeError as e:
            # print(e)
            print(' ', result[current_release['body']['load']]['times'])
        release_detail = [current_release]
        interrupt_detail = []
        limit_detail = []
        detail_one = {"date": current_release['date'], "release_rec": release_detail, "interrupt": interrupt_detail, "limit": limit_detail}
        if current_release['body'] != '':
            result[current_release['body']['load']]['details'].append(detail_one)

        for interrupt in interrupt_rec:
            if current_release_time <= int(interrupt['time']) < next_release_time and int(interrupt['time']) - current_release_time < 10 * 60 * 1000:
                interrupt_detail.append(interrupt)

        for limit in limit_rec:
            if current_release_time <= int(limit['time']) < next_release_time and int(limit['time']) - current_release_time < 10 * 60 * 1000:
                limit_detail.append(limit)

        if current_release['body']!='':
            result[current_release['body']['load']]['interrupt_times'] += len(interrupt_detail)
            result[current_release['body']['load']]['limit_times'] += len(limit_detail)

        i += 1
        j += 1

    content = str(result).replace("'", "\"").replace("True", "\"True\"").replace("False", "\"False\"")
    focuspoint_summary_file.write(content + '\n')
