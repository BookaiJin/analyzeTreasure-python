from entity.focuspoint.message.BaseFocuspointInfoMessage import BaseFocuspointInfoMessage


class LimitInfoMessage(BaseFocuspointInfoMessage):
    # 模板限制 FR-F4002

    # 限制的场景
    __reason = ''
    # 限制的格子数
    __cell_num = 0
    # 负载
    __load = ''
    # sessionID
    __session_id = ''
    # 中止的场景
    __detail = ''

    def __init__(self, focuspoint_info_message):
        super().__init__(focuspoint_info_message)
