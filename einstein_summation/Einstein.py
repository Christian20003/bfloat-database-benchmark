import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Parsing')))

from typing import List
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
import Parse_Table
import subprocess

SEMAPHORE = threading.Semaphore()

def main():
    databases = CONFIG['databases']
    scenarios = CONFIG['setups']

    produce_data(scenarios)

    for database in databases:
        if database['create_csv'] and not database['ignore']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    for scenario in scenarios:
        if scenario['ignore']:
            continue
        dimension = scenario['dimension']
        matrix_file = f'./data{scenario["id"]}_ma.csv'
        vector_file = f'./data{scenario["id"]}_vec.csv'
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
                        if not check_execution(name, dimension, number):
                            continue

                        print_setting(dimension, name, type, number, agg)
                        data = generate_statement(content, number, agg)
                        prepare_benchmark(database, type, matrix_file, vector_file)

                        time = Time.python_time(time_exe)
                        if database['name'] == 'postgres':
                            Postgres.stop_database(database['server-preparation'][3])
                        if time == -1:
                            if name == 'postgres' or name == 'umbra' or name == 'lingodb':
                                Helper.remove_dir(database['files'])
                            else:
                                Helper.remove_files(database['files'])
                            continue
                        memory = []
                        for _ in range(CONFIG['memory_trials']):
                            memory = Memory.python_memory(memory_exe, time, data)
                            if memory[0] != 0:
                                break
                            Format.print_information('Restart memory benchmark. Did not measure a value')

                        error = get_error(database, type, data, matrix_file, vector_file)
                        relation_size = get_relation_size(database, type, data)

                        Create_CSV.append_row(database['csv_file'], 
                                              [
                                                  type,
                                                  agg,
                                                  number,
                                                  dimension*dimension, 
                                                  dimension*dimension, 
                                                  dimension,
                                                  time, 
                                                  memory[0], 
                                                  relation_size,
                                                  error
                                               ])
                        
                        if name == 'postgres' or name == 'umbra' or name == 'lingodb':
                            Helper.remove_dir(database['files'])
                        else:
                            Helper.remove_files(database['files'])
    Helper.remove_files([Settings.STATEMENT_FILE])

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
        pass
    elif database == 'postgres':
        pass
    elif database == 'lingodb':
        pass
    return True

def print_setting(dimension: int, database: str, type: str, statement: int, agg_func: str) -> None:
    '''
    This function prints the settings for the current benchmark.

    :param dimension: The number of elements.
    :param database: The database name.
    :param type: The datatype for tensor entries.
    :param statement: The number of the statement that should be used.
    :param agg_func: The aggregation function to be used in the recursive CTE.
    '''

    Format.print_title(f'START BENCHMARK - EINSTEIN SUMMATION WITH THE FOLLOWING SETTINGS')
    Format.print_information(f'Matrix A: {dimension}x{dimension}', tabs=1)
    Format.print_information(f'Matrix B: {dimension}x{dimension}', tabs=1)
    Format.print_information(f'Vector V: {dimension}x1', tabs=1)
    Format.print_information(f'Database: {database}', tabs=1)
    Format.print_information(f'Type: {type}', tabs=1)
    Format.print_information(f'Statement: {statement}', tabs=1)
    Format.print_information(f'Aggregation Function: {agg_func}', tabs=1)

