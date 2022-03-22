import os

class Column:
    def __init__(self, column_name):
        self.column_name = column_name
        self.column_function = ""
        self.column_alias = ""

    def print_column_info(self):
        print("\t" + self.column_name)
        if self.column_function != "":
            print("\t\t" + self.column_function)
        if self.column_alias != "":
            print("\t\talias: " + self.column_alias)

    def write_column_info(self, out_file):
        out_file.write("\t" + self.column_name + "\n")
        if self.column_function != "":
            out_file.write("\t\t" + self.column_function + "\n")
        if self.column_alias != "":
            out_file.write("\t\talias: " + self.column_alias + "\n")

    def set_column_function(self, function_name):
        self.column_function = function_name

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
    
    def write_table_info(self, out_file):
        out_file.write("\t" + self.table_name + "\n")
        if self.table_alias != "":
            out_file.write("\t\talias: " + self.table_alias + "\n")
        if self.schema != "":
            out_file.write("\t\tschema: " + self.schema + "\n")

class Filter:
    def __init__(self, column_name, operator):
        self.column_name = column_name
        self.operator = operator
        self.value = []

    def add_value(self, value):
        self.value.append(value)

    def print_filter_info(self, tab_num):
        if self.operator == "in":
            print(("\t" * (tab_num + 1)) + "column_name: " + self.column_name)
            print(("\t" * (tab_num + 1)) + "operator: " + self.operator)
            for cur_value in self.value:
                print(("\t" * (tab_num + 1)) + "value: " + cur_value)
        else:
            print(("\t" * (tab_num + 2)) + "column_name: " + self.column_name)
            print(("\t" * (tab_num + 2)) + "operator: " + self.operator)
            for cur_value in self.value:
                print(("\t" * (tab_num + 2)) + "value: " + cur_value)

    def write_filter_info(self, tab_num, out_file):
        if self.operator == "in":
            out_file.write(("\t" * (tab_num + 1)) + "column_name: " + self.column_name + "\n")
            out_file.write(("\t" * (tab_num + 1)) + "operator: " + self.operator + "\n")
            for cur_value in self.value:
                out_file.write(("\t" * (tab_num + 1)) + "value: " + cur_value + "\n")
        else:
            out_file.write(("\t" * (tab_num + 2)) + "column_name: " + self.column_name + "\n")
            out_file.write(("\t" * (tab_num + 2)) + "operator: " + self.operator + "\n")
            for cur_value in self.value:
                out_file.write(("\t" * (tab_num + 2)) + "value: " + cur_value + "\n")

class Filter_block:
    def __init__(self):
        self.operator = ""
        self.filter_list = []

    def set_operator(self, operator):
        self.operator = operator

    def add_filter(self, filter_obj):
        self.filter_list.append(filter_obj)
        
    def print_filter_block_info(self, tab_num):
        print(("\t" * tab_num) + self.operator)
        filter_count = 1
        for cur_filter in self.filter_list:
            if type(cur_filter) == Filter:
                if cur_filter.operator != "in":
                    print(("\t" * (tab_num + 1)) + "filter" + str(filter_count) + ":")
                cur_filter.print_filter_info(tab_num)
                filter_count += 1
            elif type(cur_filter) == Filter_block:
                cur_filter.print_filter_block_info(2)

    def write_filter_block_info(self, tab_num, out_file):
        out_file.write(("\t" * tab_num) + self.operator + "\n")
        filter_count = 1
        for cur_filter in self.filter_list:
            if type(cur_filter) == Filter:
                if cur_filter.operator != "in":
                    out_file.write(("\t" * (tab_num + 1)) + "filter" + str(filter_count) + ":" + "\n")
                cur_filter.write_filter_info(tab_num, out_file)
                filter_count += 1
            elif type(cur_filter) == Filter_block:
                cur_filter.write_filter_block_info(2, out_file)

