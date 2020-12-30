import os


def generate(des_directory):
    result_file = des_directory + os.sep + 'total_sql_cal.csv'
    result_file_writer = open(result_file, 'w')
    # 遍历日压缩包
    execute_sql_directory = os.walk(des_directory)
    # dayZip is one of tuple 0:top文件名 1:dir文件夹 2:nondir文件
    for parent, dic, execute_sql_total_cal_file_list in execute_sql_directory:
        for execute_sql_total_cal_file in execute_sql_total_cal_file_list:
            if execute_sql_total_cal_file.startswith('treas') and execute_sql_total_cal_file.endswith('executeSqlCalTotal.csv'):
                with open(parent + os.sep + execute_sql_total_cal_file) as file:
                    row = file.read()
                    result_file_writer.write(row + '\n')

    result_file_writer.close()


if __name__ == '__main__':
    treasure_path = input('输入treasure最外层文件夹「合并sql执行详情」: ')
    generate(treasure_path)
    # input('Please input any key to exit')
