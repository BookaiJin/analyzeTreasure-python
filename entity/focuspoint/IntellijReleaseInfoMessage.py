from entity.focuspoint.BaseFocuspointInfoMessage import BaseFocuspointInfoMessage


class IntellijReleaseInfoMessage(BaseFocuspointInfoMessage):
    # 智能释放 FR-F4003

    def __init__(self, focus_point_info_message):
        super().__init__(focus_point_info_message)
