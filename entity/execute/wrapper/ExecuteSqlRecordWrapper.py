class ExecuteSqlRecordWrapper:

    __execute_sql_id_list_detail = {}
    __execute_sql_sql_span_list_detail = {}

    def __init__(self, execute_sql_id_list_detail, execute_sql_sql_span_list_detail):
        self.__execute_sql_id_list_detail = execute_sql_id_list_detail
        self.__execute_sql_sql_span_list_detail = execute_sql_sql_span_list_detail
