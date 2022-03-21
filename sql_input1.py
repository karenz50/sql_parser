class Column:
    def __init__(self, column_name):
        self.column_name = column_name
        self.column_function = ""
        self.column_alias = ""

    def print_column_info(self):
        print("\t" + self.column_name)
        if self.function != "":
            print("\t\t" + self.function)
        if self.column_alias != "":
            print("\t\talias: " + self.column_alias)

    def set_function(self, function_name):
        self.function = function_name

    def set_column_alias(self, alias):
        self.column_alias = alias

class Table:
    def __init__(self, table_name, alias, schema):
        self.table_name = table_name
        self.table_alias = alias
        self.schema = schema

    def print_table_info(self):
        print("\t" + self.table_name)
        if self.table_alias != "":
            print("\t\talias: " + self.table_alias)
        if self.schema != "":
            print("\t\tschema: " + self.schema)

class Filter:
    def __init__(self, column_name, operator, value):
        self.column_name = column_name
        self.operator = operator
        self.value = value

    def print_filter_info(self):
        print("\t\t\tcolumn_name: " + self.column_name)
        print("\t\t\toperator: " + self.operator)
        print("\t\t\tvalue: " + self.value)

class Filter_block():
    def __init__(self, operator):
        operator = ""
        filter_list = []

    def set_filter_list(self, filter_list):
        self.filter_list = filter_list
        
    def print_filter_block_info(self):
        print("\t" + self.operator)
        for i in range(len(self.filter_list)):
            print("\t\tfilter" + str(i + 1) + ":")
            self.filter_list[i].print_filter_info()

class Statement:
    def __init__(self, table_obj_list, column_obj_list):
        self.Table_obj_list = table_obj_list
        self.Column_obj_list = column_obj_list
        self.Filter_block_obj_list = []

    def set_Filter_list(self, filter_list):
        self.Filter_block_obj_list = filter_list

    def print_block_info(self):
        def print_divider_line(): print("================")
        print_divider_line()

        print("Projection: ")
        for cur_column_obj in self.Column_obj_list:
            cur_column_obj.print_column_info()

        print("\nTables: ")
        for cur_table_obj in self.Table_obj_list:
            cur_table_obj.print_table_info()

        if len(Filter_block_obj_list) != 0:
            print("\nFilter: ")
            for cur_filter_obj in self.Filter_block_obj_list:
                cur_filter_obj.print_filter_block_info() 
        else:
            print("\nFilter: N/A")

        print_divider_line()
 
def get_sql_input( file_name ):
    in_file = open(file_name, "r")
    sql_data_list = in_file.readlines()
    cur_data_block, blocked_sql_data_list = [], []

    for cur_line in sql_data_list:
        cur_data_block.append(cur_line.strip().replace("\n", ""))
        if ";" in cur_line: # Assuming last block ends with ";"
            blocked_sql_data_list.append(" ".join(cur_data_block))
            cur_data_block = []

    return blocked_sql_data_list

def get_column_names( line ):
    line_section = line[7: line.find(" FROM ")].strip()
    column_names = []
    while len(line_section) > 0:
        comma_index = line_section.find(", ") if ", " in line_section else len(line_section)
        parenthesis_index = line_section.find("(") if "(" in line_section else len(line_section)

        if comma_index < parenthesis_index:
            append_str = line_section[:comma_index]
            line_section = line_section[comma_index + 1:].strip()

        elif parenthesis_index < comma_index:
            tmp_index = line_section.find(")")
            comma_index = line_section[tmp_index:].find(", ") if ", " in line_section[tmp_index:] else len(line_section)
            append_str = line_section[:tmp_index + comma_index]
            line_section = line_section[tmp_index + comma_index + 1:].strip()

        elif comma_index == len(line_section) and parenthesis_index == len(line_section):
            append_str = line_section
            line_section = ""

        column_names.append(append_str)

    return column_names

def get_column_objects( column_name_list, table_alias_list ):
    pass

def get_table_objects( line ):
    line_section = line[line.find(" FROM ") + 6:] if "WHERE" not in line else line[line.find(" FROM ") + 6: line.find(" WHERE")]
    table_list = line_section.split(", ")
    table_obj_list, table_alias_list = [], {}

    for cur_table in table_list:
        schema, table_name, alias = seperate_into_table_info(cur_table)
        cur_table_obj = Table(table_name, alias, schema)
        table_obj_list.append(cur_table_obj)

        if alias not in table_alias_list.keys():
            table_alias_list[alias] = table_name

    return table_obj_list, table_alias_list

def seperate_into_table_info( table_str ): # Used in get_table_objects()
    schema, table_name, alias = "", "", ""
    if "." in table_str:
        schema = table_str[:table_str.find(".")]
        table_str = table_str[table_str.find(".") + 1:]
    if " " in table_str:
        tmp_data_list = table_str.split(" ")
        table_name, alias = tmp_data_list[0], tmp_data_list[1]
    else:
        table_name = table_str

    return schema, table_name, alias

def get_filter_objects( line ):
    pass

def create_statement( line ):
    table_obj_list, table_alias_list = get_table_objects(line)
    column_name_list = get_column_names(line)
    column_obj_list = get_column_objects(column_name_list, table_alias_list)
    filter_obj_list = get_filter_objects(line)
    cur_statement = Statement(table_obj_list, column_obj_list)

    if filter_obj_list != []:
        cur_statement.set_Filter_list(filter_obj_list)

    return cur_statement

def print_output_to_screen( blocked_data_list ):
    for cur_line in blocked_data_list:
        statement = create_statement(cur_line)
        statement.print_block_info()

if __name__ == "__main__":
    input_sql_file_name = "sql_input.sql"
    blocked_data_list = get_sql_input(input_sql_file_name)
