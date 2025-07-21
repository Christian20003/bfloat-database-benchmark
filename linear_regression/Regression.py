import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Parsing')))

from Config import CONFIG
import random
import subprocess
import threading
import Format
import Helper
import Database
import Postgres
import Settings
import Create_CSV
import Relation
import Memory
import Time
import Parse_Table

SEMAPHORE = threading.Semaphore()

def main():
    databases = CONFIG['databases']
    scenarios = CONFIG['setups']

    # Generate data if not already done
    produce_data(scenarios)

    # Generate result CSV files for each database 
    for database in databases:
        if database['create_csv'] and not database['ignore']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    # Iterate over each defined scenarion
    for scenario in scenarios:
        # Scenarios can be deactivated
        if scenario['ignore']:
            continue
        parameters = scenario['params_amount']
        points = scenario['points_amount']
        iterations = scenario['iterations']
        learning_rate = scenario['lr']
        statement = scenario['statement']
        # Iterate over each database
        for database in databases:
            if database['ignore']:
                continue
            name = database['name']
            time_exe = database['time-executable']
            memory_exe = database['memory-executable']
            # Iterate over each defined database type
            for datatype in database['types']:
                # Iterate over each defined database aggregation function
                for aggregation in database['aggregations']:
                    # Check if specific setup should be ignored
                    if not check_execution(name, points, parameters, aggregation, datatype):
                        continue

                    # Prepare benchmark
                    data_file = f'gd_{parameters}.csv'
                    setup_file = 'gd_bench.csv'
                    print_setting(name, points, parameters, aggregation, datatype, iterations, learning_rate)
                    query = generate_statement(statement, name, parameters, aggregation, datatype, iterations, learning_rate)
                    prepare_benchmark(database, points, CONFIG['param_start'], parameters-1, datatype, data_file, setup_file)

                    # Execute time benchmark
                    time = Time.python_time(time_exe)
                    # Stop postgres server (memory benchmark will be done otherwise)
                    if database['name'] == 'postgres':
                        Postgres.stop_database(database['server-preparation'][3])
                    # If timeout occurs clean setup and jump to next one
                    if time == -1:
                        if name == 'postgres' or name == 'umbra' or name == 'lingodb':
                            Helper.remove_dir(database['files'])
                        else:
                            Helper.remove_files(database['files'])
                        continue

                    memory = []
                    # Execute memory benchmark (if psutil does not catch memory correctly, try again)
                    for _ in range(CONFIG['memory_trials']):
                        memory = Memory.python_memory(memory_exe, time, query)
                        if memory[0] < 0:
                            break
                        Format.print_information('Restart memory benchmark. Did not measure a value')

                    # Get MSE and relation size
                    error = get_error(database, datatype, parameters-1, query, iterations)
                    relation_size = get_relation_size(database, datatype, query)

                    # Write results to CSV file and clean setup
                    Create_CSV.append_row(database['csv_file'], [datatype, aggregation, parameters, points, iterations, time, memory[0], relation_size, error])
                    if name == 'postgres' or name == 'umbra' or name == 'lingodb':
                        Helper.remove_dir(database['files'])
                    else:
                        Helper.remove_files(database['files'])
    Helper.remove_files(['gd_bench.csv', Settings.STATEMENT_FILE])

def check_execution(db_name: str, points: int, parameters: int, aggregation: str, datatype: str) -> bool:
    '''
    This function allows some custom specifications about which specific setups should be ignored.

    :param db_name: The name of the database.
    :param points: The number of points used to learn all parameters.
    :param parameters: The number of parameters learned with gradient descent.
    :param aggregations: The type of aggregation function that is used during training.
    :param datatype: The datatype of all variables and parameters.

    :returns: True if the scenario should be executed, otherwise false.
    '''

    if db_name == 'duckdb':
        pass
    elif db_name == 'umbra':
        pass
    elif db_name == 'postgres':
        pass
    elif db_name == 'lingodb':
        pass
    return True

def print_setting(db_name: str, points: int, parameters: int, aggregation: str, datatype: str, iterations: int, learning_rate: float) -> None:
    '''
    This function prints the settings of the benchmark to the console.

    :param db_name: The name of the database.
    :param points: The number of points used to learn all parameters.
    :param parameters: The number of parameters learned with gradient descent.
    :param aggregation: The type of aggregation function that is used during training.
    :param datatype: The datatype of all variables and parameters.
    :param iterations: The number of update iterations.
    :param learning_rate: The learning rate for gradient descent.
    '''
    Format.print_title(f'START BENCHMARK - LINEAR-REGRESSION WITH THE FOLLOWING SETTINGS')
    Format.print_information(f'Points: {points}', tabs=1)
    Format.print_information(f'Parameters: {parameters}', tabs=1)
    Format.print_information(f'Database: {db_name}', tabs=1)
    Format.print_information(f'Type: {datatype}', tabs=1)
    Format.print_information(f'Iterations: {iterations}', tabs=1)
    Format.print_information(f'Learning Rate: {learning_rate}', tabs=1)
    Format.print_information(f'Aggregation Function: {aggregation}', tabs=1)

