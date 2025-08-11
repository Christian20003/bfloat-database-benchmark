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
    'Aggregation',
    'Statement', 
    'MatrixA', 
    'MatrixB', 
    'VectorV', 
    'Execution', 
    'Memory', 
    'Relation-Size',
    'MSE'
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
    'databases': [
        duckdb,
        umbra,
        postgresql,
        lingodb
    ],
    'setups': [
        {
            'id': 'first',
            'dimension': 10,
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
            'id': 'second',
            'dimension': 250,
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
            'dimension': 500,
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
            'dimension': 750,
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
        }
    ]
}
