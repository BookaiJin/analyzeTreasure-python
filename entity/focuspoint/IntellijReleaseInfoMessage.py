from entity.focuspoint.BaseIntellijInfoMessage import BaseIntellijInfoMessage


class IntellijReleaseInfoMessage(BaseIntellijInfoMessage):
    # 智能释放 FR-F4003

    def __init__(self, focus_point_info_message):
        super().__init__(focus_point_info_message)
