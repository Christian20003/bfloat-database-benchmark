import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from Config import CONFIG
import random
import threading
import Format
import Database
import Postgres
import Create_CSV
import Time
import Memory
import Relation
import Settings
import Helper

SEMAPHORE = threading.Semaphore()

def main():
    databases = CONFIG['databases']
    scenarios = CONFIG['setups']
    data_file = './data.csv'

    key = list(scenarios.keys())[-1]
    max_setup = scenarios[key]

    produce_data(max_setup['dimension1'], data_file)

    for database in databases:
        if database['create_csv'] and not database['ignore']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    for scenario in scenarios:
        if scenario['ignore']:
            continue
        rowsA = scenario['dimension_1']
        rowsB = scenario['dimension_2']
        rowsC = scenario['dimension_3']
        for database in databases:
            if database['ignore']:
                continue
            name = database['name']
            time_exe = database['time-executable']
            memory_exe = database['memory-executable']
            for type in database['types']:
                for statement in scenario['statements']:
                    number = statement['number']
                    content = statement['statement']
                    for agg in database['aggregations']:
                        if not check_execution(name, rowsA, number):
                            continue

                        print_setting(rowsA, rowsB, rowsC, name, type, number, agg)
                        data = generate_statement(content, number, agg)
                        prepare_benchmark(database, type, data_file, rowsA)

                        time = Time.python_time(time_exe)
                        if time == -1:
                            if name == 'postgres' or name == 'umbra' or name == 'lingodb':
                                Helper.remove_dir(database['files'])
                            else:
                                Helper.remove_files(database['files'])
                            continue
                        memory = 0
                        if database['name'] == 'postgres':
                            Postgres.stop_database(database['server-preparation'][3])
                            memory = Memory.python_memory(memory_exe, time, data)
                        else:
                            memory = Memory.python_memory(memory_exe, time)

                        relation_size = get_relation_size(database, type, data)

                        Create_CSV.append_row(database['csv_file'], 
                                              [
                                                  type,
                                                  agg,
                                                  number,
                                                  rowsA*rowsB, 
                                                  rowsB*rowsC, 
                                                  rowsC,
                                                  time, 
                                                  memory[0], 
                                                  relation_size
                                               ])
                        
                        if name == 'postgres' or name == 'umbra' or name == 'lingodb':
                            Helper.remove_dir(database['files'])
                        else:
                            Helper.remove_files(database['files'])
    Helper.remove_files([data_file, Settings.STATEMENT_FILE])

def check_execution(database: str, setup_id: int, number: int) -> bool:
    '''
    This function checks if the current setup should be executed. These decision have been
    defined through experience from previous executions.

    :param database: The name of the database.
    :param setup_id: The size of each dimension.
    :param number: The statement number.

    :returns: True if the setup can be executed otherwise false
    '''
    
    if database == 'duckdb':
        pass
    elif database == 'umbra':
        if number == 1 and setup_id >= 2500:
            return False
    elif database == 'postgres':
        pass
    elif database == 'lingodb':
        pass
    return True

def print_setting(dimension1: int, dimension2: int, dimension3: int, database: str, type: str, statement: int, agg_func: str) -> None:
    '''
    This function prints the settings for the current benchmark.

    :param dimension1: The number of rows in the first matrix.
    :param dimension2: The number of columns in the first matrix and rows in the second matrix.
    :param dimension3: The number of columns in the second matrix and rows in the vector.
    :param database: The database name.
    :param type: The datatype for tensor entries.
    :param statement: The number of the statement that should be used.
    :param agg_func: The aggregation function to be used in the recursive CTE.
    '''

    Format.print_title(f'START BENCHMARK - EINSTEIN SUMMATION WITH THE FOLLOWING SETTINGS')
    Format.print_information(f'Matrix A: {dimension1}x{dimension2}', tabs=1)
    Format.print_information(f'Matrix B: {dimension2}x{dimension3}', tabs=1)
    Format.print_information(f'Vector V: {dimension3}x1', tabs=1)
    Format.print_information(f'Database: {database}', tabs=1)
    Format.print_information(f'Type: {type}', tabs=1)
    Format.print_information(f'Statement: {statement}', tabs=1)
    Format.print_information(f'Aggregation Function: {agg_func}', tabs=1)

