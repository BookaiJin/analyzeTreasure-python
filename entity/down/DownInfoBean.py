class DownInfoBean:
    # 宕机开始时间，开始不可用时间戳
    __down_start_time = 0
    # 宕机结束时间，开始使用时时间戳
    __down_end_time = 0
    # 宕机持续时间 ms
    __duration = 0
    # 宕机类别
    __down_type = ''

    def __init__(self, down_start_gc_list, down_end_gc_list):
        self.__down_start_time = int(down_start_gc_list[-1].get_timestamps())
        self.__down_end_time = int(down_end_gc_list[0].get_timestamps())
        self.__duration = self.__down_end_time - self.__down_start_time

    def get_duration(self):
        return self.__duration

    def get_down_type(self):
        return self.__down_type
