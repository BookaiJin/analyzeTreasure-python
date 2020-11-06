class DownInfoBean:
    # 宕机开始时间，开始不可用时间戳
    __down_start_time = 0
    # 宕机结束时间，开始使用时时间戳
    __down_end_time = 0
    # 宕机持续时间 ms
    __duration = 0
    # 宕机类别
    __down_type = ''
    # 宕机时刻pid
    __down_pid = ''
    # 重启pid
    __restart_pid = ''
    # 宕机前用户目录
    __user_dir = ''

    def __init__(self, down_gc_list, restart_gc_list, down_realtime_list, down_shutdown_info_message, restart_shutdown_info_message):
        # 宕机前工作目录
        if down_shutdown_info_message is not None:
            self.__user_dir = down_shutdown_info_message.get_user_dir()

        # 宕机重启可用时间
        if restart_shutdown_info_message is not None:
            self.__down_end_time = restart_shutdown_info_message.get_available_time()
        else:
            self.__down_end_time = int(restart_gc_list[0].get_timestamps())

        self.__down_start_time = int(down_gc_list[-1].get_timestamps())
        self.__down_pid = down_gc_list[0].get_pid()
        self.__restart_pid = restart_gc_list[0].get_pid()
        self.__duration = self.__down_end_time - self.__down_start_time

    def get_duration(self):
        return self.__duration

    def get_down_type(self):
        return self.__down_type

    def get_down_pid(self):
        return self.__down_pid

    def get_restart_pid(self):
        return self.__restart_pid

    def get_user_dir(self):
        return self.__user_dir