def prepare_benchmark(database: dict, type: str, matrix_file: str, vector_file: str) -> None:
    '''
    This function prepares the benchmark by creating the database and inserting the data.

    :param database: The database object from CONFIG.
    :param type: The type of the matrix / vector entries.
    :param matrix_file: The name of the csv file where the values of matrices are stored.
    :param vector_file: The name of the csv file where the values of vectors are stored.
    '''

    Format.print_information('Preparing benchmark - This can take some time', mark=True)
    # Postgres is inside another directory
    extend_file_path = '.' if database['name'] == 'postgres' else ''
    # Create directories for these database that generate multiple files
    if database['name'] == 'postgres':
        Helper.create_dir(Settings.POSTGRESQL_DIR)
        executables = database['server-preparation']
        Postgres.create_database(executables[0], executables[1], executables[2])
    elif database['name'] == 'umbra':
        Helper.create_dir(Settings.UMBRA_DIR)
    elif database['name'] == 'lingodb':
        Helper.create_dir(Settings.LINGODB_DIR)
    # Create necessary tables
    prep_database = Database.Database(database['client-preparation'], database['start-sql'], database['end-sql'])
    prep_database.create_table('matrixa', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
    prep_database.create_table('matrixb', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
    prep_database.create_table('vectorv', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', type])
    # Copy with bfloat does not work in LingoDB (apache arrow does not support it)
    if database['name'] == 'lingodb' and type == 'bfloat':
        # Workaround by creating float tables and insert the content from them
        prep_database.create_table('data1', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', 'float'])
        prep_database.create_table('data2', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', 'float'])
        prep_database.create_table('data3', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', 'float'])
        prep_database.insert_from_csv('data1', extend_file_path + matrix_file)
        prep_database.insert_from_csv('data2', extend_file_path + matrix_file)
        prep_database.insert_from_csv('data3', extend_file_path + vector_file)
        prep_database.insert_from_select('matrixa', 'SELECT * FROM data1')
        prep_database.insert_from_select('matrixb', 'SELECT * FROM data2')
        prep_database.insert_from_select('vectorv', 'SELECT * FROM data3')
    else:
        prep_database.insert_from_csv('matrixa', extend_file_path + matrix_file)
        prep_database.insert_from_csv('matrixb', extend_file_path + matrix_file)
        prep_database.insert_from_csv('vectorv', extend_file_path + vector_file)
    prep_database.execute_sql()

    # Delete temporary float tables from LingoDB
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

def get_error(database: dict, type: str, statement: str, matrix_file: str, vector_file: str) -> float:
    '''
    This function calculates the Mean-Squared-Error of the matrix multiplication with type DOUBLE as reference.
    This function only works with DuckDB.

    :param database: The database object from CONFIG.
    :param type: The type of the matrix / vector entries.
    :param statement: The statement that should be benchmarked.
    :param matrix_file: The CSV file of the matrix data.
    :param vector_file: The CSV file of the vector data.

    :returns: The MSE of the matrix multiplication if the database is DuckDB, otherwise -1.
    '''
    if database['name'] != 'duckdb' or 'sum' not in statement.lower():
        return -1
    if type == 'double':
        return 0
    Format.print_information(f'Calculate error', mark=True)
    # Generate tables for reference result
    prep_database = Database.Database(database['client-preparation'], database['start-sql'], database['end-sql'])
    prep_database.create_table('refA', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', 'double'])
    prep_database.create_table('refB', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', 'double'])
    prep_database.create_table('refV', ['rowIndex', 'columnIndex', 'val'], ['int', 'int', 'double'])
    prep_database.insert_from_csv('refA', matrix_file)
    prep_database.insert_from_csv('refB', matrix_file)
    prep_database.insert_from_csv('refV', vector_file)
    prep_database.execute_sql()

    # Modify statement with new table names
    statement = statement[:-1]
    statementRef = statement.replace('matrixa', 'refA')
    statementRef = statementRef.replace('matrixb', 'refB')
    statementRef = statement.replace('vectorv', 'refV')

    # Define MSE in SQL
    final_stat = f'SELECT AVG(result) FROM (SELECT pow(truth - pred, 2) AS result FROM (SELECT res1.val AS pred, res2.val AS truth FROM ({statement}) res1 JOIN ({statementRef}) res2 ON res1.rowIndex = res2.rowIndex));'

    # Start database and get the result
    process = subprocess.Popen(
        database['client-preparation'].split() + ['-json'], 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True
    )

    process.stdin.write(final_stat)
    process.stdin.flush()

    output, error = process.communicate()
    if error:
        Format.print_error('An error has been printed during precision calculation', error)

    # Parse the result
    result = Parse_Table.output_to_numpy(database['name'], output, 1, [0])

    # Delete created reference tables for other tests
    prep_database = Database.Database(database['client-preparation'], database['start-sql'], database['end-sql'])
    prep_database.drop_table('refA')
    prep_database.drop_table('refB')
    prep_database.drop_table('refV')
    prep_database.execute_sql()

    return result[0][0]

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
    statement = statement[:-1]
    # Create table for result and fill it with result content
    prep_database = Database.Database(database['client-preparation'], database['start-sql'], database['end-sql'])
    prep_database.create_table('relation', ['rowIndex', 'val'], ['int', type])
    prep_database.insert_from_select('relation', statement)
    prep_database.execute_sql()
    # LingoDB case
    if database['name'] == 'lingodb':
        return Relation.measure_relation_size(f'{Settings.LINGODB_DIR}/relation.arrow')
    # DuckDB case (produces only a single file, therefore delete everything else)
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

def single_thread(rows: List[int], columns: int, file_name: str) -> None:
    '''
    This function represents the task for a single thread to produce benchmark data.
    Relies on the global semaphore.

    :param rows: A list of rows that should be produced by this thread.
    :param columns: The number of columns for each row.
    :param file_name: The name of the file where the data should be stored.
    '''
    for row in rows:
        data = [[row, column, random.random()] for column in range(0, columns)]
        with SEMAPHORE:
            Create_CSV.append_rows(file_name, data)

def produce_data(scenarios: dict) -> None:
    '''
    This function generates the necessary data for the benchmarks. This function
    will generate for each scenarion a single file with the naming scheme: 
    data<scenario_id><ma||vec>.csv

    :param scenarios: A dictionary containing each benchmark setup.
    '''

    Format.print_information(f'Generating data for benchmarks', mark=True)
    # Iterate over each scenario
    for scenario in scenarios:
        # Matrix and vector content will be stored seperatly
        file_name_matrix = f'./data{scenario["id"]}_ma.csv'
        file_name_vector = f'./data{scenario["id"]}_vec.csv'
        # Generate matrix data only if the file does not exist yet
        if not os.path.exists(file_name_matrix):
            Create_CSV.create_csv_file(file_name_matrix, ['rowIndex', 'columnIndex', 'val'])
            chunck_size = scenario['dimension'] // 10
            generated = 0
            threads = []
            # Iterate over each thread
            for _ in range(0, 10):
                rows = []
                # Define how many rows it should generate
                # Last one only produces the remaining rows
                if generated + chunck_size > scenario['dimension']:
                    rows = [row for row in range(generated, scenario['dimension'])]
                else:
                    rows = [row for row in range(generated, generated+chunck_size)]
                generated += chunck_size
                thread = threading.Thread(target=single_thread, args=(rows, scenario['dimension'], file_name_matrix))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
        Format.print_information(f'Data for scenario "{scenario["id"]}" generated')
        # Generate vector data only if the file does not exist yet
        if not os.path.exists(file_name_vector):
            Create_CSV.create_csv_file(file_name_vector, ['rowIndex', 'columnIndex', 'val'])
            data = [[0, column, random.random()] for column in range(0, scenario['dimension'])]
            Create_CSV.append_rows(file_name_vector, data)

if __name__ == "__main__":
    main()
