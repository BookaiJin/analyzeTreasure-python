from entity.focuspoint.message.BaseFocuspointInfoMessage import BaseFocuspointInfoMessage


class IntellijReleaseInfoMessage(BaseFocuspointInfoMessage):
    # 智能释放 FR-F4003

    def __init__(self, focuspoint_info_message):
        super().__init__(focuspoint_info_message)
