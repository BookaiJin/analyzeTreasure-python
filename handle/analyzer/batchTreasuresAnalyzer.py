import os

from file.execute.utilsBoxes import mergeExecuteSqlTotalInfo
from handle.analyzer import treasureAnalyzer


def batch_treasures_analyzer(des_path):
    for parent, dic, treasure_file_list in os.walk(des_path):
        for treasure_file in treasure_file_list:
            if treasure_file.startswith('treas') and treasure_file.endswith('.zip'):
                try:
                    treasureAnalyzer.start_analyze(parent + os.sep + treasure_file)
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    to_analyze_treasures_path = input('输入待处理的所有单月数据包的文件夹：')
    batch_treasures_analyzer(to_analyze_treasures_path)
    mergeExecuteSqlTotalInfo.generate(to_analyze_treasures_path)
