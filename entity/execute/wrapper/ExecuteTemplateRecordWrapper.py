class ExecuteTemplateRecordWrapper:

    __execute_template_id_list_detail = {}
    __execute_template_sql_span_list_detail = {}

    def __init__(self, execute_template_id_list_detail, execute_template_sql_span_list_detail):
        self.__execute_template_id_list_detail = execute_template_id_list_detail
        self.__execute_template_sql_span_list_detail = execute_template_sql_span_list_detail
