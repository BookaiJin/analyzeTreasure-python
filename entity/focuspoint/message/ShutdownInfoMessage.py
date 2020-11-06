from entity.focuspoint.message.BaseFocuspointInfoMessage import BaseFocuspointInfoMessage


class ShutdownInfoMessage(BaseFocuspointInfoMessage):
    # 服务器启停信息 FR-F5002

    # 启动时间 deprecated
    __up_time = 0
    # 虚拟机启动的时间 deprecated
    __start_time = 0
    # 启动信号量
    __signal_name = ''
    # 系统可用时间
    __available_time = 0
    # 项目部署时间
    __app_start_time = 0
    # 虚拟机启动时间
    __jvm_start_time = 0
    # 本次进程启动的用户目录
    __user_dir = ''

    def __init__(self, focuspoint_info_message):
        super().__init__(focuspoint_info_message)
