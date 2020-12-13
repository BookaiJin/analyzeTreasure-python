class ExecuteTemplateRecord:
    # <id, tname, [sql1, sql2, ...]>
    # executeId
    __execute_id = ''
    # template name absolute path
    __template_name = ''
    # display name
    __display_name = ''
    # consume
    __consume = 0
    # complete
    __complete = 0
    # mem
    __memory = 0
    # sql time
    __sql_time = 0
    # time
    __timestamp = 0
    # start time = timestamp - consume
    __start_time = 0

    def __init__(self, row):
        self.__execute_id = row[0]
        self.__template_name = row[1]
        self.__display_name = row[2]
        self.__timestamp = int(row[3])
        self.__memory = int(row[4])
        self.__consume = int(row[6])
        self.__sql_time = int(row[7])
        self.__complete = int(row[11])
        self.__start_time = self.__timestamp - self.__consume

    def get_start_time(self):
        return self.__start_time