def generate_statement(statement: str, db_name: str, parameters: int, aggregation: str, datatype: str, iterations: int, learning_rate: float) -> str:
    '''
    This function generates the SQL statement for the benchmark.

    :param statement: The SQL statement to be executed with placeholders.
    :param db_name: The name of the database.
    :param parameters: The number of parameters learned with gradient descent.
    :param aggregation: The type of aggregation function that is used during training.
    :param datatype: The datatype of all variables and parameters.
    :param iterations: The number of update iterations.
    :param learning_rate: The learning rate for gradient descent.

    :returns: The SQL query with all placeholders replaced.
    '''

    function = 'AVG' if aggregation == 'standard' else 'FAVG'
    with open(Settings.STATEMENT_FILE, 'w') as file:
        content = []
        # Add aggregation function and lr to the statement
        for _ in range(parameters):
            content.append(learning_rate)
            content.append(function)
        # Add type casts if necessary
        for _ in range(parameters):
            if db_name == 'postgres' and type == 'float4':
                content.append(f'::{datatype}')
            else:
                content.append('')
        content.append(iterations)
        statement = statement.format(*content)
        file.write(statement)
        return statement

def prepare_benchmark(database: dict, points: int, parameter: float, variables: int, datatype: str, src: str, dst: str) -> None:
    '''
    This function prepares the benchmark by creating the necessary tables and copying the data
    from the source file to the destination file.

    :param database: The database object from the CONFIG file.
    :param points: The number of points used to learn all parameters.
    :param parameter: The value of all parameters.
    :param variables: The number of variables in the points.
    :param datatype: The datatype of all variables and parameters.
    :param src: The name of the csv file, where the points are stored.
    :param dst: The name of the csv file, where the needed points are stored.
    '''

    Format.print_information('Preparing benchmark - This can take some time', mark=True)
    # Generate the csv file with the points only needed
    Helper.copy_csv_file(src, dst, points + 1, variables)
    # Postgres reads csv file from a subdirectory
    file = '../' + dst if database['name'] == 'postgres' else './' + dst
    # For some databases create directories
    if database['name'] == 'postgres':
        Helper.create_dir(Settings.POSTGRESQL_DIR)
        executables = database['server-preparation']
        Postgres.create_database(executables[0], executables[1], executables[2])
    elif database['name'] == 'umbra':
        Helper.create_dir(Settings.UMBRA_DIR)
    elif database['name'] == 'lingodb':
        Helper.create_dir(Settings.LINGODB_DIR)
    
    letters = 'abcdefghijklmnopqrstuvwxyz'
    # List of inital values for each parameter
    parameters = [parameter for _ in range(variables+1)]
    gd_columns = ['idx'] + [letters[value] for value in range(variables+1)]
    gd_columns_types = ['int'] + [type for _ in range(variables+1)]
    points_columns = ['y'] + [f'x{i+1}' for i in range(variables)]
    points_columns_types = [type] + [type for _ in range(variables)]

    prep_database = Database.Database(database['client-preparation'], database['start-sql'], database['end-sql'])
    prep_database.create_table('gd_start', gd_columns, gd_columns_types)
    prep_database.create_table('points', points_columns, points_columns_types)
    # Copy with bfloat does not work in LingoDB (apache arrow does not support it)
    if database['name'] == 'lingodb' and type == 'bfloat':
        points_columns_types = ['float'] + ['float' for _ in range(variables)]
        prep_database.create_table('data', points_columns, points_columns_types)
        prep_database.insert_from_csv('data', file)
        prep_database.insert_from_select('points', 'SELECT * FROM data')
    else:
        prep_database.insert_from_csv('points', file)
    prep_database.insert_from_select('gd_start', f'SELECT 0, {",".join(str(parameters))}')
    prep_database.execute_sql()

    # Remove float tables, because that should not be there for bfloat benchmark
    if database['name'] == 'lingodb' and type == 'bfloat':
        Helper.remove_files([
            f'{Settings.LINGODB_DIR}/data.arrow', 
            f'{Settings.LINGODB_DIR}/data.arrow.sample', 
            f'{Settings.LINGODB_DIR}/data.metadata.json',
        ])

