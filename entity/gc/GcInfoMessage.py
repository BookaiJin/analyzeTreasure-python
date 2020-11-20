from utils.myTime import utils


class GcInfoMessage:
    __node = '1'
    __timestamps = 0
    __gc_type = 'gc'
    __gc_cause = 'er'
    __gc_duration = 0
    __pid = '0'
    __start_time = '0'
    __gc_record_dict = {}

    # {}: [{} ({}) [PSYoungGen: {}K->{}K({}K)] {}K->{}K({}K), {} secs] [Times: real={} secs]
    # 2019-12-05T01:43:05.435+0800: 60637.045: [GC (Allocation Failure) [PSYoungGen: 1028864K->1984K(1006080K)]
    # 2712558K->1685718K(4730368K), 0.022 secs] [Times: real=0.022 secs]
    __young_result_str_temp = '{}: [{} ({}) [PSYoungGen: {}K->{}K({}K)] {}K->{}K({}K), {} secs] ' \
                              '[Times: real={} secs] [pid:{}]'

    # {}: [{} ({}) [PSYoungGen: {}K->{}K({}K)] [ParOldGen: {}K->{}K({}K)] {}K->{}K({}K),
    # [Metaspace: {}K->{}K({}K)], {} secs] [Times: real={} secs]
    # 2019-12-05T09:01:33.354+0800: 86944.964: [Full GC (System.gc()) [PSYoungGen: 96K->0K(3393536K)]
    # [ParOldGen: 341136K->341075K(3211776K)] 341232K->341075K(6605312K),
    # [Metaspace: 150304K->150304K(154008K)], 0.295 secs] [Times: real=0.295 secs]
    __full_result_str_temp = '{}: [{} ({}) [PSYoungGen: {}K->{}K({}K)] [ParOldGen: {}K->{}K({}K)] {}K->{}K({}K), ' \
                             '[Metaspace: {}K->{}K({}K)], {} secs] [Times: real={} secs] [pid:{}]'

    def __init__(self, gc_record_dict):
        self.__node = gc_record_dict.get('node')
        self.__timestamps = int(gc_record_dict.get('gcStartTime'))
        self.__gc_type = gc_record_dict.get('gcType')
        self.__gc_cause = gc_record_dict.get('gcCause')
        self.__gc_duration = int(gc_record_dict.get('duration'))
        self.__pid = gc_record_dict.get('pid')
        temp_time = utils.convert_time2date_timezone(self.__timestamps)
        self.__start_time = temp_time[:23] + temp_time[26:]
        self.__gc_record_dict = gc_record_dict

    def to_print_gc_log(self):
        result_str = ''
        if self.__gc_type == 'GC':
            result_str = self.__young_result_str_temp.format(self.__start_time, self.__gc_type,
                                                             self.__gc_cause,
                                                             self.__gc_record_dict.get('youngBeforeUsed'),
                                                             self.__gc_record_dict.get('youngAfterUsed'),
                                                             self.__gc_record_dict.get('youngAfterCommitted'),
                                                             self.__gc_record_dict.get('heapBeforeUsed'),
                                                             self.__gc_record_dict.get('heapAfterUsed'),
                                                             self.__gc_record_dict.get('heapAfterCommitted'),
                                                             int(self.__gc_duration) / 1000,
                                                             int(self.__gc_duration) / 1000,
                                                             self.__pid)
        elif self.__gc_type == 'Full GC':
            result_str = self.__full_result_str_temp.format(self.__start_time, self.__gc_type,
                                                            self.__gc_record_dict.get('gcCause'),
                                                            self.__gc_record_dict.get('youngBeforeUsed'),
                                                            self.__gc_record_dict.get('youngAfterUsed'),
                                                            self.__gc_record_dict.get('youngAfterCommitted'),
                                                            self.__gc_record_dict.get('oldBeforeUsed'),
                                                            self.__gc_record_dict.get('oldAfterUsed'),
                                                            self.__gc_record_dict.get('oldAfterCommitted'),
                                                            self.__gc_record_dict.get('heapBeforeUsed'),
                                                            self.__gc_record_dict.get('heapAfterUsed'),
                                                            self.__gc_record_dict.get('heapAfterCommitted'),
                                                            self.__gc_record_dict.get('metaspaceBeforeUsed'),
                                                            self.__gc_record_dict.get('metaspaceAfterUsed'),
                                                            self.__gc_record_dict.get('metaspaceAfterCommitted'),
                                                            int(self.__gc_duration) / 1000,
                                                            int(self.__gc_duration) / 1000,
                                                            self.__pid)

        result = {'log': result_str, 'gcStartTime': self.__timestamps, 'node': self.__node}
        return result

    def get_node(self):
        return self.__node

    def get_pid(self):
        return self.__pid

    def get_timestamps(self):
        return self.__timestamps

    def get_gc_type(self):
        return self.__gc_type

    def get_duration(self):
        return self.__gc_duration
