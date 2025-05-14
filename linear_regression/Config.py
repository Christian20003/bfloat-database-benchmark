import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

import Settings

DUCK_DB_DATABASE_FILE = 'regression.db'
UMBRA_DB_DATABASE_FILE = 'regression'
POSTGRES_DB_DATABASE_FILE = 'regression'
STATEMENT_FILE = 'Statement.sql'

STATEMENT_2_PARAM = '''
WITH RECURSIVE gd (idx, a, b) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b) AS (
    SELECT idx, a - {} * {}(2 * x1 * (a * x1 + b - y)), b - {} * {}(2 * (a * x1 + b - y))
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

STATEMENT_3_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c) AS (
    SELECT idx, 
            a - {} * {}(2 * pow(x2, 2) * (a * pow(x2, 2) + b * x1 + c - y)), 
            b - {} * {}(2 * x1 * (a * pow(x2, 2) + b * x1 + c - y)), 
            c - {} * {}(2 * (a * pow(x2, 2) + b * x1 + c - y))
    FROM current_gd, points 
    GROUP BY idx, a, b, c
  )
  SELECT idx + 1, a, b, c
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd WHERE idx = {};
'''

STATEMENT_4_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c, d) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c, d) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c, d) AS (
    SELECT idx, 
            a - {} * {}(2 * pow(x3, 3) * (a * pow(x3, 3) + b * pow(x2, 2) + c * x1 + d - y)), 
            b - {} * {} (2 * pow(x2, 2) * (a * pow(x3, 3) + b * pow(x2, 2) + c * x1 + d - y)), 
            c - {} * {}(2 * x1 * (a * pow(x3, 3) + b * pow(x2, 2) + c * x1 + d - y)), 
            d - {} * {}(2 * (a * pow(x3, 3) + b * pow(x2, 2) + c * x1 + d - y))
    FROM current_gd, points 
    GROUP BY idx, a, b, c, d
  )
  SELECT idx + 1, a, b, c, d
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd WHERE idx = {};
'''

STATEMENT_5_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c, d, e) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c, d, e) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c, d, e) AS (
    SELECT idx, 
            a - {} * {}(2 * pow(x4, 4) * (a * pow(x4, 4) + b * pow(x3, 3) + c * pow(x2, 2) + d * x1 + e - y)), 
            b - {} * {}(2 * pow(x3, 3) * (a * pow(x4, 4) + b * pow(x3, 3) + c * pow(x2, 2) + d * x1 + e - y)), 
            c - {} * {} (2 * pow(x2, 2) * (a * pow(x4, 4) + b * pow(x3, 3) + c * pow(x2, 2) + d * x1 + e - y)), 
            d - {} * {}(2 * x1 * (a * pow(x4, 4) + b * pow(x3, 3) + c * pow(x2, 2) + d * x1 + e - y)), 
            e - {} * {}(2 * (a * pow(x4, 4) + b * pow(x3, 3) + c * pow(x2, 2) + d * x1 + e - y))
    FROM current_gd, points 
    GROUP BY idx, a, b, c, d, e
  )
  SELECT idx + 1, a, b, c, d, e
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd WHERE idx = {};
'''

