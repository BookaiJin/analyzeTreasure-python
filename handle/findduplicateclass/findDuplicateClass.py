#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 筛选出文件夹下重复的class """
import traceback

__author__ = 'bokai'

import os
import zipfile

# 输入的路径
error_log_file = None
result_file = None


def find_duplicate_class_from_list(all_jar_file_full_name_list):
    # 解压jar的路径 class_file_name:jar的键值对 重复添加到duplicate_class_jar_list_dict
    # 遍历的最终结果 {'com.fr.A':'a.jar', 'com.fr.B':'b.jar c.jar‘}
    # 展示的最终结果 {'com.fr.B':['b.jar', 'c.jar']}
    all_class_jar_dict = {}
    duplicate_class_jar_list_dict = {}

    global error_log_file
    for jar_file_name in all_jar_file_full_name_list:
        try:
            jar_file = zipfile.ZipFile(jar_file_name, 'r')
            for class_file in jar_file.filelist:
                class_file_name = class_file.filename
                if class_file_name[-6:] != '.class':
                    continue
                if class_file_name not in all_class_jar_dict:
                    all_class_jar_dict[class_file_name] = [jar_file_name]
                else:
                    all_class_jar_dict[class_file_name].append(jar_file_name)
                    duplicate_class_jar_list_dict[class_file_name] = all_class_jar_dict[class_file_name]
        except Exception as e:
            error_log_file.write('error file: ' + jar_file_name + '\n' + str(e) + '\n' + traceback.format_exc())
    error_log_file.close()
    return duplicate_class_jar_list_dict


def find_duplicate_class(to_find_full_path):
    # dir里面有dir 遍历dir
    # 最终dir里面有jar 遍历jar

    all_jar_file_full_name_list = []
    add_jar_file_list(to_find_full_path, all_jar_file_full_name_list)

    duplicate_class_jar_list_dict = find_duplicate_class_from_list(all_jar_file_full_name_list)

    global result_file
    for key, value in duplicate_class_jar_list_dict.items():
        result_file.write(key + "\n")
        for duplicate_class_jar_file in value:
            result_file.write('\t')
            result_file.write(duplicate_class_jar_file)
            result_file.write('\n')
    result_file.close()


def add_jar_file_list(path, all_jar_file_full_name_list):
    for path, dir_list, file_list in os.walk(path):
        for file in file_list:
            if file[-4:] == '.jar':
                all_jar_file_full_name_list.append(path + os.sep + file)


if __name__ == '__main__':
    to_find_path = input('输入待查找的路径：')
    result_file = open(to_find_path + os.sep + 'duplicate_class.log', 'w')
    error_log_file = open(to_find_path + os.sep + 'error.log', 'w')
    find_duplicate_class(to_find_path)
    print('处理完毕，' + error_log_file.name + '查看处理异常，' + result_file.name + '查看结果')
