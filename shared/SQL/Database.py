import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Print')))

from typing import List
import Format
import subprocess
import csv

class Database:

    statements: List[str] = []
    csv_files: List[str] = []
    
    def __init__(self, execute_string: str, start_statements: List[str], end_statements: List[str]):
        '''
        Creates a new instance.

        :param execute_string: This string resprents the complete execution command of that particular
                               SQL-Database (console).
        :param start_statements: A list of SQL statements that needs to be executed at the beginning of
                                 all statements.
        :param end_statements: A list of SQL statements that needs to be executed at the end of
                               all statements. 
        '''

        self.exe = execute_string.split()
        self.statements = start_statements
        self.end = end_statements

    def create_table(self, table_name: str, columns: List[str], types: List[str]) -> None:
        '''
        This method adds a create statement to the list.

        :param table_name: The name of the table which should be created.
        :param columns: A list of column names of the table.
        :param types: A list of types for each column.
        '''
        
        statement = f'CREATE TABLE {table_name}('
        for idx in range(len(columns)):
            statement += f'{columns[idx]} {types[idx]}'
            if idx != len(columns) - 1:
                statement += ','
            else:
                statement += ')'
        statement += ';\n'
        self.statements.append(statement)

    def insert_from_csv(self, table_name: str, csv_file: str, header: List[str], data: List[List[str]]) -> None:
        '''
        This method adds a copy statement to the list in which a table gets all entries
        from a CSV file. Therefore the CSV file will be generated as well.

        :param table_name: The name of the table.
        :param csv_file: The name of the CSV file.
        :param header: A list of header data of the csv file.
        :param data: A list of rows which should be stored in the CSV file.
        '''

        statement = f"COPY {table_name} FROM '{csv_file}' delimiter ',' HEADER;\n"
        self.statements.append(statement)

        if len(header) != 0 and len(data) != 0:
            with open(csv_file, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(data)
            self.csv_files.append(csv_file)

    def insert_from_select(self, table_name: str, select_stmt: str) -> None:
        '''
        This method adds the specified select statement into an insert statement
        to fill the given table with the resulting entries.

        :param table_name: The name of the table where the data should be inserted.
        :param select_stmt: The select statement which generates the resulting data.
        '''

        statement = f'INSERT INTO {table_name} ({select_stmt});\n'
        self.statements.append(statement)

    def execute_sql(self) -> None:
        '''
        This function executes a list of SQL statements for preparation.
        '''

        self.statements = self.statements + self.end
        database = subprocess.Popen(
            self.exe, 
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for statement in self.statements:
            database.stdin.write(statement)
            database.stdin.flush()
        _, error = database.communicate()
        if error:
            print(error)

        for file in self.csv_files:
            try:
                os.remove(file)
            except Exception:
                Format.print_warning(f'The file {file} could not be removed')
                continue
    