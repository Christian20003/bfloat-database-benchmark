import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from Statements import *
import DuckDB
import Umbra
import LingoDB

'''
This file contains the configuration for iris experiment.
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
    'Network_Size', 
    'Data_Size',
    'Learning_Rate', 
    'Iterations', 
    'Execution', 
    'Memory', 
    'Relation-Size', 
    'Accuracy',
]

duckdb = DuckDB.DUCKDB
duckdb['csv_header'] = csv_header
umbra = Umbra.UMBRA
umbra['csv_header'] = csv_header
lingodb = LingoDB.LINGODB
lingodb['csv_header'] = csv_header

CONFIG = {
    'memory_trials': 10,
    'memory_average': True,
    'learning_rate': 0.01,
    'databases': [
        duckdb,
        umbra,
        lingodb
    ],
    'setups': [
        # Setups with increased data size
        {
            # Number of iterations
            'iterations': 20,
            # Number of neurons in the hidden layer
            'network_size': 300,
            # Number of data points
            'data_size': 150,
            'statements': [{
                # Statement id
                'number': 1,
                # The actual statement
                'statement': STATEMENT,
                # The statement to return the learned weights
                'weights': STATEMENT_WEIGHTS
            }],
            # Whether to ignore this setup or not
            'ignore': False
        },
        {
            'iterations': 20,
            'network_size': 300,
            'data_size': 300,
            'statements': [{
                'number': 1,
                'statement': STATEMENT,
                'weights': STATEMENT_WEIGHTS
            }],
            'ignore': False
        },
        {
            'iterations': 20,
            'network_size': 300,
            'data_size': 600,
            'statements': [{
                'number': 1,
                'statement': STATEMENT,
                'weights': STATEMENT_WEIGHTS
            }],
            'ignore': False
        },
        {
            'iterations': 20,
            'network_size': 300,
            'data_size': 1200,
            'statements': [{
                'number': 1,
                'statement': STATEMENT,
                'weights': STATEMENT_WEIGHTS
            }],
            'ignore': False
        },
        # Setups with increased network size
        {
            'iterations': 20,
            'network_size': 100,
            'data_size': 1200,
            'statements': [{
                'number': 1,
                'statement': STATEMENT,
                'weights': STATEMENT_WEIGHTS
            }],
            'ignore': False
        },
        {
            'iterations': 20,
            'network_size': 200,
            'data_size': 1200,
            'statements': [{
                'number': 1,
                'statement': STATEMENT,
                'weights': STATEMENT_WEIGHTS
            }],
            'ignore': False
        },
        {
            'iterations': 20,
            'network_size': 400,
            'data_size': 1200,
            'statements': [{
                'number': 1,
                'statement': STATEMENT,
                'weights': STATEMENT_WEIGHTS
            }],
            'ignore': False
        },
        # Setups with increased iterations
        {
            'iterations': 1,
            'network_size': 300,
            'data_size': 1200,
            'statements': [{
                'number': 1,
                'statement': STATEMENT,
                'weights': STATEMENT_WEIGHTS
            }],
            'ignore': False
        },
        {
            'iterations': 5,
            'network_size': 300,
            'data_size': 1200,
            'statements': [{
                'number': 1,
                'statement': STATEMENT,
                'weights': STATEMENT_WEIGHTS
            }],
            'ignore': False
        },
        {
            'iterations': 10,
            'network_size': 300,
            'data_size': 1200,
            'statements': [{
                'number': 1,
                'statement': STATEMENT,
                'weights': STATEMENT_WEIGHTS
            }],
            'ignore': False
        },
        {
            'iterations': 15,
            'network_size': 300,
            'data_size': 1200,
            'statements': [{
                'number': 1,
                'statement': STATEMENT,
                'weights': STATEMENT_WEIGHTS
            }],
            'ignore': False
        }
    ] 
}
