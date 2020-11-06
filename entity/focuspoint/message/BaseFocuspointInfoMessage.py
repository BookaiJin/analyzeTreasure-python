class BaseFocuspointInfoMessage:
    # 中止和释放记录的基类 埋点数据不区分pid入库

    # id 限制4002 释放4003 中止4004 启停5002
    _id = ' '
    # 时间戳
    _time = 0
    # 可读性时间
    _date = ' '
    # 节点
    _node = ' '
    _username = ' '
    _source = ' '
    # 模板名
    _text = ' '
    # 类型 模板限制的类型 释放的等级
    _title = ' '
    # 明细
    _body = {}
    # log 用于输出日志的字典
    _focuspoint_dict = {}

    def __init__(self, focuspoint_info_message):
        self._id = focuspoint_info_message['id']
        self._time = int(focuspoint_info_message['time'])
        self._date = focuspoint_info_message['date']
        self._username = focuspoint_info_message['username']
        self._source = focuspoint_info_message['source']
        self._text = focuspoint_info_message['text']
        self._title = focuspoint_info_message['title']
        self._body = focuspoint_info_message['body']
        self._node = focuspoint_info_message['node']
        self._focuspoint_dict = focuspoint_info_message

    def to_print_focuspoint_log(self):
        return self._focuspoint_dict

    def get_time(self):
        return self._time

    def get_node(self):
        return self._node
