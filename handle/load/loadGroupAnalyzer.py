#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from entity.focuspoint.message.LoadGroupMessage import LoadGroupMessage

""" main """

__author__ = 'bokai'


def analyze_load_detail(load_group_message):
    release_rec = load_group_message.release_detail
    interrupt_rec = load_group_message.interrupt_detail
    limit_rec = load_group_message.limit_detail

    """
    {
        "high":
        {"times":3, "details":[{"time":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]},{"time":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]},{"time":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]}]},
        "terrible": 
        {"times":5, "details":[{"time":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]},{"time":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]},{"time":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]},{"time":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]},{"time":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]}]},
        "endanger": 
        {"times":2, "details":[{"time":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]},{"time":"xxx", "release_rec":[], "interrupt_rec":[], "limit_rec":[]}]}
    }
    """
    result = {}

    i = 0
    j = 1
    while j < len(release_rec):
        current_release = release_rec[i]
        next_release = release_rec[j]

        current_release_time = current_release['time']
        next_release_time = next_release['time']
        for interrupt in interrupt_rec:
            if current_release_time < interrupt['time'] < next_release_time:
                pass
        i += 1
        j += 1
