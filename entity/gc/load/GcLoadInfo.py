class GcLoadInfo:
    gc_type = ''
    young_release = 0
    young_promote = 0
    young_rate = 0.0
    old_use_rate = 0.0
    heap_use_rate = 0.0
    old_release = 0

    def __init__(self, load_dict):
        self.gc_type = load_dict['gcType']
        self.young_release = load_dict['young_release']
        self.young_promote = load_dict['young_promote']
        self.young_rate = load_dict['young_use_rate']
        self.old_use_rate = load_dict['old_use_rate']
        self.heap_use_rate = load_dict['heap_use_rate']
        self.old_release = load_dict['old_release']

    def to_load_log(self):
        return self.gc_type + ', ' + str(self.young_release) + ', ' + str(self.young_promote) + ', ' + str(self.young_rate) + ', ' + str(
            self.old_use_rate) + ', ' + str(self.heap_use_rate) + ', ' + str(self.old_release)
