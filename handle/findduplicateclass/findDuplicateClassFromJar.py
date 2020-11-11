#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 从指定的文件夹下，找与指定jar包重复的class """

__author__ = 'bokai'


def find_duplicate_class_from_jar(all_jar_dir, duplicate_class_from_jar_full_name):
    # 保存待分析jar包的 class:jar_file_name 的dict
    # 遍历路径 all_jar_dir，已经包含的class记录为冲突，规避掉指定的jar避免重复扫描

    pass


if __name__ == '__main__':
    to_find_all_jar_dir = input("所有jar包路径：")
    duplicate_class_from_jar_file_full_name = input("报错class所属jar包路径：")
    find_duplicate_class_from_jar(to_find_all_jar_dir, duplicate_class_from_jar_file_full_name)
