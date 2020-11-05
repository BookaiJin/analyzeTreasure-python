class BaseIntellijInfoMessage:
    # 中止和释放记录的基类

    # id 限制4002 释放4003 中止4004 启动5002
    __id = ' '
    # 时间戳
    __time = 0
    # 可读性时间
    __date = ' '
    # 几点
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
        pass