class Statement:
    def __init__(self, table_obj_list, column_obj_list):
        self.Table_obj_list = table_obj_list
        self.Column_obj_list = column_obj_list
        self.Filter_block_obj = None

    def set_Filter_obj(self, filter_list):
        self.Filter_block_obj = filter_list

    def print_block_info(self):
        print("Projection: ")
        for cur_column_obj in self.Column_obj_list:
            cur_column_obj.print_column_info()

        print("\nTables: ")
        for cur_table_obj in self.Table_obj_list:
            cur_table_obj.print_table_info()

        if self.Filter_block_obj != None:
            print("\nFilter: ")
            self.Filter_block_obj.print_filter_block_info(1) 
        else:
            print("\nFilter: N/A")

        print("================")

    def write_block_info(self, out_file):
        out_file.write("Projection: " + "\n")
        for cur_column_obj in self.Column_obj_list:
            cur_column_obj.write_column_info(out_file)

        out_file.write("\nTables: " + "\n")
        for cur_table_obj in self.Table_obj_list:
            cur_table_obj.write_table_info(out_file)

        if self.Filter_block_obj != None:
            out_file.write("\nFilter: " + "\n")
            self.Filter_block_obj.write_filter_block_info(1, out_file) 
        else:
            out_file.write("\nFilter: N/A" + "\n")

        out_file.write("================" + "\n")
 
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
    line_section = line[7: line.lower().find(" from ")].strip()
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
    column_obj_list = []
    for cur_column in column_name_list:
        column_name = find_column_name(cur_column, table_alias_list)
        column_obj = Column(column_name)

        alias = find_column_alias(cur_column)
        if alias != "":
            column_obj.set_column_alias(alias)

        function = find_column_function(cur_column)
        if function != "":
            column_obj.set_column_function(function)

        column_obj_list.append(column_obj)

    return column_obj_list

def find_column_name( column_str, table_alias_list ):
    if "(" in column_str:
        column_name = column_str[column_str.find("(") + 1: column_str.find(", ")]
    elif " " in column_str:
        column_name = column_str[:column_str.find(" ")]
    else:
        column_name = column_str

    column_alias_str = column_name[:column_name.find(".")]

    if column_alias_str in table_alias_list.keys():
        column_name = table_alias_list[column_alias_str] + column_name[column_name.find("."):]

    return column_name

def find_column_alias( column_str ):
    if ") \"" in column_str:
        alias = column_str[column_str.find(") \"") + 3 : -1]
    elif " " in column_str:
        alias = column_str[column_str.find(" ") + 2: -1]
    else:
        alias = ""

    return alias

def find_column_function( column_str ):
    if "(" in column_str:
        function_name = column_str[:column_str.find("(")]
        format = column_str[column_str.find(", ") + 2 :column_str.find(")")]
        function = function_name + "(format: " + format + ")"
    else:
        function = ""

    return function

def get_table_objects( line ):
    line_section = line[line.lower().find(" from ") + 6:] if "where" not in line.lower() else line[line.lower().find(" from ") + 6: line.lower().find(" where")]
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

def get_filter_block_objects( line, table_alias_list ):
    if "where" in line.lower():
        filter_str = line[line.lower().find("where") + 5: -1].strip()
        filter_block_obj = create_filter_block_objects(filter_str, table_alias_list)
    else:
        filter_block_obj = None
    
    return filter_block_obj

def create_filter_block_objects( filter_str, table_alias_list ):
    operator = find_operator(filter_str)
    filter_block_obj = Filter_block()
    if operator == []:
        add_filter_obj_to_block(filter_str, filter_block_obj, table_alias_list)
    else:
        filter_block_obj.set_operator(operator[0])
        if operator[0] == "in":
            add_filter_obj_to_block(filter_str, filter_block_obj, table_alias_list)
        else:
            filter_str_list = [filter_str[:filter_str.find(operator[0]) - 1], filter_str[filter_str.find(" ", filter_str.find(operator[0])) + 1:]]
            
            for i in range(2):
                filter_clause = filter_str_list[i]
                clause_operator = find_operator(filter_clause)
                if clause_operator == []:
                    add_filter_obj_to_block(filter_clause, filter_block_obj, table_alias_list)
                else:
                    filter_obj = create_filter_block_objects(filter_clause, table_alias_list)
                    filter_block_obj.add_filter(filter_obj)

    return filter_block_obj

