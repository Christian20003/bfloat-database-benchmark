import sys
import os
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))

from typing import List
from Config import CONFIG, STATEMENT
import random
import Format
import Database
import Create_CSV
import Helper
import numpy as np
import tensorflow as tf

def main():
    databases = CONFIG['databases']
    scenarios = CONFIG['setups']

    for database in databases:
        if database['create_csv']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    for scenario in scenarios:
        if scenario['ignore']:
            continue
        generate_statement(scenario['iterations'])
        for database in databases:
            for type in database['types']:
                Format.print_title(f'START BENCHMARK - IRIS-REGRESSION WITH HIDDEN_LAYER_WIDTH: {scenario["network_size"]} AND {scenario["data_size"]} SAMPLES')
                prep_database = Database.Database(database['execution'], database['start-sql'], database['end-sql'])
                prep_database.create_table('iris', ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species'], [type, type, type, type, 'int'])
                prep_database.create_table('iris2', ['id', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species'], ['int', type, type, type, type, 'int'])
                prep_database.create_table('img', ['i', 'j', 'v'], ['int', 'int', type])
                prep_database.create_table('one_hot', ['i', 'j', 'v', 'dummy'], ['int', 'int', 'int', 'int'])
                prep_database.create_table('w_xh', ['i', 'j', 'v'], ['int', 'int', type])
                prep_database.create_table('w_ho', ['i', 'j', 'v'], ['int', 'int', type])
                for _ in range(0, scenario['data_size'], 150):
                    prep_database.insert_from_csv('iris', './iris.csv', [], [])
                prep_database.insert_from_select('iris2', 'SELECT row_number() OVER (), * FROM iris')
                prep_database.insert_from_select('img', 'SELECT id, 1, sepal_length/10 FROM iris2')
                prep_database.insert_from_select('img', 'SELECT id, 2, sepal_width/10 FROM iris2')
                prep_database.insert_from_select('img', 'SELECT id, 3, petal_length/10 FROM iris2')
                prep_database.insert_from_select('img', 'SELECT id, 4, petal_width/10 FROM iris2')
                prep_database.insert_from_select('one_hot', 'select n.i, n.j, coalesce(i.v,0), i.v from (select id,species+1 as species,1 as v from iris2) i right outer join (select a.a as i, b.b as j from (select generate_series as a from generate_series(1,150)) a, (select generate_series as b from generate_series(1,4)) b) n on n.i=i.id and n.j=i.species order by i,j')
                prep_database.insert_from_select('w_xh', f'select i.*,j.*,random()*2-1 from generate_series(1,4) i, generate_series(1,{scenario["network_size"]}) j')
                prep_database.insert_from_select('w_ho', f'select i.*,j.*,random()*2-1 from generate_series(1,{scenario["network_size"]}) i, generate_series(1,3) j')
                prep_database.execute_sql()

                time = 0
                memory = 0

                #tf_output = kmeans_tensorflow(points, cluster, CONFIG['iterations'], type)
                #accuracy = evaluate_accuray(tf_output, _, scenario['min'], scenario['max'])

                Create_CSV.append_row(database['csv_file'], [time, memory])
                Helper.remove_files(database['files'], './')


def generate_statement(iterations: int) -> None:
    '''
    This function generates the SQL file.

    :param iterations: The number of iterations in the recursive CTE.
    '''

    with open('./Statement.sql', 'w') as file:
        file.write(STATEMENT.format(iterations))

if __name__ == '__main__':
    main()