import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from Statements import *
import DuckDB
import Umbra
import Postgresql
import LingoDB

'''
This file contains the configuration for gradient descent experiment.
Most of the settings can be modified, without changing the code which executes the actual benchmark.
This does not include: 
    - Extending with further databases
    - Extending the CSV file header
    - Extending with further SQL statements
All of these options can be done, but don't be surprised if an unexpected error occurs. Therefore, it
is highly recommended to check the code before.
'''

csv_header = [
    'Type',
    'Aggregation',
    'Parameters',
    'Points', 
    'Iterations', 
    'Execution', 
    'Memory', 
    'Relation-Size',
    'MAPE'
]

duckdb = DuckDB.DUCKDB
duckdb['csv_header'] = csv_header
umbra = Umbra.UMBRA
umbra['csv_header'] = csv_header
postgresql = Postgresql.POSTGRESQL
postgresql['csv_header'] = csv_header
lingodb = LingoDB.LINGODB
lingodb['csv_header'] = csv_header

CONFIG = {
    'memory_trials': 10,
    'memory_average': True,
    'param_value': 0.75,
    'param_start': 10,
    'databases': [
        duckdb,
        umbra,
        postgresql,
        lingodb
    ],
    'setups': [
        # setups with increasing amount of points
        {
            # Number of iterations
            'iterations': 20,
            # Learning rate
            'lr': 0.05,
            # The SQL statement to be executed
            'statement': STATEMENT_2_PARAM,
            # The amount of data points
            'points_amount': 10,
            # The amount of parameters (MUST BE COMPATIBLE WITH THE STATEMENT)
            'params_amount': 2,
            # Whether to ignore this setup or not
            'ignore': False
        },
        {
            'iterations': 20,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 1000,
            'params_amount': 2,
            'ignore': False
        },
        {
            'iterations': 20,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 100000,
            'params_amount': 2,
            'ignore': False
        },
        {
            'iterations': 20,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 10000000,
            'params_amount': 2,
            'ignore': False
        },
        {
            'iterations': 20,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 1000000000,
            'params_amount': 2,
            'ignore': False
        },
        # setups with increasing amount of parameters
        {
            'iterations': 20,
            'lr': 0.05,
            'statement': STATEMENT_4_PARAM,
            'points_amount': 10000000,
            'params_amount': 4,
            'ignore': False
        },
        {
            'iterations': 20,
            'lr': 0.05,
            'statement': STATEMENT_6_PARAM,
            'points_amount': 10000000,
            'params_amount': 6,
            'ignore': False
        },
        {
            'iterations': 20,
            'lr': 0.05,
            'statement': STATEMENT_8_PARAM,
            'points_amount': 10000000,
            'params_amount': 8,
            'ignore': False
        },
        {
            'iterations': 20,
            'lr': 0.05,
            'statement': STATEMENT_10_PARAM,
            'points_amount': 10000000,
            'params_amount': 10,
            'ignore': False
        }
    ] 
}