def add_filter_obj_to_block( cur_filter_str, filter_block_obj, table_alias_list ):
    filter_obj = get_filter_object(cur_filter_str, table_alias_list)
    filter_block_obj.add_filter(filter_obj)

def get_filter_object( filter_str, table_alias_list ): # Assuming spaces around operator such as "x = y"
    column_name = filter_str[:filter_str.find(" ")].replace("(", "").replace(")", "")
    if column_name in table_alias_list.keys():
        column_name = table_alias_list[column_name]
    operator = filter_str[filter_str.find(" ") + 1:filter_str.find(" ", filter_str.find(" ") + 1)]
    filter_obj = Filter(column_name, operator)
    if operator.lower() == "in":
        tmp_filter_str = filter_str.replace("(", "").replace(")", "")
        value_list = tmp_filter_str[tmp_filter_str.find("in") + 3:].split(", ")
        for cur_value in value_list:
            filter_obj.add_value(cur_value)
    else:
        filter_obj.add_value(filter_str[filter_str.find(" ", filter_str.find(" ") + 1):].replace("(", "").replace(")", ""))

    return filter_obj

def find_operator( filter_str ):
    operator_possibilities = ["and", "or", "in"]
    if " and " not in filter_str.lower():
        operator_possibilities.remove("and")
    if " or " not in filter_str.lower():
        operator_possibilities.remove("or")
    if " in " not in filter_str.lower():
        operator_possibilities.remove("in")

    if len(operator_possibilities) > 1:
        edited_filter_str = str(filter_str)
        while len(operator_possibilities) > 1:
            parenthesis_str = find_parenthesis_section(edited_filter_str)
            for operator in operator_possibilities:
                if operator in parenthesis_str:
                    operator_possibilities.remove(operator)
            edited_filter_str = edited_filter_str.replace(parenthesis_str, "")
       
    return operator_possibilities     

def find_parenthesis_section( filter_str ): # Used if multiple operators in filter
    parenthesis_str = filter_str[filter_str.find("("):filter_str.find(")") + 1]
    if parenthesis_str.count("(") != parenthesis_str.count(")"):
        parenthesis_str = filter_str[filter_str.find("("):filter_str.find(")", filter_str.find(")") + 1) + 1]

    return parenthesis_str

def create_statement( line ):
    table_obj_list, table_alias_list = get_table_objects(line)
    column_name_list = get_column_names(line)
    column_obj_list = get_column_objects(column_name_list, table_alias_list)
    filter_obj = get_filter_block_objects(line, table_alias_list)
    cur_statement = Statement(table_obj_list, column_obj_list)

    if filter_obj != None:
        cur_statement.set_Filter_obj(filter_obj)

    return cur_statement

def print_output_to_screen( blocked_data_list ):
    for cur_line in blocked_data_list:
        statement = create_statement(cur_line)
        statement.print_block_info()

def write_output_to_file( blocked_data_list ):
    write_flag = input("Write output to file? Y/N: ").lower()

    while write_flag != "y" and write_flag!= "n":
        write_flag = input("Write output to file? Y/N: ").lower()

    if write_flag == "n":
        exit()
    else:
        output_file_name = "./output_files/" + input("Output file name: ")
        #output_file_name = input("Output file name: ")

        if not os.path.exists("./output_files/"):
            os.makedirs("./output_files/")

        out_file = open(output_file_name, "w+")
        for cur_line in blocked_data_list:
            statement = create_statement(cur_line)
            statement.write_block_info(out_file)

if __name__ == "__main__":
    input_sql_file_name = "./input_files/sql_input1.sql"
    blocked_data_list = get_sql_input(input_sql_file_name)
    print_output_to_screen(blocked_data_list)
    write_output_to_file(blocked_data_list)