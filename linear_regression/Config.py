import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

import Settings

DUCK_DB_DATABASE_FILE = 'regression.db'
UMBRA_DB_DATABASE_FILE = 'regression'
POSTGRES_DB_DATABASE_FILE = 'regression'
STATEMENT_FILE = 'Statement.sql'

CONFIG = {
    'slope': 0.75,
    'intercept': -2.582,
    'max_points': 1000000000,
    'databases': [
        {
            'name': 'duckdb',
            'create_csv': True,
            'ignore': False,
            'csv_file': 'DuckDB_Regression_Results.csv',
            'csv_header': [
                'Type', 
                'Points', 
                'Iterations', 
                'Execution', 
                'Heap', 
                'RSS',
                'DuckDB-MAE',
                'Tensorflow-MAE',
                'DuckDB-MSE',
                'Tensorflow-MSE',
                'DuckDB-MAPE',
                'Tensorflow-MAPE',
                'DuckDB-sMAPE',
                'Tensorflow-sMAPE',
                'DuckDB-MPE', 
                'Tensorflow-MPE', 
                'DuckDB', 
                'Tensorflow', 
                'Truth'
            ],
            'files': [f'./{DUCK_DB_DATABASE_FILE}'],
            'execution': f'{Settings.DUCK_DB_PATH} {DUCK_DB_DATABASE_FILE}',
            'execution-bench': f'{Settings.DUCK_DB_PATH} -json -f {STATEMENT_FILE} {DUCK_DB_DATABASE_FILE}',
            'start-sql': [],
            'end-sql': ['.exit'],
            'types': ['float', 'bfloat'],
            'aggregations': ['standard', 'kahan']
        },
        {
            'name': 'umbra',
            'create_csv': True,
            'ignore': True,
            'csv_file': 'Umbra_Regression_Results.csv',
            'csv_header': [
                'Type', 
                'Points',  
                'Iterations',  
                'Execution', 
                'Heap', 
                'RSS', 
                'MAPE', 
                'Umbra', 
                'Tensorflow',
                'Truth'
                ],
            'files': [
                f'./{UMBRA_DB_DATABASE_FILE}', 
                f'./{UMBRA_DB_DATABASE_FILE}.0_0.data', 
                f'./{UMBRA_DB_DATABASE_FILE}.0_0.sample', 
                f'./{UMBRA_DB_DATABASE_FILE}.0_0s.data', 
                f'./{UMBRA_DB_DATABASE_FILE}.lock', 
                f'./{UMBRA_DB_DATABASE_FILE}.pages', 
                f'./{UMBRA_DB_DATABASE_FILE}.wal'
                ],
            'execution': f'{Settings.UMBRA_DB_PATH} -createdb {UMBRA_DB_DATABASE_FILE}',
            'execution-bench': f'{Settings.UMBRA_DB_PATH} {UMBRA_DB_DATABASE_FILE} {STATEMENT_FILE}',
            'start-sql': [],
            'end-sql': ['\q;'],
            'types': ['float']
        },
        {
            'name': 'postgres',
            'create_csv': True,
            'ignore': True,
            'csv_file': 'Postgres_Regression_Results.csv',
            'csv_header': [
                'Type', 
                'Points', 
                'Iterations', 
                'Execution', 
                'Heap', 
                'RSS', 
                'Loss', 
                'Postgres', 
                'Tensorflow',
                'Truth'
                ],
            'files': [],
            'prep': [
                f'{Settings.POSTGRESQL_DB_PATH}initdb -D {Settings.POSTGRESQL_DIR} -U {Settings.POSTGRESQL_USERNAME}', 
                f'{Settings.POSTGRESQL_DB_PATH}pg_ctl -D {Settings.POSTGRESQL_DIR} start', 
                f'{Settings.POSTGRESQL_DB_PATH}createdb -h {Settings.POSTGRESQL_HOST} -p {Settings.POSTGRESQL_PORT} {POSTGRES_DB_DATABASE_FILE} -U {Settings.POSTGRESQL_USERNAME}', 
                f'{Settings.POSTGRESQL_DB_PATH}pg_ctl -D {Settings.POSTGRESQL_DIR} stop'],
            'execution': f'{Settings.POSTGRESQL_DB_PATH}psql -h {Settings.POSTGRESQL_HOST} -p {Settings.POSTGRESQL_PORT} -U {Settings.POSTGRESQL_USERNAME} -d {POSTGRES_DB_DATABASE_FILE}',
            'execution-bench': f'{Settings.POSTGRESQL_DB_PATH}psql -h {Settings.POSTGRESQL_HOST} -p {Settings.POSTGRESQL_PORT} -U {Settings.POSTGRESQL_USERNAME} -d {POSTGRES_DB_DATABASE_FILE} -f {STATEMENT_FILE}',
            'start-sql': [],
            'end-sql': [],
            'types': ['float']
        }
    ],
    'setups': [
        # setups with increasing amount of points
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 10,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 100,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 1000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 10000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 100000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 1000000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 2500000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 5000000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 7500000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 10000000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 25000000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 50000000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 75000000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 100000000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 250000000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 500000000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 750000000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 1000000000,
            'ignore': False
        },
        # setups with increasing amount of iterations
        {
            'iterations': 10,
            'lr': 0.05,
            'p_amount': 100000000,
            'ignore': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'p_amount': 100000000,
            'ignore': False
        },
        {
            'iterations': 1000,
            'lr': 0.05,
            'p_amount': 100000000,
            'ignore': False
        },
    ] 
}

STATEMENT = '''
WITH RECURSIVE gd (idx, a, b) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b) AS (
    SELECT idx, a - {} * {}(2 * x * (a * x + b - y)), b - {} * {}(2 * (a * x + b - y))
    FROM current_gd, points 
    GROUP BY idx, a, b
  )
  SELECT idx + 1, a, b
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd WHERE idx = {};
'''