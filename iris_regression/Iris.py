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
import Format
import Database
import Create_CSV
import Postgres
import Time
import Memory
import Relation
import Helper
import Settings
import Parse_Table
import subprocess

def main():
    databases = CONFIG['databases']
    scenarios = CONFIG['setups']
    learning_rate = CONFIG['learning_rate']

    # Create result csv files for each database
    for database in databases:
        if database['create_csv'] and not database['ignore']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    # Iterate over each single scenario
    for scenario in scenarios:
        if scenario['ignore']:
            continue
        network = scenario['network_size']
        data = scenario['data_size']
        iterations = scenario['iterations']
        # Iterate over each database
        for database in databases:
            if database['ignore']:
                continue
            # LingoDB has restricted recursive CTE
            if database['name'] == 'lingodb' and iterations != 20:
                continue
            name = database['name']
            time_exe = database['time-executable']
            memory_exe = database['memory-executable']
            # Iterate over each defined SQL datatype
            for datatype in database['types']:
                # Iterate over each statement
                for statement in scenario['statements']:
                    model = statement['statement']
                    weigths = statement['weights']
                    number = statement['number']
                    print_setting(network, data, name, datatype, iterations, number)
                    query = generate_statement(name, model, iterations, learning_rate)
                    prepare_benchmark(database, datatype, data, network)

                    time = Time.python_time(time_exe)
                    if database['name'] == 'postgres':
                        Postgres.stop_database(database['server-preparation'][3])
                    # -1 means that time benchmark got an timeout. Therefore ignore this setup
                    if time == -1:
                        if name == 'postgres' or name == 'umbra' or name == 'lingodb':
                            Helper.remove_dir(database['files'])
                        else:
                            Helper.remove_files(database['files'])
                        continue

                    memory = []
                    memory_state = []
                    for idx in range(CONFIG['memory_trials']):
                        memory = Memory.python_memory(memory_exe, time, query)
                        # Make measurement multiple times if selected
                        if CONFIG['memory_average']:
                            memory_state.append(memory[0] if memory[0] > 0 else 0) 
                            Format.print_information(f'{idx+1}. Measurement')
                        else:
                            # If psutil does not catch memory correctly, try again
                            if memory[0] > 0:
                                memory_state.append(memory[0]) 
                                break
                            else:
                                Format.print_information('Did not measure a correct value. Try again')

                    accuracy = get_accuracy(database, query)
                    # Create statement that returns only the weights
                    weight_query = generate_statement(name, weigths, iterations, learning_rate)
                    relation_size = get_relation_size(database, datatype, weight_query)

                    Create_CSV.append_row(database['csv_file'], [datatype, network, data, learning_rate, iterations, time, sum(memory_state) / len(memory_state), relation_size, accuracy])
                    if database['name'] == 'postgres' or database['name'] == 'umbra' or name == 'lingodb':
                        Helper.remove_dir(database['files'])
                    else:
                        Helper.remove_files(database['files'])
    Helper.remove_files([Settings.STATEMENT_FILE])

def print_setting(network_size: int, data_size: int, db_name: str, datatype: str, iterations: int, statement: int) -> None:
    '''
    This function prints the settings for the current benchmark.

    :param network_size: The size of the hidden layer.
    :param data_size: The number of samples.
    :param db_name: The database name.
    :param datatype: The datatype for x and y values.
    :param iterations: The number of update iterations.
    :param statement: The statement number that will be executed.
    '''
    Format.print_title(f'START BENCHMARK - IRIS-ML-MODEL WITH THE FOLLOWING SETTINGS')
    Format.print_information(f'Network Size: {network_size}', tabs=1)
    Format.print_information(f'Sample Size: {data_size}', tabs=1)
    Format.print_information(f'Database: {db_name}', tabs=1)
    Format.print_information(f'Type: {datatype}', tabs=1)
    Format.print_information(f'Iterations: {iterations}', tabs=1)
    Format.print_information(f'Statement: {statement}', tabs=1)

