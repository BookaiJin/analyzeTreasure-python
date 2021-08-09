class FocuspointWrapper:
    __limit_info_message_node_list_detail = {}

    __release_info_message_node_list_detail = {}

    __interrupt_info_message_node_list_detail = {}

    __shutdown_info_message_node_pid_item = {}

    load_group_message = None

    def __init__(self, limit_info_message_node_list_detail, release_info_message_node_list_detail,
                 interrupt_info_message_node_list_detail, shutdown_info_message_node_pid_item, load_group_message):
        self.__limit_info_message_node_list_detail = limit_info_message_node_list_detail
        self.__release_info_message_node_list_detail = release_info_message_node_list_detail
        self.__interrupt_info_message_node_list_detail = interrupt_info_message_node_list_detail
        self.__shutdown_info_message_node_pid_item = shutdown_info_message_node_pid_item
        self.load_group_message = load_group_message

    def get_limit_message_list(self):
        return self.__limit_info_message_node_list_detail

    def get_release_message_list(self):
        return self.__release_info_message_node_list_detail

    def get_interrupt_message_list(self):
        return self.__interrupt_info_message_node_list_detail

    def get_shutdown_message_item(self, node, pid):
        if node in self.__shutdown_info_message_node_pid_item:
            if pid in self.__shutdown_info_message_node_pid_item[node]:
                return self.__shutdown_info_message_node_pid_item[node][pid]
        return None
