class ExecuteSqlRecord:
    # executeId
    __execute_id = ''
    # data source name
    __ds_name = ''
    # row count
    __rows = 0
    # column count
    __columns = 0
    # connection name
    __connection = ''
    # sql time
    __sql_time = 0
    # time
    __timestamp = 0

    def __init__(self, row):
        self.__timestamp = int(row[0])
        self.__execute_id = row[1]
        self.__ds_name = row[2]
        self.__sql_time = int(row[3])
        self.__rows = int(row[4])
        self.__columns = int(row[5])
        self.__connection = row[6]

    def get_timestamp(self):
        return self.__timestamp

    def get_sql_time(self):
        return self.__sql_time
