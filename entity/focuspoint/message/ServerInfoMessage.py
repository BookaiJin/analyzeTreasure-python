from entity.focuspoint.message.BaseFocuspointInfoMessage import BaseFocuspointInfoMessage


class ServerInfoMessage(BaseFocuspointInfoMessage):
    # 服务器容器信息

    # CPU核数
    __cpu = 0

    def __init__(self, focuspoint_info_message):
        super().__init__(focuspoint_info_message)
        self.__cpu = self._body['cpu']
