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
    'Relation-Size'
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
    'databases': [
        duckdb,
        umbra,
        postgresql,
        lingodb
    ],
    'setups': [
        {
            'dimension_1': 10,
            'dimension_2': 10,
            'dimension_3': 10,
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
            ],
            'ignore': False
        },
        {
            'dimension_1': 100,
            'dimension_2': 100,
            'dimension_3': 100,
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
            ],
            'ignore': False
        },
        {
            'dimension_1': 200,
            'dimension_2': 200,
            'dimension_3': 200,
            'statements': [
                {
                    'number': 2,
                    'statement': STATEMENT_2
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 300,
            'dimension_2': 300,
            'dimension_3': 300,
            'statements': [
                {
                    'number': 2,
                    'statement': STATEMENT_2
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 400,
            'dimension_2': 400,
            'dimension_3': 400,
            'statements': [
                {
                    'number': 2,
                    'statement': STATEMENT_2
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 1000,
            'dimension_2': 1000,
            'dimension_3': 1000,
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
            ],
            'ignore': False
        },
        {
            'dimension_1': 10000,
            'dimension_2': 10000,
            'dimension_3': 10000,
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
            ],
            'ignore': False
        },
        {
            'dimension_1': 100000,
            'dimension_2': 100000,
            'dimension_3': 100000,
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
            ],
            'ignore': False
        }
    ]
}
