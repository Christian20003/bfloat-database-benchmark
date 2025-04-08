import sys
import os
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Parsing')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Types')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))

from Format import print_title
from Csv import init_csv_file, write_to_csv
from Parse_Args import parse_args
from Config import CONFIG, CTE
from Helper import execute_sql, remove_files, tfloat_switch
from Execute import time_benchmark, memory_benchmark
from Parse_Time import parse_time_metrics
from Parse_Table import parse_table_output
from Parse_Memory import parse_memory_metrics

def main():
    args = parse_args('Kmeans')
    types = CONFIG['types']
    iterations = CONFIG['iterations']
    init_csv_file(['dataSize', 'networkSize', 'accuracy'])
    # Iterate over all benchmarks
    for iteration in iterations:
        for key, value in CONFIG.items():
            if 'setup' not in key:
                continue
            network_size = value["network_size"]
            data_size = value["data_size"]
            print_title(f'### START BENCHMARKING IRIS WITH {network_size} neurons, {data_size} samples ###')
            for type in types:
                if type == 'tfloat':
                    init_iris('irisdummy', data_size, 'float', args)
                    tfloat_switch('iris', 'irisdummy', args)
                else:
                    init_iris('iris', data_size, type, args)
                init_img_tables(data_size, type, args)
                init_weigths(network_size, type, args)
                generate_sql_file(data_size, CONFIG['learning_rate'], iteration, args)
                output = time_benchmark(args)
                results = parse_time_metrics(output)
                database = parse_table_output(output, 1, 0, 0)
                file = memory_benchmark(args, 'iris')
                results = parse_memory_metrics(results, file)
                write_to_csv(results, 'Iris', type, [data_size, network_size, database[0]])


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
        
def init_iris(table_name: str, data_size: int, type: str, paths: dict) -> None:
    '''
    This function initializes the iris table with a defines number of tuples.

    :param table_name: The name of the resulting table.
    :param data_size: The number of tuples in the table.
    :param type: The type of important columns of the resulting table.
    :param paths: A dictionary with important paths of executables and directories. 
    '''

    files = [f'{table_name}.arrow', f'{table_name}.arrow.sample', f'{table_name}.metadata.json']
    remove_files(files, paths['storage'])
    generate_iris_csv(int(data_size / 150))
    statements = [
        'SET persist=1;\n',
        f'CREATE TABLE {table_name}(id int, sepal_length {type}, sepal_width {type}, petal_length {type}, petal_width {type}, species int);\n',
        f"COPY {table_name} from './iris2.csv' delimiter ',' HEADER CSV;\n"
    ]
    execute_sql(statements, paths['exe'], paths['storage'])

def init_img_tables(data_size: int, type: str, paths: dict) -> None:
    '''
    This function initializes the image table.

    :param data_size: The number of tuples in the table (iris table).
    :param type: The type of important columns of the resulting table.
    :param paths: A dictionary with important paths of executables and directories. 
    '''

    files = []
    tables_names = ['data', 'one_hot']
    for file in tables_names:
        files.append(f'{file}.arrow')
        files.append(f'{file}.arrow.sample')
        files.append(f'{file}.metadata.json')
    remove_files(files, paths['storage'])

    statements = [
        'SET persist=1;\n',
        f'CREATE TABLE {tables_names[0]}(sample_id int, feature_id int, value {type});\n',
        f'CREATE TABLE {tables_names[1]}(sample_id int, species_id int, isValid int, dummy int);\n',
        f'INSERT INTO {tables_names[0]} (SELECT id, 1, sepal_length / 10 FROM iris);\n',
        f'INSERT INTO {tables_names[0]} (SELECT id, 2, sepal_width / 10 FROM iris);\n',
        f'INSERT INTO {tables_names[0]} (SELECT id, 3, petal_length / 10 FROM iris);\n',
        f'INSERT INTO {tables_names[0]} (SELECT id, 4, petal_width / 10 FROM iris);\n',
        f'''INSERT INTO one_hot (SELECT result.sample_id, result.species_id, coalesce(samples.value, 0), samples.value
            FROM (SELECT id, species+1 AS species, 1 AS value FROM iris) samples RIGHT OUTER JOIN 
            (SELECT data_table.id AS sample_id, species_table.id AS species_id
            FROM (SELECT generate_series AS id FROM generate_series(1, {data_size})) data_table, 
            (SELECT generate_series AS id FROM generate_series(1,4)) species_table) result ON result.sample_id = samples.id AND result.species_id=samples.species ORDER BY sample_id, species_id);\n'''
    ]
    execute_sql(statements, paths['exe'], paths['storage'])

def init_weigths(hidden_layer: int, type: str, paths: dict) -> None:
    '''
    This function creates the weight tables.

    :param hidden_layer: The number of neurons in the hidden layer.
    :param type: The type of important columns of the resulting table.
    :param paths: A dictionary with important paths of executables and directories.
    '''

    files = []
    tables_names = ['weights_layer1_layer2', 'weights_layer2_layer3']
    for file in tables_names:
        files.append(f'{file}.arrow')
        files.append(f'{file}.arrow.sample')
        files.append(f'{file}.metadata.json')
    remove_files(files, paths['storage'])

    statements = [
        'SET persist=1;\n',
        f'CREATE TABLE {tables_names[0]}(input int, output int, value {type});\n',
        f'CREATE TABLE {tables_names[1]}(input int, output int, value {type});\n',
        f'INSERT INTO {tables_names[0]} (SELECT i.generate_series, j.generate_series, random()*2-1 FROM generate_series(1, 4) i, generate_series(1, {hidden_layer}) j);\n',
        f'INSERT INTO {tables_names[1]} (SELECT i.generate_series, j.generate_series, random()*2-1 FROM generate_series(1, {hidden_layer}) i, generate_series(1, 3) j);\n'
    ]
    execute_sql(statements, paths['exe'], paths['storage'])

def generate_sql_file(data_size: int, lr: float, iterations: int, paths: dict) -> None:
    '''
    This function generates the Statement.sql file for the benchmark.

    :param data_size: The number of training samples.
    :param lr: The learning rate.
    :param iterations: Number of iterations in the CTE.
    :param paths: A dictionary with important paths of executables and directories.
    '''
    with open(paths['statement'], mode='w') as file:
        file.write(CTE.format(data_size, data_size, lr, iterations))

if __name__ == '__main__':
    main()