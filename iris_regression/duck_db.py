import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Parsing')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Types')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))

from Helper import execute_sql, remove_files
from Parse_Memory import parse_memory_metrics
from datetime import datetime
from time import time
import subprocess
import csv

def duck_db_benchmark(data_size: int, network_size: int, file_path: str, key_name: str) -> None:
    print('PSEUDO-DUCKDB BENCHMARK')
    remove_files(['data.db'], '.')
    insert_data(data_size, network_size)
    time = time_benchmark(file_path)
    file_name = memory_benchmark(file_path, key_name)
    result = parse_memory_metrics({}, file_name)
    return time, result['memory']['total']

def generate_iris_csv(amount: int) -> None:
    '''
    This function generates the the iris.csv file.

    :param amount: How many time the content should be copied.
    '''
    data = []
    with open('./iris.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        data = [row for row in reader]
    length = len(data)
    for counter in range(amount):
        for element in data[1:length].copy():
            data.append(element.copy())
    for idx, entry in enumerate(data):
        entry.insert(0, idx + 1)
    with open('./iris2.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def insert_data(data_size: int, network_size: int) -> None:
    remove_files(['data.db'], '.')
    generate_iris_csv(int(data_size / 150))
    statements = [
        f'CREATE TABLE iris(id int, sepal_length float, sepal_width float, petal_length float, petal_width float, species int);\n',
        f"COPY iris from './iris2.csv' delimiter ',' HEADER CSV;\n",
        f'CREATE TABLE data(sample_id int, feature_id int, value float);\n',
        f'CREATE TABLE one_hot(sample_id int, species_id int, isValid int, dummy int);\n',
        f'INSERT INTO data (SELECT id, 1, sepal_length / 10 FROM iris);\n',
        f'INSERT INTO data (SELECT id, 2, sepal_width / 10 FROM iris);\n',
        f'INSERT INTO data (SELECT id, 3, petal_length / 10 FROM iris);\n',
        f'INSERT INTO data (SELECT id, 4, petal_width / 10 FROM iris);\n',
        f'''INSERT INTO one_hot (SELECT result.sample_id, result.species_id, coalesce(samples.value, 0), samples.value
            FROM (SELECT id, species+1 AS species, 1 AS value FROM iris) samples RIGHT OUTER JOIN 
            (SELECT data_table.id AS sample_id, species_table.id AS species_id
            FROM (SELECT generate_series AS id FROM generate_series(1, {data_size})) data_table, 
            (SELECT generate_series AS id FROM generate_series(1,4)) species_table) result ON result.sample_id = samples.id AND result.species_id=samples.species ORDER BY sample_id, species_id);\n''',
        f'CREATE TABLE weights_layer1_layer2(input int, output int, value float);\n',
        f'CREATE TABLE weights_layer2_layer3(input int, output int, value float);\n',
        f'INSERT INTO weights_layer1_layer2 (SELECT i.generate_series, j.generate_series, random()*2-1 FROM generate_series(1, 4) i, generate_series(1, {network_size}) j);\n',
        f'INSERT INTO weights_layer2_layer3 (SELECT i.generate_series, j.generate_series, random()*2-1 FROM generate_series(1, {network_size}) i, generate_series(1, 3) j);\n',
        '.exit\n'
    ]
    execute_sql(statements, '/home/goellner/.duckdb/cli/latest/duckdb', './data.db')

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