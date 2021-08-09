class LoadGroupMessage:
    # 按照负载区分释放、中止和限制记录

    """
    {
        {high:
            {
                time:4

            }
        }
        {}
        {}
    }
    """
    load_times_detail = {}

    limit_detail = []

    release_detail = []

    interrupt_detail = []

    def __init__(self):
        super(LoadGroupMessage, self).__init__()

    def add_limit_detail(self, limit_detail):
        self.limit_detail.append(limit_detail)

    def add_release_detail(self, release_detail):
        self.release_detail.append(release_detail)

    def add_interrupt_detail(self, interrupt_detail):
        self.interrupt_detail.append(interrupt_detail)
