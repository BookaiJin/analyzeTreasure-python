from entity.focuspoint.message.BaseFocuspointInfoMessage import BaseFocuspointInfoMessage


class InterruptInfoMessage(BaseFocuspointInfoMessage):
    # 中止机制 FR-F4004

    def __init__(self, focuspoint_info_message):
        super().__init__(focuspoint_info_message)
