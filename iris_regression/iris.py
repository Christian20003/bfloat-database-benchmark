import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from Config import CONFIG, STATEMENT_1, STATEMENT_2, STATEMENT_FILE
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

    for database in databases:
        if database['create_csv'] and not database['ignore']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    for scenario in scenarios:
        if scenario['ignore']:
            continue
        for database in databases:
            if database['ignore']:
                continue
            for type in database['types']:
                for statement in scenario['statements']:
                    statement_number = 0
                    if (statement == STATEMENT_1):
                        statement_number = 1
                    elif (statement == STATEMENT_2):
                        statement_number = 2
                    for agg in database['aggrations']:
                        Format.print_title(f'START BENCHMARK - IRIS-REGRESSION WITH HIDDEN_LAYER_WIDTH: {scenario["network_size"]} AND {scenario["data_size"]} SAMPLES, TYPE: {type}, DATABASE: {database["name"]}')
                        generate_statement(statement, scenario['iterations'], agg)
                        prepare_benchmark(database, type, scenario['data_size'], scenario['network_size'])

                        time, output = Time.benchmark(database['execution-bench'], database['name'], 2, [0, 1])
                        server = []
                        if database['name'] == 'postgres':
                            Postgres.stop_database(database['prep'][3])
                            server = [database['prep'][4], database['prep'][3]]
                        heap, rss = Memory.benchmark(database['name'], database['execution-bench'], f'{database["name"]}_{type}_{scenario["data_size"]}_{scenario["network_size"]}_{agg}_{statement_number}', server)

                        Create_CSV.append_row(database['csv_file'], [
                            type, 
                            scenario["network_size"], 
                            scenario["data_size"],
                            statement_number, 
                            agg,
                            CONFIG['learning_rate'],
                            scenario['iterations'], 
                            time, 
                            heap, 
                            rss, 
                            output, 
                            '-'])
                        if database['name'] == 'postgres' or database['name'] == 'umbra':
                            Helper.remove_dir(database['files'])
                        else:
                            Helper.remove_files(database['files'])
    Helper.remove_files([STATEMENT_FILE])

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
        os.mkdir(Settings.POSTGRESQL_DIR)
        executables = database['prep']
        Postgres.create_database(executables[0], executables[1], executables[2])
    elif database['name'] == 'umbra':
        os.mkdir(Settings.UMBRA_DIR)

    prep_database = Database.Database(database['execution'], database['start-sql'], database['end-sql'])
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

def generate_statement(statement: str, iterations: int, aggr_func: str) -> None:
    '''
    This function generates the SQL file.

    :param statement: The SQL statement to be executed.
    :param iterations: The number of iterations in the recursive CTE.
    :param aggr_func: The aggregation function to be used.
    '''

    agg_func = 'SUM' if agg_func == 'standard' else 'KAHAN_SUM'
    with open(STATEMENT_FILE, 'w') as file:
        if statement == STATEMENT_1:
            file.write(statement.format(
                agg_func,
                agg_func,
                agg_func,
                agg_func,
                agg_func,
                iterations,
                agg_func,
                agg_func
            ))
        else:
            file.write(statement.format(
                agg_func,
                agg_func,
                agg_func,
                agg_func,
                agg_func,
                iterations
            ))

if __name__ == '__main__':
    main()