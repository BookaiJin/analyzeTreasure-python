from entity.focuspoint.BaseFocuspointInfoMessage import BaseFocuspointInfoMessage


class ShutdownInfoMessage(BaseFocuspointInfoMessage):

    def __init__(self, focus_point_info_message):
        super().__init__(focus_point_info_message)
