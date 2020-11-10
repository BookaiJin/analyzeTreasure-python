#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 文件按照key排序 """

__author__ = 'bokai'

import csv
import os
import zipfile


def find_duplicate_class_from_list(all_jar_file_full_name_list):

    # 解压jar的路径 class_file_name:jar的键值对 重复添加到duplicate_class_jar_list_dict
    # 遍历的最终结果 {'com.fr.A':'a.jar', 'com.fr.B':'b.jar c.jar‘}
    # 展示的最终结果 {'com.fr.B':['b.jar', 'c.jar']}
    all_class_jar_dict = {}
    duplicate_class_jar_list_dict = {}

    for jar_file_name in all_jar_file_full_name_list:
        jar_file = zipfile.ZipFile(jar_file_name, 'r')
        for class_file in jar_file.filelist:
            class_file_name = class_file.filename
            if class_file_name[-6:] != '.class':
                continue
            if class_file_name not in all_class_jar_dict:
                all_class_jar_dict[class_file_name] = jar_file_name
            else:
                duplicate_class_jar_list = [jar_file_name, all_class_jar_dict[class_file_name]]
                duplicate_class_jar_list_dict[class_file_name] = duplicate_class_jar_list

    return duplicate_class_jar_list_dict


def find_duplicate_class(to_find_full_path):
    # dir里面有dir 遍历dir
    # 最终dir里面有jar 遍历jar

    all_jar_file_full_name_list = []
    add_jar_file_list(to_find_full_path, all_jar_file_full_name_list)

    duplicate_class_jar_list_dict = find_duplicate_class_from_list(all_jar_file_full_name_list)

    file = open(to_find_full_path + 'duplicate_class.log', 'w')
    file_header = ['duplicate_class', 'jars']
    file_writer = csv.DictWriter(file, file_header)
    file_writer.writeheader()

    for key, value in duplicate_class_jar_list_dict.items():
        row = {'duplicate_class': key, 'jars': value}
        file_writer.writerow(row)

    file.close()


def add_jar_file_list(path, all_jar_file_full_name_list):
    for path, dir_list, file_list in os.walk(path):
        for file in file_list:
            if file.endswith('.jar'):
                all_jar_file_full_name_list.append(path + os.sep + file)


if __name__ == '__main__':
    to_find_path = input('输入待查找的路径：')
    find_duplicate_class(to_find_path)