STATEMENT_6_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c, d, e, f) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c, d, e, f) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c, d, e, f) AS (
    SELECT idx, 
           a - {} * {}(2 * pow(x5, 5) * (a * pow(x5, 5) + b * pow(x4, 4) + c * pow(x3, 3) + d * pow(x2, 2) + e * x1 + f - y)), 
           b - {} * {}(2 * pow(x4, 4) * (a * pow(x5, 5) + b * pow(x4, 4) + c * pow(x3, 3) + d * pow(x2, 2) + e * x1 + f - y)), 
           c - {} * {}(2 * pow(x3, 3) * (a * pow(x5, 5) + b * pow(x4, 4) + c * pow(x3, 3) + d * pow(x2, 2) + e * x1 + f - y)), 
           d - {} * {}(2 * pow(x2, 2) * (a * pow(x5, 5) + b * pow(x4, 4) + c * pow(x3, 3) + d * pow(x2, 2) + e * x1 + f - y)), 
           e - {} * {}(2 * x1 * (a * pow(x5, 5) + b * pow(x4, 4) + c * pow(x3, 3) + d * pow(x2, 2) + e * x1 + f - y)), 
           f - {} * {}(2 * (a * pow(x5, 5) + b * pow(x4, 4) + c * pow(x3, 3) + d * pow(x2, 2) + e * x1 + f - y))
    FROM current_gd, points 
    GROUP BY idx, a, b, c, d, e, f
  )
  SELECT idx + 1, a, b, c, d, e, f
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd WHERE idx = {};
'''

STATEMENT_7_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c, d, e, f, g) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c, d, e, f, g) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c, d, e, f, g) AS (
    SELECT idx, a - {} * {}(2 * pow(x6, 6) * (a * pow(x6, 6) + b * pow(x5, 5) + c * pow(x4, 4) + d * pow(x3, 3) + e * pow(x2, 2) + f * x1 + g - y)), 
           b - {} * {}(2 * pow(x5, 5) * (a * pow(x6, 6) + b * pow(x5, 5) + c * pow(x4, 4) + d * pow(x3, 3) + e * pow(x2, 2) + f * x1 + g - y)), 
           c - {} * {}(2 * pow(x4, 4) * (a * pow(x6, 6) + b * pow(x5, 5) + c * pow(x4, 4) + d * pow(x3, 3) + e * pow(x2, 2) + f * x1 + g - y)), 
           d - {} * {}(2 * pow(x3, 3) * (a * pow(x6, 6) + b * pow(x5, 5) + c * pow(x4, 4) + d * pow(x3, 3) + e * pow(x2, 2) + f * x1 + g - y)), 
           e - {} * {}(2 * pow(x2, 2) * (a * pow(x6, 6) + b * pow(x5, 5) + c * pow(x4, 4) + d * pow(x3, 3) + e * pow(x2, 2) + f * x1 + g - y)),
           f - {} * {}(2 * x1 * (a * pow(x6, 6) + b * pow(x5, 5) + c * pow(x4, 4) + d * pow(x3, 3) + e * pow(x2, 2) + f * x1 + g - y)),
           g - {} * {}(2 * (a * pow(x6, 6) + b * pow(x5, 5) + c * pow(x4, 4) + d * pow(x3, 3) + e * pow(x2, 2) + f * x1 + g - y))
    FROM current_gd, points 
    GROUP BY idx, a, b, c, d, e, f, g
  )
  SELECT idx + 1, a, b, c, d, e, f, g
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd WHERE idx = {};
'''

