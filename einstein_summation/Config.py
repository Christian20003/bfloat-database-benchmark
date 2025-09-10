import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from Statements import *
import DuckDB
import Umbra
import Postgresql
import LingoDB

'''
This file contains the configuration for Einstein summation experiment.
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
    'Statement', 
    'MatrixA', 
    'MatrixB', 
    'VectorV', 
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
    'databases': [
        duckdb,
        umbra,
        postgresql,
        lingodb
    ],
    'setups': [
        {
            # Used for the name of the data file
            'id': 'first',
            # The dimension of the (square) matrices and vectors
            'dimension': 30,
            # Whether to ignore this setup or not
            'ignore': False,
            # The statements to execute with this setup
            'statements': [
                {
                    # Id of the statement
                    'number': 1,
                    # The actual statement
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ]
        },
        {
            'id': 'second',
            'dimension': 100,
            'ignore': False,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ]
        },
        {
            'id': 'third',
            'dimension': 300,
            'ignore': False,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ]
        },
        {
            'id': 'fourth',
            'dimension': 1000,
            'ignore': False,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ]
        },
        {
            'id': 'fifth',
            'dimension': 3100,
            'ignore': False,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ]
        }
    ]
}