def prepare_benchmark(database: dict, type: str, data_file: str, rowIndex: int) -> None:
    '''
    This function prepares the benchmark by creating the database and inserting the data.

    :param database: The database name.
    :param type: The datatype for x and y values.
    :param data_file: The name of the csv file where the values of are stored.
    '''

    Format.print_information('Preparing benchmark - This can take some time', mark=True)
    extend_file_path = '.' if database['name'] == 'postgres' else ''
    counter = rowIndex / 10
    if database['name'] == 'postgres':
        Helper.create_dir(Settings.POSTGRESQL_DIR)
        executables = database['server-preparation']
        Postgres.create_database(executables[0], executables[1], executables[2])
    elif database['name'] == 'umbra':
        Helper.create_dir(Settings.UMBRA_DIR)
    elif database['name'] == 'lingodb':
        Helper.create_dir(Settings.LINGODB_DIR)
    prep_database = Database.Database(database['client-preparation'], database['start-sql'], database['end-sql'])
    prep_database.create_table('matrixa', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
    prep_database.create_table('matrixb', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
    prep_database.create_table('vectorv', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
    # Copy with bfloat does not work (apache arrow does not support it)
    if database['name'] == 'lingodb' and type == 'bfloat':
        prep_database.create_table('data1', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', 'float'])
        prep_database.create_table('data2', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', 'float'])
        prep_database.create_table('data3', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', 'float'])
        prep_database.insert_einstein_data('data1', extend_file_path + data_file, counter)
        prep_database.insert_einstein_data('data2', extend_file_path + data_file, counter)
        prep_database.insert_einstein_data('data3', extend_file_path + data_file, 1)
        prep_database.insert_from_select('matrixa', 'SELECT * FROM data1')
        prep_database.insert_from_select('matrixb', 'SELECT * FROM data2')
        prep_database.insert_from_select('vectorv', 'SELECT * FROM data3')
    else:
        prep_database.insert_einstein_data('matrixa', extend_file_path + data_file, counter)
        prep_database.insert_einstein_data('matrixb', extend_file_path + data_file, counter)
        prep_database.insert_einstein_data('vectorv', extend_file_path + data_file, 1)
    prep_database.execute_sql()

    if database['name'] == 'lingodb' and type == 'bfloat':
        Helper.remove_files([
            f'{Settings.LINGODB_DIR}/data1.arrow', 
            f'{Settings.LINGODB_DIR}/data1.arrow.sample', 
            f'{Settings.LINGODB_DIR}/data1.metadata.json',
            f'{Settings.LINGODB_DIR}/data2.arrow', 
            f'{Settings.LINGODB_DIR}/data2.arrow.sample', 
            f'{Settings.LINGODB_DIR}/data2.metadata.json',
            f'{Settings.LINGODB_DIR}/data3.arrow', 
            f'{Settings.LINGODB_DIR}/data3.arrow.sample', 
            f'{Settings.LINGODB_DIR}/data3.metadata.json',
        ])

def get_relation_size(database: dict, type: str, statement: str) -> float:
    '''
    This function reads the size of the output file of a database (only lingodb and
    duckdb. Other databases will get the value -1).

    :param database: The database object from the CONFIG file.
    :param type: The type of each matrix entry.
    :param statement: The statement which will be benchmarked.

    :returns: The output file size in bytes.
    '''
    if database['name'] != 'lingodb' and database['name'] != 'duckdb':
        return -1
    prep_database = Database.Database(database['client-preparation'], database['start-sql'], database['end-sql'])
    prep_database.create_table('result', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
    prep_database.insert_from_select('result', statement)
    prep_database.execute_sql()
    if database['name'] == 'lingodb':
        return Relation.measure_relation_size(f'{Settings.LINGODB_DIR}/result.arrow')
    elif database['name'] == 'duckdb':
        prep_database.clear()
        prep_database.drop_table('matrixa')
        prep_database.drop_table('matrixb')
        prep_database.drop_table('vectorv')
        prep_database.execute_sql()
        return Relation.measure_relation_size(Settings.DUCK_DB_DATABASE_FILE)

def generate_statement(statement: str, number: int, aggr_func: str) -> str:
    '''
    This function generates the SQL statement for the database.
    
    :param statement: The type of statement that should be used.
    :param number: The number of the statement.
    :param aggr_func: The aggregation function that should be used.

    :returns: The SQL statement without any placeholders.
    '''

    function = 'SUM' if aggr_func == 'standard' else 'KAHAN_SUM'
    with open(Settings.STATEMENT_FILE, 'w') as file:
        if number == 1 or number == 3:
            file.write(statement.format(function))
            return statement.format(function)
        elif number == 4:
            file.write(statement.format(function, function))
            return statement.format(function, function)
        else:
            file.write(statement)
            return statement

def single_thread(start: int, stop: int, file_name: str) -> None:
    data = [[0, column, random.random()] for column in range(start, stop)]
    with SEMAPHORE:
        Create_CSV.append_rows(file_name, data)

def produce_data(columns: int, file_name: str) -> None:
    '''
    This function generates the necessary data for the benchmarks.

    :param columns: The number of columns in the tensor.
    :param file_name: The name of the csv file where the data should be stored.
    '''

    if not os.path.exists(file_name):
        Format.print_information(f'Generating data for benchmark', mark=True)
        Create_CSV.create_csv_file(file_name, ['rowIndex', 'columnIndex', 'val'])
        chunck = columns / 10
        threads = []
        for number in range(1, 11):
            thread = threading.Thread(target=single_thread, args=(number * chunck, (number+1) * chunck, file_name))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()