STATEMENT_8_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c, d, e, f, g, h) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c, d, e, f, g, h) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c, d, e, f, g, h) AS (
    SELECT idx, a - {} * {}(2 * pow(x7, 7) * (a * pow(x7, 7) + b * pow(x6, 6) + c * pow(x5, 5) + d * pow(x4, 4) + e * pow(x3, 3) + f * pow(x2, 2) + g * x1 + h - y)), 
           b - {} * {}(2 * pow(x6, 6) * (a * pow(x7, 7) + b * pow(x6, 6) + c * pow(x5, 5) + d * pow(x4, 4) + e * pow(x3, 3) + f * pow(x2, 2) + g * x1 + h - y)), 
           c - {} * {}(2 * pow(x5, 5) * (a * pow(x7, 7) + b * pow(x6, 6) + c * pow(x5, 5) + d * pow(x4, 4) + e * pow(x3, 3) + f * pow(x2, 2) + g * x1 + h - y)), 
           d - {} * {}(2 * pow(x4, 4) * (a * pow(x7, 7) + b * pow(x6, 6) + c * pow(x5, 5) + d * pow(x4, 4) + e * pow(x3, 3) + f * pow(x2, 2) + g * x1 + h - y)), 
           e - {} * {}(2 * pow(x3, 3) * (a * pow(x7, 7) + b * pow(x6, 6) + c * pow(x5, 5) + d * pow(x4, 4) + e * pow(x3, 3) + f * pow(x2, 2) + g * x1 + h - y)), 
           f - {} * {}(2 * pow(x2, 2) * (a * pow(x7, 7) + b * pow(x6, 6) + c * pow(x5, 5) + d * pow(x4, 4) + e * pow(x3, 3) + f * pow(x2, 2) + g * x1 + h - y)), 
           g - {} * {}(2 * x1 * (a * pow(x7, 7) + b * pow(x6, 6) + c * pow(x5, 5) + d * pow(x4, 4) + e * pow(x3, 3) + f * pow(x2, 2) + g * x1 + h - y)),
           h - {} * {}(2 * (a * pow(x7, 7) + b * pow(x6, 6) + c * pow(x5, 5) + d * pow(x4, 4) + e * pow(x3, 3) + f * pow(x2, 2) + g * x1 + h - y))
    FROM current_gd, points
    GROUP BY idx, a, b, c, d, e, f, g, h
  )
  SELECT idx + 1, a, b, c, d, e, f, g, h
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd WHERE idx = {};
'''

STATEMENT_9_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c, d, e, f, g, h, i) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c, d, e, f, g, h, i) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c, d, e, f, g, h, i) AS (
    SELECT idx, a - {} * {}(2 * pow(x8, 8) * (a * pow(x8, 8) + b * pow(x7, 7) + c * pow(x6, 6) + d * pow(x5, 5) + e * pow(x4, 4) + f * pow(x3, 3) + g * pow(x2, 2) + h * x1 + i - y)), 
           b - {} * {}(2 * pow(x7, 7) * (a * pow(x8, 8) + b * pow(x7, 7) + c * pow(x6, 6) + d * pow(x5, 5) + e * pow(x4, 4) + f * pow(x3, 3) + g * pow(x2, 2) + h * x1 + i - y)), 
           c - {} * {}(2 * pow(x6, 6) * (a * pow(x8, 8) + b * pow(x7, 7) + c * pow(x6, 6) + d * pow(x5, 5) + e * pow(x4, 4) + f * pow(x3, 3) + g * pow(x2, 2) + h * x1 + i - y)), 
           d - {} * {}(2 * pow(x5, 5) * (a * pow(x8, 8) + b * pow(x7, 7) + c * pow(x6, 6) + d * pow(x5, 5) + e * pow(x4, 4) + f * pow(x3, 3) + g * pow(x2, 2) + h * x1 + i - y)), 
           e - {} * {}(2 * pow(x4, 4) * (a * pow(x8, 8) + b * pow(x7, 7) + c * pow(x6, 6) + d * pow(x5, 5) + e * pow(x4, 4) + f * pow(x3, 3) + g * pow(x2, 2) + h * x1 + i - y)), 
           f - {} * {}(2 * pow(x3, 3) * (a * pow(x8, 8) + b * pow(x7, 7) + c * pow(x6, 6) + d * pow(x5, 5) + e * pow(x4, 4) + f * pow(x3, 3) + g * pow(x2, 2) + h * x1 + i - y)), 
           g - {} * {}(2 * pow(x2, 2) * (a * pow(x8, 8) + b * pow(x7, 7) + c * pow(x6, 6) + d * pow(x5, 5) + e * pow(x4, 4) + f * pow(x3, 3) + g * pow(x2, 2) + h * x1 + i - y)),
           h - {} * {}(2 * x1 * (a * pow(x8, 8) + b * pow(x7, 7) + c * pow(x6, 6) + d * pow(x5, 5) + e * pow(x4, 4) + f * pow(x3, 3) + g * pow(x2, 2) + h * x1 + i - y)),
           i - {} * {}(2 * (a * pow(x8, 8) + b * pow(x7, 7) + c * pow(x6, 6) + d * pow(x5, 5) + e * pow(x4, 4) + f * pow(x3, 3) + g * pow(x2, 2) + h * x1 + i - y))
    FROM current_gd, points
    GROUP BY idx, a, b, c, d, e, f, g, h, i
  )
  SELECT idx + 1, a, b, c, d, e, f, g, h, i
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd WHERE idx = {};
'''

