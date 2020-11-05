class BaseFocuspointInfoMessage:
    # 中止和释放记录的基类

    # id 限制4002 释放4003 中止4004 启停5002
    __id = ' '
    # 时间戳
    __time = 0
    # 可读性时间
    __date = ' '
    # 节点
    __node = ' '
    __username = ' '
    __source = ' '
    # 模板名
    __text = ' '
    # 类型 模板限制的类型 释放的等级
    __title = ' '
    # 明细
    __body = {}
    # log 用于输出日志的字典
    __focuspoint_dict = {}

    def __init__(self, focus_point_info_message):
        self.__id = focus_point_info_message['id']
        self.__time = focus_point_info_message['time']
        self.__date = focus_point_info_message['date']
        self.__username = focus_point_info_message['username']
        self.__source = focus_point_info_message['source']
        self.__text = focus_point_info_message['text']
        self.__title = focus_point_info_message['title']
        self.__body = focus_point_info_message['body']
        self.__node = focus_point_info_message['node']
        self.__focuspoint_dict = focus_point_info_message

    def to_print_focuspoint_log(self):
        return self.__focuspoint_dict
