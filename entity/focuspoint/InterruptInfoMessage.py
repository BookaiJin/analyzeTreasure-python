from entity.focuspoint.BaseIntellijInfoMessage import BaseIntellijInfoMessage


class InterruptInfoMessage(BaseIntellijInfoMessage):
    # 中止机制 FR-F4004

    def __init__(self, focus_point_info_message):
        super().__init__(focus_point_info_message)
