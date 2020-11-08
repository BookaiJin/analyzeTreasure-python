from entity.gc.GcInfoMessage import GcInfoMessage
from entity.realtimeusage.RealtimeUsage import RealtimeUsage
from utils.myTime import utils


class DownInfoBean:
    # 宕机开始时间，开始不可用时间戳
    __down_start_timestamps = 0
    # 宕机结束时间，开始使用时时间戳
    __down_end_timestamps = 0
    # 宕机可读时间节点
    __down_start_time = ''
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
    # 关闭信号量
    __signal_name = ''

    def __init__(self, down_gc_list, restart_gc_list, down_realtime_list, down_shutdown_info_message, restart_shutdown_info_message):
        # 宕机前工作目录 信号量
        if down_shutdown_info_message is not None:
            # 宕机前运行的工作目录
            self.__user_dir = down_shutdown_info_message.get_user_dir()
            # 记录的关机信号量
            self.__signal_name = down_shutdown_info_message.get_signal_name()

        # 宕机重启可用时间
        if restart_shutdown_info_message is not None:
            self.__down_end_timestamps = restart_shutdown_info_message.get_available_time()
        else:
            self.__down_end_timestamps = restart_gc_list[0].get_timestamps()
            self.__down_time = utils.convert_time_to_date(self.__down_end_timestamps)

        # 宕机开始时间
        self.__down_start_timestamps = down_gc_list[-1].get_timestamps()

        # 宕机类型 xmx-oom xcpu offheap term
        if self.is_xmx_oom(down_gc_list):
            # 十分钟有三分钟 xmx-oom
            self.__down_type = "Xmx-OOM"
        elif self.is_xcpu(down_realtime_list):
            # 最后十分钟有八分钟 CPU高于
            self.__down_type = "XCPU"
        elif self.is_off_heap(down_realtime_list[-1]):
            # 信号量OOM 或者 realtime最后物理内存小于1M
            self.__down_type = "OFFHEAP"
        else:
            self.__down_type = 'TERM'

        self.__down_pid = down_gc_list[0].get_pid()
        self.__restart_pid = restart_gc_list[0].get_pid()
        self.__duration = self.__down_end_timestamps - self.__down_start_timestamps

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

    def get_signal_name(self):
        return self.__signal_name

    def get_down_start_time(self):
        return self.__down_start_time

    def is_off_heap(self, last_realtime_info_message):
        return self.__signal_name == 'OOM' or (
                0 < last_realtime_info_message.get_physical_mem_free() < 1024)

    def is_xcpu(self, down_realtime_list):
        # 最后十分钟的realtime记录点80%的CPU高于0.9即为CPU宕机
        # 最后一条realtime的时间
        down_realtime_list.sort(key=RealtimeUsage.get_timestamps, reverse=True)
        last_realtime_time = down_realtime_list[0].get_timestamps()
        total_cpu_times = 0
        high_cpu_times = 0
        for realtime_usage_info_message in down_realtime_list:
            if last_realtime_time - realtime_usage_info_message.get_timestamps() > 10 * 60 * 1000:
                break
            if realtime_usage_info_message.get_cpu() > 0.95:
                high_cpu_times += 1
            total_cpu_times += 1
        if high_cpu_times / total_cpu_times > 0.8:
            self.__down_start_timestamps = last_realtime_time
            return True
        else:
            return False

    def is_xmx_oom(self, down_gc_list):
        down_gc_list.sort(key=GcInfoMessage.get_timestamps, reverse=True)
        # 列表最后一条gc时间的时间戳
        last_gc_time = down_gc_list[0].get_timestamps()
        # 最后十分钟gc持续时长
        last_10_gc_duration = 0
        last_10_gc_times = 0
        for gc_info_message in down_gc_list:
            if last_gc_time - gc_info_message.get_timestamps() > 10 * 60 * 1000:
                break
            if gc_info_message.get_gc_type() is 'Full GC':
                last_10_gc_duration += gc_info_message.get_duration()
            last_10_gc_times += 1
        if last_10_gc_duration > 3 * 60 * 1000:
            self.__down_type = 'Xmx-OOM'
            # 判断为宕机之后，最后一条为full gc，继续往前索引，找到连续full gc的第一条
            if down_gc_list[last_10_gc_times].get_gc_type() is 'Full GC':
                down_gc_list = down_gc_list[last_10_gc_times:]
                for gc_info_message in down_gc_list:
                    if gc_info_message.get_gc_type() is 'Full GC':
                        self.__down_start_timestamps = gc_info_message.get_timestamps
                    else:
                        break
            return True
        return False
