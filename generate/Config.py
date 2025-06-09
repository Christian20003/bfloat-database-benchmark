import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

import DuckDB
import Umbra
import Statements

HEADER = [
    'Type',
    'Entries',
    'Array',
    'Heaptrack-RSS',
    'Psutil-RSS',
    'Psutil-VMS'
]

duckdb = DuckDB.DUCKDB
umbra = Umbra.UMBRA
duckdb['csv_header'] = HEADER
umbra['csv_header'] = HEADER

CONFIG = {
    'databases': [
        duckdb,
        umbra
    ],
    'setups': [
        {
            'entries': 1000,
            'statements': [
                {
                    'statement_duckdb': Statements.STATEMENT_1,
                    'statement_umbra': Statements.STATEMENT_1,
                    'array': False
                },
                {
                    'statement_duckdb': Statements.STATEMENT_2_D,
                    'statement_umbra': Statements.STATEMENT_2_U,
                    'array': True
                }
            ]
        },
        {
            'entries': 10000,
            'statements': [
                {
                    'statement_duckdb': Statements.STATEMENT_1,
                    'statement_umbra': Statements.STATEMENT_1,
                    'array': False
                },
                {
                    'statement_duckdb': Statements.STATEMENT_2_D,
                    'statement_umbra': Statements.STATEMENT_2_U,
                    'array': True
                }
            ]
        },
        {
            'entries': 100000,
            'statements': [
                {
                    'statement_duckdb': Statements.STATEMENT_1,
                    'statement_umbra': Statements.STATEMENT_1,
                    'array': False
                },
                {
                    'statement_duckdb': Statements.STATEMENT_2_D,
                    'statement_umbra': Statements.STATEMENT_2_U,
                    'array': True
                }
            ]
        },
        {
            'entries': 1000000,
            'statements': [
                {
                    'statement_duckdb': Statements.STATEMENT_1,
                    'statement_umbra': Statements.STATEMENT_1,
                    'array': False
                },
                {
                    'statement_duckdb': Statements.STATEMENT_2_D,
                    'statement_umbra': Statements.STATEMENT_2_U,
                    'array': True
                }
            ]
        },
        {
            'entries': 10000000,
            'statements': [
                {
                    'statement_duckdb': Statements.STATEMENT_1,
                    'statement_umbra': Statements.STATEMENT_1,
                    'array': False
                },
                {
                    'statement_duckdb': Statements.STATEMENT_2_D,
                    'statement_umbra': Statements.STATEMENT_2_U,
                    'array': True
                }
            ]
        },
        {
            'entries': 100000000,
            'statements': [
                {
                    'statement_duckdb': Statements.STATEMENT_1,
                    'statement_umbra': Statements.STATEMENT_1,
                    'array': False
                },
                {
                    'statement_duckdb': Statements.STATEMENT_2_D,
                    'statement_umbra': Statements.STATEMENT_2_U,
                    'array': True
                }
            ]
        },
        {
            'entries': 1000000000,
            'statements': [
                {
                    'statement_duckdb': Statements.STATEMENT_1,
                    'statement_umbra': Statements.STATEMENT_1,
                    'array': False
                },
                {
                    'statement_duckdb': Statements.STATEMENT_2_D,
                    'statement_umbra': Statements.STATEMENT_2_U,
                    'array': True
                }
            ]
        }
    ]
}