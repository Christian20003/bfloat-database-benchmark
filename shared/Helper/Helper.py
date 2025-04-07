import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Types')))

from typing import List
from Format import print_error, print_warning
import subprocess
import csv

def execute_sql(statements: List[str], exe: str, dir: str) -> str:
    '''
    This function executes a list of SQL statements (without benchmarking).

    :param statements: A list of SQL statements (Every element should end with ";\n").
    :param exe: The path to the executable of the database.
    :param dir: The path to the directory where the data should be stored.

    :returns: The output of the executions

    :raise RuntimeError: If the database process failed.
    '''

    database = subprocess.Popen(
        [exe, dir], 
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    for statement in statements:
        database.stdin.write(statement)
        database.stdin.flush()
    output, error = database.communicate()
    if error:
        print_error('Something went wrong by creating the table', error)
    return output

def remove_files(files: List[str], dir: str) -> None:
    '''
    This function deletes a list of files.

    :param files: A list of file names.
    :param dir: The directory of the files.

    :raise RuntimeError: If something went wrong during deletion. 
    '''
    for file in files:
        try:
            os.unlink(os.path.join(dir, file))
        except FileNotFoundError:
            print_warning(f'{file} does not exist. Ignore deletion')
        except Exception as e:
            print_error(f'Failed to remove {file}', e)

def generate_csv(file_name: str, header: List[str], data: List) -> None:
    '''
    This function generates a csv file for the data which should be used 
    for the SQL statement.

    :param file_name: The name of the csv file.
    :param header: All headers in the csv file.
    :param data: The data which should be added to the csv file (in correct format)
    '''
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        data.insert(0, header)
        writer.writerows(data)

def tfloat_switch(table_name_new: str, table_name_old: str, paths: dict) -> None:
    '''
    This function transfers the data into an table with tfloat type.

    :param table_name_new: The name of the table with the type tfloat.
    :param table_name_old: The name of the table with the type float.
    :paths: A dictionary with paths to all necessary executables and directories.
    '''
    statements = ['SET persist=1;\n']
    copy = f'INSERT INTO {table_name_new} SELECT * FROM {table_name_old};\n'
    statements.append(copy)
    execute_sql(statements, paths['exe'], paths['storage'])

    files = [f'{table_name_old}.arrow', f'{table_name_old}.arrow.sample', f'{table_name_old}.metadata.json']
    remove_files(files, paths['storage'])