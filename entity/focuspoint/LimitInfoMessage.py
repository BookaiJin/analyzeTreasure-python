from entity.focuspoint.BaseIntellijInfoMessage import BaseIntellijInfoMessage


class LimitInfoMessage(BaseIntellijInfoMessage):
    # 模板限制 FR-F4002

    def __init__(self, focus_point_info_message):
        super().__init__(focus_point_info_message)
