from entity.focuspoint.message.BaseFocuspointInfoMessage import BaseFocuspointInfoMessage


class ShutdownInfoMessage(BaseFocuspointInfoMessage):
    # 服务器启停信息 FR-F5002

    # pid
    __pid = ''
    # 系统可用时间
    __available_time = 0
    # 项目部署时间
    __app_start_time = 0
    # 虚拟机启动时间
    __jvm_start_time = 0
    # 本次进程启动的用户目录
    __user_dir = ''
    # 启动信号量
    __signal_name = ''
    # 启动时间 deprecated
    __up_time = 0
    # 虚拟机启动的时间 deprecated
    __start_time = 0

    def __init__(self, focuspoint_info_message):
        super().__init__(focuspoint_info_message)
        self.__pid = self._body['pid']
        self.__available_time = int(self._body['availableTime'])
        self.__app_start_time = int(self._body['appStartTime'])
        self.__jvm_start_time = int(self._body['jvmStartTime'])
        self.__user_dir = self._body['userDir']
        self.__signal_name = self._body['signalName']
        self.__up_time = int(self._body['upTime'])
        self.__start_time = int(self._body['startTime'])

    def get_pid(self):
        return self.__pid

    def get_available_time(self):
        return self.__available_time

    def get_user_dir(self):
        return self.__user_dir

    def get_signal_name(self):
        return self.__signal_name