def get_relation_size(database: dict, statement: str, datatype: str) -> float:
    '''
    This function reads the size of the output file of a database (only lingodb and
    duckdb. Other databases will get the value -1).

    :param database: The database object from the CONFIG file.
    :param statement: The SQL statement to be executed.
    :param datatype: The datatype of all variables and parameters.

    :returns: The output file size in bytes.
    '''
    if database['name'] != 'lingodb' and database['name'] != 'duckdb':
        return -1
    # Eliminate the last semicolon
    statement = statement[:-1]
    # Create table for result and fill it with result content
    prep_database = Database.Database(database['client-preparation'], database['start-sql'], database['end-sql'])
    prep_database.create_table('relation', ['rowIndex', 'val'], ['int', datatype])
    prep_database.insert_from_select('relation', statement)
    prep_database.execute_sql()
    # LingoDB case
    if database['name'] == 'lingodb':
        return Relation.measure_relation_size(f'{Settings.LINGODB_DIR}/relation.arrow')
    # DuckDB case (produces only a single file, therefore delete everything else)
    elif database['name'] == 'duckdb':
        prep_database.clear()
        prep_database.drop_table('points')
        prep_database.drop_table('gd_start')
        prep_database.execute_sql()
        return Relation.measure_relation_size(Settings.DUCK_DB_DATABASE_FILE)

def get_error(database: dict, statement: str, variables: int, iterations: int) -> float:
    '''
    This function calculates the mean squared error (MSE) of the gradient descent
    algorithm in DuckDB.

    :param database: The database object from CONFIG file.
    :param statement: The SQL statement to be executed.
    :param variables: The number of variables in the points.
    :param iterations: The number of update iterations.

    :returns: The mean squared error (MSE) of the gradient descent algorithm in DuckDB, otherwise -1.
    '''
    if database['name'] != 'duckdb':
        return -1
    # Eliminate the last semicolon
    statement = statement[:-1]
    letters = 'abcdefghijklmnopqrstuvwxyz'
    # Create a list of parameter names
    parameter_column = [letters[i] for i in range(variables+1)]
    # Create the statement to calculate a prediction
    pred = [f'x{i+1} * {letters[i]}' for i in range(variables)]
    pred_stmt = f'SELECT {'+'.join(pred)} +' + letters[variables]

    # Create the final statement to calculate the MSE
    final_stmt = f'WITH paramter({','.join(parameter_column)}) AS ({statement}) SELECT AVG(result) FROM (SELECT pow(y - pred, 2) AS result FROM ({pred_stmt} AS pred, y FROM points, parameter WHERE idx = {iterations}));\n'

    # Start database and get the result
    process = subprocess.Popen(
        database['client-preparation'].split() + ['-json'], 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True
    )

    process.stdin.write(final_stmt)
    process.stdin.flush()

    output, error = process.communicate()
    if error:
        Format.print_error('An error has been printed during precision calculation', error)

    # Parse the result
    result = Parse_Table.output_to_numpy(database['name'], output, 1, [0])

    return result[0]

def single_thread(points: int, variables: int, parameter: float, file_name: str) -> None:
    '''
    This function represents the task for a single thread to produce benchmark data.
    Relies on the global semaphore.

    :param points: The number of points this thread should produce.
    :param variables: How many variables a point should have.
    :param parameter: The value of all parameters.
    :param file_name: The name of the file where the data should be stored.
    '''
    counter = 0
    while counter <= points:
        chunk = 100000 if counter + 100000 <= points else points - counter
        data = []
        for point in range(chunk):
            x = [random.random() for _ in range(variables)]
            y = sum([var * parameter for var in x]) + parameter
            data.append([y] + x)
        with SEMAPHORE:
            Create_CSV.append_rows(file_name, data)
        counter += chunk        

def produce_data(scenarios: dict) -> None:
    '''
    This function generates the necessary data for the benchmarks. This function
    will generate multiple files. Each file consists points data with a specific amount
    of variables for a single point (multiple xs). The name of the files will be 
    './gd_<parameter_amount>.csv'

    :param scenarios: A dictionary containing each benchmark setup.
    '''

    # Identify every setup with different amounts of parameters and 
    # get the setup with the highest number of points
    data_files = {}
    for scenario in scenarios:
        key = scenario['params_amount']
        if key in data_files:
            if data_files[key] < scenario['points_amount']:
                data_files[key] = scenario['points_amount']
        else:
            data_files[key] = scenario['points_amount']

    Format.print_information(f'Generating data for benchmarks', mark=True)
    for key, value in data_files.items():
        file_name = f'./gd_{key}.csv'
        if os.path.exists(file_name):
            continue

        parameter = CONFIG['param_value']
        points = value
        variables = key-1

        header = ['y'] + [f'x{i+1}' for i in range(variables)]
        Create_CSV.create_csv_file(file_name, header)

        chunk = points // 10
        assigned = 0
        threads = []
        # Iterate over each thread
        for _ in range(0, 10):
            if assigned + chunk > points:
                thread = threading.Thread(target=single_thread, args=(points-chunk, variables, parameter, file_name))
                threads.append(thread)
                thread.start()
            else:
                thread = threading.Thread(target=single_thread, args=(chunk, variables, parameter, file_name))
                threads.append(thread)
                thread.start()
            assigned += chunk

        for thread in threads:
            thread.join()
        Format.print_information(f'Generating data for {key} parameters')

if __name__ == "__main__":
    main()
