import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from Statements import *
import DuckDB
import Umbra
import LingoDB

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
    'learning_rate': 0.01,
    'databases': [
        duckdb,
        umbra,
        lingodb
    ],
    'setups': [
        # Setups with increased data size
        {
            'iterations': 10,
            'network_size': 300,
            'data_size': 150,
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
            'data_size': 300,
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
            'data_size': 600,
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
        # Setups with increased network size
        {
            'iterations': 10,
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
            'iterations': 10,
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
            'iterations': 10,
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
