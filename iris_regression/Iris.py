import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from Config import CONFIG
import Format
import Database
import Create_CSV
import Postgres
import Time
import Memory
import Helper
import Settings

def main():
    databases = CONFIG['databases']
    scenarios = CONFIG['setups']
    lr = CONFIG['learning_rate']

    for database in databases:
        if database['create_csv'] and not database['ignore']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    for scenario in scenarios:
        if scenario['ignore']:
            continue
        network = scenario['network_size']
        data = scenario['data_size']
        iter = scenario['iterations']
        for database in databases:
            if database['ignore']:
                continue
            name = database['name']
            time_exe = database['time-executable']
            memory_exe = database['memory-executable']
            for type in database['types']:
                for statement in scenario['statements']:
                    content = statement['statement']
                    number = statement['number']
                    for agg in database['aggrations']:
                        print_setting(network, data, name, type, iter,number, agg)
                        generate_statement(content, number, iter, lr, agg)
                        prepare_benchmark(database, type, data, network)

                        time, output = Time.benchmark(time_exe, name, 2, [0, 1], False)
                        if time == -1:
                            if name == 'postgres' or name == 'umbra' or name == 'lingodb':
                                Helper.remove_dir(database['files'])
                            else:
                                Helper.remove_files(database['files'])
                            continue
                        if database['name'] == 'postgres':
                            Postgres.stop_database(database['server-preparation'][3])
                        heap, rss = Memory.benchmark(name, memory_exe, '', f'{name}_{type}_{data}_{network}_{agg}_{number}', Settings.STATEMENT_FILE)

                        Create_CSV.append_row(database['csv_file'], [
                            type, 
                            network, 
                            data,
                            number, 
                            agg,
                            lr,
                            iter, 
                            time, 
                            heap, 
                            rss, 
                            output, 
                            '-'])
                        if database['name'] == 'postgres' or database['name'] == 'umbra':
                            Helper.remove_dir(database['files'])
                        else:
                            Helper.remove_files(database['files'])
    Helper.remove_files([Settings.STATEMENT_FILE])

def print_setting(network_size: int, data_size: int, database: str, type: str, iterations: int, statement: int, agg: str) -> None:
    '''
    This function prints the settings for the current benchmark.

    :param network_size: The size of the hidden layer.
    :param data_size: The number of samples.
    :param database: The database name.
    :param type: The datatype for x and y values.
    :param iterations: The number of update iterations.
    :param statement: The statement number that will be executed.
    :param agg: The aggregation function to be used in the recursive CTE.
    '''
    Format.print_title(f'START BENCHMARK - IRIS-ML-Model WITH THE FOLLOWING SETTINGS')
    Format.print_information(f'Network Size: {network_size}', tabs=1)
    Format.print_information(f'Sample Size: {data_size}', tabs=1)
    Format.print_information(f'Database: {database}', tabs=1)
    Format.print_information(f'Type: {type}', tabs=1)
    Format.print_information(f'Iterations: {iterations}', tabs=1)
    Format.print_information(f'Statement: {statement}', tabs=1)
    Format.print_information(f'Aggregation Function: {agg}', tabs=1)

def prepare_benchmark(database: dict, type: str, data_size: int, network_size: int) -> None:
    '''
    This function prepares the benchmark by creating the database and inserting the data.

    :param database: The database name.
    :param type: The datatype for x and y values.
    :param data_size: The number of samples.
    :param network_size: The number of neurons in the hidden layer.
    '''

    Format.print_information('Preparing benchmark - This can take some time', mark=True)
    extend_file_path = '.' if database['name'] == 'postgres' else ''
    if database['name'] == 'postgres':
        Helper.create_dir(Settings.POSTGRESQL_DIR)
        executables = database['server-preparation']
        Postgres.create_database(executables[0], executables[1], executables[2])
    elif database['name'] == 'umbra':
        Helper.create_dir(Settings.UMBRA_DIR)

    prep_database = Database.Database(database['client-preparation'], database['start-sql'], database['end-sql'])
    prep_database.create_table('iris', ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species'], [type, type, type, type, 'int'])
    prep_database.create_table('iris2', ['id', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species'], ['int', type, type, type, type, 'int'])
    prep_database.create_table('img', ['i', 'j', 'v'], ['int', 'int', type])
    prep_database.create_table('one_hot', ['i', 'j', 'v', 'dummy'], ['int', 'int', 'int', 'int'])
    prep_database.create_table('w_xh', ['i', 'j', 'v'], ['int', 'int', type])
    prep_database.create_table('w_ho', ['i', 'j', 'v'], ['int', 'int', type])
    for _ in range(0, data_size, 150):
        prep_database.insert_from_csv('iris', extend_file_path + './iris.csv')
    prep_database.insert_from_select('iris2', 'SELECT row_number() OVER (), * FROM iris')
    prep_database.insert_from_select('img', 'SELECT id, 1, sepal_length/10 FROM iris2')
    prep_database.insert_from_select('img', 'SELECT id, 2, sepal_width/10 FROM iris2')
    prep_database.insert_from_select('img', 'SELECT id, 3, petal_length/10 FROM iris2')
    prep_database.insert_from_select('img', 'SELECT id, 4, petal_width/10 FROM iris2')
    prep_database.insert_from_select('one_hot', 'select n.i, n.j, coalesce(i.v,0), i.v from (select id,species+1 as species,1 as v from iris2) i right outer join (select a.a as i, b.b as j from (select generate_series as a from generate_series(1,150)) a, (select generate_series as b from generate_series(1,4)) b) n on n.i=i.id and n.j=i.species order by i,j')
    prep_database.insert_from_select('w_xh', f'select i.*,j.*,random()*2-1 from generate_series(1,4) i, generate_series(1,{network_size}) j')
    prep_database.insert_from_select('w_ho', f'select i.*,j.*,random()*2-1 from generate_series(1,{network_size}) i, generate_series(1,3) j')
    prep_database.execute_sql()

def generate_statement(statement: str, number: int, iterations: int, lr: float,  agg: str) -> None:
    '''
    This function generates the SQL file.

    :param statement: The SQL statement to be executed.
    :param number: The statement number.
    :param iterations: The number of iterations in the recursive CTE.
    :param lr: The learning rate.
    :param agg: The aggregation function to be used.
    '''

    function = 'SUM' if agg == 'standard' else 'KAHAN_SUM'
    with open(Settings.STATEMENT_FILE, 'w') as file:
        if number == 1:
            file.write(statement.format(
                function,
                function,
                function,
                function,
                function,
                lr,
                iterations,
                function,
                function
            ))
        else:
            file.write(statement.format(
                function,
                function,
                function,
                function,
                function,
                lr,
                iterations
            ))

if __name__ == '__main__':
    main()