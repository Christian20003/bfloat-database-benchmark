import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from Statements import *
import DuckDB
import Umbra
import Postgresql
import LingoDB

csv_header = [
    'Type', 
    'Network_Size', 
    'Data_Size',
    'Statement',
    'Aggregation',
    'Learning_Rate', 
    'Iterations', 
    'Execution', 
    'Heap', 
    'RSS', 
    'Database', 
    'Tensorflow'
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
    'learning_rate': 0.01,
    'databases': [
        duckdb,
        umbra,
        postgresql,
        lingodb
    ],
    'setups': [
        {
            'iterations': 100,
            'network_size': 100,
            'data_size': 150,
            'statements': [{
                'number': 1,
                'statement': STATEMENT_1
            }],
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 100,
            'data_size': 300,
            'statements': [{
                'number': 1,
                'statement': STATEMENT_1
            }],
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 100,
            'data_size': 600,
            'statements': [{
                'number': 1,
                'statement': STATEMENT_1
            }],
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 100,
            'data_size': 1200,
            'statements': [{
                'number': 1,
                'statement': STATEMENT_1
            }],
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 100,
            'data_size': 2400,
            'statements': [{
                'number': 1,
                'statement': STATEMENT_1
            }],
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 100,
            'data_size': 4800,
            'statements': [{
                'number': 1,
                'statement': STATEMENT_1
            }],
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 300,
            'data_size': 150,
            'statements': [{
                'number': 1,
                'statement': STATEMENT_1
            }],
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 300,
            'data_size': 300,
            'statements': [{
                'number': 1,
                'statement': STATEMENT_1
            }],
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 300,
            'data_size': 600,
            'statements': [{
                'number': 1,
                'statement': STATEMENT_1
            }],
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 300,
            'data_size': 1200,
            'statements': [{
                'number': 1,
                'statement': STATEMENT_1
            }],
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 300,
            'data_size': 2400,
            'statements': [{
                'number': 1,
                'statement': STATEMENT_1
            }],
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 300,
            'data_size': 4800,
            'statements': [{
                'number': 1,
                'statement': STATEMENT_1
            }],
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 300,
            'data_size': 4800,
            'statements': [{
                'number': 1,
                'statement': STATEMENT_1
            }],
            'ignore': False
        },
        # Setups with increased iterations
        {
            'iterations': 1,
            'network_size': 300,
            'data_size': 4800,
            'statements': [{
                'number': 2,
                'statement': STATEMENT_2
            }],
            'ignore': False
        },
        {
            'iterations': 2,
            'network_size': 300,
            'data_size': 4800,
            'statements': [{
                'number': 2,
                'statement': STATEMENT_2
            }],
            'ignore': False
        },
        {
            'iterations': 3,
            'network_size': 300,
            'data_size': 4800,
            'statements': [{
                'number': 2,
                'statement': STATEMENT_2
            }],
            'ignore': False
        },
        {
            'iterations': 4,
            'network_size': 300,
            'data_size': 4800,
            'statements': [{
                'number': 2,
                'statement': STATEMENT_2
            }],
            'ignore': False
        },
        {
            'iterations': 5,
            'network_size': 300,
            'data_size': 4800,
            'statements': [{
                'number': 2,
                'statement': STATEMENT_2
            }],
            'ignore': False
        },
        {
            'iterations': 6,
            'network_size': 300,
            'data_size': 4800,
            'statements': [{
                'number': 2,
                'statement': STATEMENT_2
            }],
            'ignore': False
        },
        {
            'iterations': 7,
            'network_size': 300,
            'data_size': 4800,
            'statements': [{
                'number': 2,
                'statement': STATEMENT_2
            }],
            'ignore': False
        },
        {
            'iterations': 8,
            'network_size': 300,
            'data_size': 4800,
            'statements': [{
                'number': 2,
                'statement': STATEMENT_2
            }],
            'ignore': False
        },
        {
            'iterations': 9,
            'network_size': 300,
            'data_size': 4800,
            'statements': [{
                'number': 2,
                'statement': STATEMENT_2
            }],
            'ignore': False
        },
        {
            'iterations': 10,
            'network_size': 300,
            'data_size': 4800,
            'statements': [{
                'number': 2,
                'statement': STATEMENT_2
            }],
            'ignore': False
        },
        {
            'iterations': 10,
            'network_size': 300,
            'data_size': 4800,
            'statements': [{
                'number': 1,
                'statement': STATEMENT_1
            }],
            'ignore': False
        }
    ] 
}
