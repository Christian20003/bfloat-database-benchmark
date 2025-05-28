import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from Statements import *
import Settings
import DuckDB
import Umbra
import Postgresql
import LingoDB

DUCK_DB_DATABASE_FILE = 'regression.db'
UMBRA_DB_DATABASE_FILE = 'regression'
POSTGRES_DB_DATABASE_FILE = 'regression'
STATEMENT_FILE = 'Statement.sql'

csv_header = {
    'Type',
    'Aggregation',
    'Parameters',
    'Points', 
    'Iterations', 
    'Execution', 
    'Heap', 
    'RSS',
    'Database-MAE',
    'Tensorflow-MAE',
    'Database-MSE',
    'Tensorflow-MSE',
    'Database-MAPE',
    'Tensorflow-MAPE',
    'Database-sMAPE',
    'Tensorflow-sMAPE',
    'Database-MPE', 
    'Tensorflow-MPE', 
    'Database', 
    'Tensorflow', 
    'Truth'
}

duckdb = DuckDB.DUCKDB
duckdb['csv_header'] = csv_header
umbra = Umbra.UMBRA
umbra['csv_header'] = csv_header
postgresql = Postgresql.POSTGRESQL
postgresql['csv_header'] = csv_header
lingodb = LingoDB.LINGODB
lingodb['csv_header'] = csv_header

CONFIG = {
    'param_value': 0.75,
    'param_start': 10,
    'max_points': 1000000000,
    'databases': [
        duckdb,
        umbra,
        postgresql,
        lingodb
    ],
    'setups': [
        # setups with increasing amount of points
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 10,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 100,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 1000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 10000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 100000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 1000000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 2500000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 5000000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 7500000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 10000000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 25000000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 50000000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 75000000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 100000000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 250000000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 500000000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 750000000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'points_amount': 1000000000,
            'params_amount': 2,
            'ignore': False,
            'use_max_points': True,
            'tensorflow': False
        },
        # setups with increasing amount of parameters
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_3_PARAM,
            'points_amount': 10000000,
            'params_amount': 3,
            'ignore': False,
            'use_max_points': False,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_4_PARAM,
            'points_amount': 10000000,
            'params_amount': 4,
            'ignore': False,
            'use_max_points': False,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_5_PARAM,
            'points_amount': 10000000,
            'params_amount': 5,
            'ignore': False,
            'use_max_points': False,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_6_PARAM,
            'points_amount': 10000000,
            'params_amount': 6,
            'ignore': False,
            'use_max_points': False,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_7_PARAM,
            'points_amount': 10000000,
            'params_amount': 7,
            'ignore': False,
            'use_max_points': False,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_8_PARAM,
            'points_amount': 10000000,
            'params_amount': 8,
            'ignore': False,
            'use_max_points': False,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_9_PARAM,
            'points_amount': 100000000,
            'params_amount': 9,
            'ignore': False,
            'use_max_points': False,
            'tensorflow': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_10_PARAM,
            'points_amount': 100000000,
            'params_amount': 10,
            'ignore': False,
            'use_max_points': False,
            'tensorflow': True
        }
    ] 
}