STATEMENT_10_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c, d, e, f, g, h, i, j) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c, d, e, f, g, h, i, j) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c, d, e, f, g, h, i, j) AS (
    SELECT idx, a - {} * {}(2 * pow(x9, 9) * (a * pow(x9, 9) + b * pow(x8, 8) + c * pow(x7, 7) + d * pow(x6, 6) + e * pow(x5, 5) + f * pow(x4, 4) + g * pow(x3, 3) + h * pow(x2, 2) + i * x1 + j - y)), 
           b - {} * {}(2 * pow(x8, 8) * (a * pow(x9, 9) + b * pow(x8, 8) + c * pow(x7, 7) + d * pow(x6, 6) + e * pow(x5, 5) + f * pow(x4, 4) + g * pow(x3, 3) + h * pow(x2, 2) + i * x1 + j - y)), 
           c - {} * {}(2 * pow(x7, 7) * (a * pow(x9, 9) + b * pow(x8, 8) + c * pow(x7, 7) + d * pow(x6, 6) + e * pow(x5, 5) + f * pow(x4, 4) + g * pow(x3, 3) + h * pow(x2, 2) + i * x1 + j - y)), 
           d - {} * {}(2 * pow(x6, 6) * (a * pow(x9, 9) + b * pow(x8, 8) + c * pow(x7, 7) + d * pow(x6, 6) + e * pow(x5, 5) + f * pow(x4, 4) + g * pow(x3, 3) + h * pow(x2, 2) + i * x1 + j - y)), 
           e - {} * {}(2 * pow(x5, 5) * (a * pow(x9, 9) + b * pow(x8, 8) + c * pow(x7, 7) + d * pow(x6, 6) + e * pow(x5, 5) + f * pow(x4, 4) + g * pow(x3, 3) + h * pow(x2, 2) + i * x1 + j - y)), 
           f - {} * {}(2 * pow(x4, 4) * (a * pow(x9, 9) + b * pow(x8, 8) + c * pow(x7, 7) + d * pow(x6, 6) + e * pow(x5, 5) + f * pow(x4, 4) + g * pow(x3, 3) + h * pow(x2, 2) + i * x1 + j - y)), 
           g - {} * {}(2 * pow(x3, 3) * (a * pow(x9, 9) + b * pow(x8, 8) + c * pow(x7, 7) + d * pow(x6, 6) + e * pow(x5, 5) + f * pow(x4, 4) + g * pow(x3, 3) + h * pow(x2, 2) + i * x1 + j - y)), 
           h - {} * {}(2 * pow(x2, 2) * (a * pow(x9, 9) + b * pow(x8, 8) + c * pow(x7, 7) + d * pow(x6, 6) + e * pow(x5, 5) + f * pow(x4, 4) + g * pow(x3, 3) + h * pow(x2, 2) + i * x1 + j - y)), 
           i - {} * {}(2 * x1 * (a * pow(x9, 9) + b * pow(x8, 8) + c * pow(x7, 7) + d * pow(x6, 6) + e * pow(x5, 5) + f * pow(x4, 4) + g * pow(x3, 3) + h * pow(x2, 2) + i * x1 + j - y)),
           j - {} * {}(2 * (a * pow(x9, 9) + b * pow(x8, 8) + c * pow(x7, 7) + d * pow(x6, 6) + e * pow(x5, 5) + f * pow(x4, 4) + g * pow(x3, 3) + h * pow(x2, 2) + i * x1 + j - y))
    FROM current_gd, points
    GROUP BY idx, a, b, c, d, e, f, g, h, i, j
  )
  SELECT idx + 1, a, b, c, d, e, f, g, h, i, j
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd WHERE idx = {};
'''

CONFIG = {
    'param_value': 1,
    'param_start': 10,
    'max_points': 1000000000,
    'databases': [
        {
            'name': 'duckdb',
            'create_csv': True,
            'ignore': False,
            'csv_file': 'DuckDB_Regression_Results.csv',
            'csv_header': [
                'Type',
                'Aggregation',
                'Parameters',
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
            'types': ['double', 'float'],
            'aggregations': ['standard']
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
            'statement': STATEMENT_2_PARAM,
            'p_amount': 10,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_3_PARAM,
            'p_amount': 10,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_4_PARAM,
            'p_amount': 10,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_5_PARAM,
            'p_amount': 10,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_6_PARAM,
            'p_amount': 10,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_7_PARAM,
            'p_amount': 10,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': False
        },




        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 100,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 1000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 10000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 100000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 1000000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 2500000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 5000000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 7500000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 10000000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 25000000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 50000000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 75000000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 100000000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 250000000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 500000000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 750000000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_2_PARAM,
            'p_amount': 1000000000,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
        },
        # setups with increasing amount of parameters
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_3_PARAM,
            'p_amount': 100000,
            'param_amount': 3,
            'ignore': True,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_4_PARAM,
            'p_amount': 100000,
            'param_amount': 4,
            'ignore': True,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_5_PARAM,
            'p_amount': 100000,
            'param_amount': 5,
            'ignore': True,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_6_PARAM,
            'p_amount': 100000,
            'param_amount': 6,
            'ignore': True,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_7_PARAM,
            'p_amount': 100000,
            'param_amount': 7,
            'ignore': True,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_8_PARAM,
            'p_amount': 100000,
            'param_amount': 8,
            'ignore': True,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_9_PARAM,
            'p_amount': 1000000,
            'param_amount': 9,
            'ignore': True,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_10_PARAM,
            'p_amount': 1000000,
            'param_amount': 10,
            'ignore': True,
            'use_max_points': False
        }
    ] 
}