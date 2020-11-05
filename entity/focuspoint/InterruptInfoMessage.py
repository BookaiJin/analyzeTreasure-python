from entity.focuspoint.BaseFocuspointInfoMessage import BaseFocuspointInfoMessage


class InterruptInfoMessage(BaseFocuspointInfoMessage):
    # 中止机制 FR-F4004

    def __init__(self, focus_point_info_message):
        super().__init__(focus_point_info_message)