def prepare_benchmark(database: dict, datatype: str, data_size: int, network_size: int) -> None:
    '''
    This function prepares the benchmark by creating the database and inserting the data.

    :param database: The database name.
    :param datatype: The datatype for x and y values.
    :param data_size: The number of samples.
    :param network_size: The size of the hidden layer.
    '''

    Format.print_information('Preparing benchmark - This can take some time', mark=True)
    # # Postgres reads csv file from a subdirectory
    extend_file_path = '.' if database['name'] == 'postgres' else ''
    # Create directories for the persistent storage
    if database['name'] == 'postgres':
        Helper.create_dir(Settings.POSTGRESQL_DIR)
        executables = database['server-preparation']
        Postgres.create_database(executables[0], executables[1], executables[2])
    elif database['name'] == 'umbra':
        Helper.create_dir(Settings.UMBRA_DIR)
    elif database['name'] == 'lingodb':
        Helper.create_dir(Settings.LINGODB_DIR)
    
    # DuckDB implicitly specifies the array dimension in the type specification
    array_type = f'{datatype}[]'
    if database['name'] == 'duckdb':
        array_type += '[]'

    prep_database = Database.Database(database['client-preparation'], database['start-sql'], database['end-sql'])
    prep_database.create_table('iris', ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species'], ['float8', 'float8', 'float8', 'float8', 'int'])
    prep_database.create_table('iris3', ['img', 'one_hot'], [array_type, array_type])
    prep_database.create_table('weights', ['id', 'w_xh', 'w_ho'], ['int', array_type, array_type])
    # iris.csv only contains 150 elements, therefore copy it multiple times
    for _ in range(0, data_size, 150):
        prep_database.insert_from_csv('iris', extend_file_path + './iris.csv')
    # DuckDB concat function only works if both parameters are arrays
    if database['name'] == 'duckdb':
        prep_database.insert_from_select('iris3', f'SELECT ARRAY[[sepal_length/10,sepal_width/10,petal_length/10,petal_width/10]] AS img, ARRAY[(array_fill(0::{datatype}, ARRAY[species]) || [1::{datatype}] ) || array_fill(0::{datatype}, ARRAY[2-species])] AS one_hot FROM iris')
    else:
        prep_database.insert_from_select('iris3', f'SELECT ARRAY[[sepal_length/10,sepal_width/10,petal_length/10,petal_width/10]] AS img, ARRAY[(array_fill(0::{datatype}, ARRAY[species]) || 1::{datatype} ) || array_fill(0::{datatype}, ARRAY[2-species])] AS one_hot FROM iris')
    prep_database.insert_from_select('weights', f'SELECT 0, (SELECT array_agg(ys) FROM (SELECT array_agg(val) AS ys FROM (SELECT random()*2-1 AS val, x.generate_series AS x, y.generate_series AS y FROM generate_series(1,4) x, generate_series(1,{network_size}) y) tmp1 GROUP BY x) tmp2), (SELECT array_agg(ys) FROM (SELECT array_agg(val) AS ys FROM (SELECT random()*2-1 AS val, x.generate_series as x, y.generate_series AS y FROM generate_series(1,{network_size}) x, generate_series(1,3) y) tmp3 GROUP BY x) tmp4)')
    prep_database.execute_sql()

def generate_statement(db_name: str, statement: str, iterations: int, learning_rate: float) -> str:
    '''
    This function generates the SQL file.

    :param db_name: The database name.
    :param statement: The SQL statement to be executed.
    :param iterations: The number of iterations in the recursive CTE.
    :param learning_rate: The learning rate.

    :returns: The SQL statement without any placeholders.
    '''

    # SUM function with arrays can only be used in DuckDB by calling the function directly
    function = 'list_sum' if db_name == 'duckdb' else 'SUM'
    query = statement.format(learning_rate, function, learning_rate, function, iterations)
    with open(Settings.STATEMENT_FILE, 'w') as file:
        file.write(query)
    return query

def get_accuracy(database: dict, query: str, iterations: int) -> float:
    '''
    This function receives the accuracy values from each iteration.

    :param database: The database object from CONFIG.
    :param query: The SQL statement that trains a ML model.
    :param iterations: The number of iterations that should be executed.

    :returns: A list of accuracy values if the database is DuckDB, otherwise -1.
    '''
    if database['name'] != 'duckdb':
        return -1
    Format.print_information(f'Get model accuracy', mark=True)
    # Add order by so that the result is sorted
    query = query[:-1]
    query += f' WHERE id = {iterations};'
    # Start database and get the result
    process = subprocess.Popen(
        database['client-preparation'].split() + ['-json'], 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True
    )

    process.stdin.write(query)
    process.stdin.flush()

    output, error = process.communicate()
    if error:
        Format.print_error('An error has been printed during accuracy calculation', error)

    # Parse the result
    result = Parse_Table.output_to_numpy(database['name'], output, 2, [1])
    return result[0][0]

def get_relation_size(database: dict, datatype: str, query: str) -> float:
    '''
    This function reads the size of the output file of a database (only lingodb and
    duckdb. Other databases will get the value -1).

    :param database: The database object from the CONFIG file.
    :param datatype: The datatype of each weight entry.
    :param query: The statement which produces all trained wieghts.

    :returns: The output file size in bytes.
    '''
    if database['name'] != 'lingodb' and database['name'] != 'duckdb':
        return -1
    query = query[:-1]
    array_type = f'{datatype}[]'
    if database['name'] == 'duckdb':
        array_type += '[]'
    # Create table for result and fill it with result content
    prep_database = Database.Database(database['client-preparation'], database['start-sql'], database['end-sql'])
    prep_database.create_table('relation', ['id', 'w_xh', 'w_ho'], ['int', array_type, array_type])
    prep_database.insert_from_select('relation', query)
    prep_database.execute_sql()
    # LingoDB case
    if database['name'] == 'lingodb':
        return Relation.measure_relation_size(f'{Settings.LINGODB_DIR}/relation.arrow')
    # DuckDB case (produces only a single file, therefore delete everything else)
    elif database['name'] == 'duckdb':
        prep_database.clear()
        prep_database.drop_table('iris')
        prep_database.drop_table('iris3')
        prep_database.drop_table('weights')
        prep_database.execute_sql()
        return Relation.measure_relation_size(Settings.DUCK_DB_DATABASE_FILE)

if __name__ == '__main__':
    main()