from entity.focuspoint.BaseFocuspointInfoMessage import BaseFocuspointInfoMessage


class LimitInfoMessage(BaseFocuspointInfoMessage):
    # 模板限制 FR-F4002

    def __init__(self, focus_point_info_message):
        super().__init__(focus_point_info_message)
