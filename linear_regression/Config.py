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
    'Parameters',
    'Points', 
    'Iterations', 
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
            'iterations': 20,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 10,
            'params_amount': 2,
            'ignore': False
        },
        {
            'iterations': 20,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 100,
            'params_amount': 2,
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
            'points_amount': 10000,
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
            'points_amount': 1000000,
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
            'points_amount': 100000000,
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
            'statement': STATEMENT_3_PARAM,
            'points_amount': 10000000,
            'params_amount': 3,
            'ignore': False
        },
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
            'statement': STATEMENT_5_PARAM,
            'points_amount': 10000000,
            'params_amount': 5,
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
            'statement': STATEMENT_7_PARAM,
            'points_amount': 10000000,
            'params_amount': 7,
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
            'statement': STATEMENT_9_PARAM,
            'points_amount': 100000000,
            'params_amount': 9,
            'ignore': False
        },
        {
            'iterations': 20,
            'lr': 0.05,
            'statement': STATEMENT_10_PARAM,
            'points_amount': 100000000,
            'params_amount': 10,
            'ignore': False
        }
    ] 
}