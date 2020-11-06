from utils.myTime import utils


class RealtimeUsage:
    __node = '0'
    __timestamps = 0
    __pid = '0'
    __physical_mem_free = 0
    __realtime_usage_dict = {}

    def __init__(self, row):
        self.__realtime_usage_dict['date'] = utils.convert_time_to_date(row[0])
        self.__realtime_usage_dict['time'] = row[0]
        self.__realtime_usage_dict['node'] = row[1]
        self.__realtime_usage_dict['cpu'] = row[2]
        self.__realtime_usage_dict['memory'] = row[3]
        self.__realtime_usage_dict['sessionnum'] = row[4]
        self.__realtime_usage_dict['onlinenum'] = row[5]
        self.__realtime_usage_dict['pid'] = row[6]
        self.__realtime_usage_dict['templateRequest'] = row[7]
        self.__realtime_usage_dict['httpRequest'] = row[8]
        self.__realtime_usage_dict['sessionRequest'] = row[9]
        if len(row) > 11:
            self.__realtime_usage_dict['fineIO'] = row[10]
            self.__realtime_usage_dict['NIO'] = row[11]
            self.__realtime_usage_dict['bufferMemUse'] = row[12]
            self.__realtime_usage_dict['physicalMemUse'] = row[13]
            self.__realtime_usage_dict['physicalMemFree'] = row[14]
            self.__physical_mem_free = self.__realtime_usage_dict['physicalMemFree']
        self.__node = self.__realtime_usage_dict['node']
        self.__timestamps = self.__realtime_usage_dict['time']
        self.__pid = self.__realtime_usage_dict['pid']

    def to_print_realtime_usage_log(self):
        return self.__realtime_usage_dict

    def get_timestamps(self):
        return self.__timestamps

    def get_node(self):
        return self.__node

    def get_pid(self):
        return self.__pid

    def get_physical_mem_free(self):
        return self.__physical_mem_free
