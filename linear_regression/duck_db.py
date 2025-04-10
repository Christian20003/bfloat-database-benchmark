import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Parsing')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Types')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))

from typing import List
from Point import Point
from Helper import execute_sql, generate_csv, remove_files
from Parse_Memory import parse_memory_metrics
import datetime
import subprocess
import time

def duck_db_benchmark(points: List[Point], lr: float, file_path: str, key_name: str) -> None:
    print('PSEUDO-DUCKDB BENCHMARK')
    remove_files(['data.db'], '.')
    insert_data(points, lr, 'points', 'data.csv')
    time = time_benchmark(file_path)
    file_name = memory_benchmark(file_path, key_name)
    result = parse_memory_metrics({}, file_name)
    return time, result['memory']['total']


def insert_data(points: List[Point], lr:float , table_name: str, csv_file: str) -> None:
    '''
    This function inserts all given tensors into a table.

    :param tensor: A list of tensors which should be inserted.
    :param table_name: The name of table in which the tensors should be inserted.
    :param csv_file: The file where the data is stored.
    :param paths: A dictionary with paths to all necessary executables and directories.

    :raise RuntimeError: If the data could not be inserted.
    '''

    data = [[value.id, value.x, value.y] for value in points]
    generate_csv(csv_file, ['id', 'x', 'y'], data)
    statements = [f'CREATE TABLE {table_name}(id int, x float, y float);\n']
    copy = f"copy {table_name} from '{csv_file}' delimiter ',' HEADER;\n"
    statements.append(copy)
    statements.append(f'CREATE TABLE lr(rate float);\n')
    statements.append(f'INSERT INTO lr(rate) VALUES ({lr});\n')
    statements.append('.exit\n')
    execute_sql(statements, '/home/goellner/.duckdb/cli/latest/duckdb', 'data.db')

def time_benchmark(file_path: str):
    start = datetime.now()
    database = subprocess.Popen(
        ['/home/goellner/.duckdb/cli/latest/duckdb', f'-f {file_path}','./data.db'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output, error = database.communicate()
    time = (datetime.now() - start).total_seconds() * 1000
    return time

def memory_benchmark(file_path: str, key_name: str):
    file_name = f'massif.{key_name}.duckdb.{int(time() * 1000)}'
    database  = subprocess.Popen(
        ['valgrind', '--quiet', '--tool=massif', '--stacks=yes', f'--massif-out-file={file_name}', '/home/goellner/.duckdb/cli/latest/duckdb', '-f', file_path,'./data.db']
    )
    _, error = database.communicate()
    return file_name