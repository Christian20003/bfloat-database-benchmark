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
SELECT * FROM gd ORDER BY idx DESC;
'''

STATEMENT_3_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c) AS (
    SELECT idx, 
            a - {} * {}(2 * x2 * (a * x2 + b * x1 + c - y)), 
            b - {} * {}(2 * x1 * (a * x2 + b * x1 + c - y)), 
            c - {} * {}(2 * (a * x2 + b * x1 + c - y))
    FROM current_gd, points 
    GROUP BY idx, a, b, c
  )
  SELECT idx + 1, a, b, c
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd ORDER BY idx DESC;
'''

STATEMENT_4_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c, d) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c, d) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c, d) AS (
    SELECT idx, 
            a - {} * {}(2 * x3 * (a * x3 + b * x2 + c * x1 + d - y)), 
            b - {} * {} (2 * x2 * (a * x3 + b * x2 + c * x1 + d - y)), 
            c - {} * {}(2 * x1 * (a * x3 + b * x2 + c * x1 + d - y)), 
            d - {} * {}(2 * (a * x3 + b * x2 + c * x1 + d - y))
    FROM current_gd, points 
    GROUP BY idx, a, b, c, d
  )
  SELECT idx + 1, a, b, c, d
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd ORDER BY idx DESC;
'''

STATEMENT_5_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c, d, e) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c, d, e) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c, d, e) AS (
    SELECT idx, 
            a - {} * {}(2 * x4 * (a * x4 + b * x3 + c * x2 + d * x1 + e - y)), 
            b - {} * {}(2 * x3 * (a * x4 + b * x3 + c * x2 + d * x1 + e - y)), 
            c - {} * {}(2 * x2 * (a * x4 + b * x3 + c * x2 + d * x1 + e - y)), 
            d - {} * {}(2 * x1 * (a * x4 + b * x3 + c * x2 + d * x1 + e - y)), 
            e - {} * {}(2 * (a * x4 + b * x3 + c * x2 + d * x1 + e - y))
    FROM current_gd, points 
    GROUP BY idx, a, b, c, d, e
  )
  SELECT idx + 1, a, b, c, d, e
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd ORDER BY idx DESC;
'''

STATEMENT_6_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c, d, e, f) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c, d, e, f) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c, d, e, f) AS (
    SELECT idx, 
           a - {} * {}(2 * x5 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
           b - {} * {}(2 * x4 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
           c - {} * {}(2 * x3 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
           d - {} * {}(2 * x2 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
           e - {} * {}(2 * x1 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y)), 
           f - {} * {}(2 * (a * x5 + b * x4 + c * x3 + d * x2 + e * x1 + f - y))
    FROM current_gd, points 
    GROUP BY idx, a, b, c, d, e, f
  )
  SELECT idx + 1, a, b, c, d, e, f
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd ORDER BY idx DESC;
'''

STATEMENT_7_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c, d, e, f, g) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c, d, e, f, g) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c, d, e, f, g) AS (
    SELECT idx, 
           a - {} * {}(2 * x6 * (a * x6 + b * x5 + c * x4 + d * x3 + e * x2 + f * x1 + g - y)), 
           b - {} * {}(2 * x5 * (a * x6 + b * x5 + c * x4 + d * x3 + e * x2 + f * x1 + g - y)), 
           c - {} * {}(2 * x4 * (a * x6 + b * x5 + c * x4 + d * x3 + e * x2 + f * x1 + g - y)), 
           d - {} * {}(2 * x3 * (a * x6 + b * x5 + c * x4 + d * x3 + e * x2 + f * x1 + g - y)), 
           e - {} * {}(2 * x2 * (a * x6 + b * x5 + c * x4 + d * x3 + e * x2 + f * x1 + g - y)),
           f - {} * {}(2 * x1 * (a * x6 + b * x5 + c * x4 + d * x3 + e * x2 + f * x1 + g - y)),
           g - {} * {}(2 * (a * x6 + b * x5 + c * x4 + d * x3 + e * x2 + f * x1 + g - y))
    FROM current_gd, points 
    GROUP BY idx, a, b, c, d, e, f, g
  )
  SELECT idx + 1, a, b, c, d, e, f, g
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd ORDER BY idx DESC;
'''

STATEMENT_8_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c, d, e, f, g, h) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c, d, e, f, g, h) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c, d, e, f, g, h) AS (
    SELECT idx, 
           a - {} * {}(2 * x7 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
           b - {} * {}(2 * x6 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
           c - {} * {}(2 * x5 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
           d - {} * {}(2 * x4 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
           e - {} * {}(2 * x3 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
           f - {} * {}(2 * x2 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)), 
           g - {} * {}(2 * x1 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y)),
           h - {} * {}(2 * (a * x7 + b * x6 + c * x5 + d * x4 + e * x3 + f * x2 + g * x1 + h - y))
    FROM current_gd, points
    GROUP BY idx, a, b, c, d, e, f, g, h
  )
  SELECT idx + 1, a, b, c, d, e, f, g, h
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd ORDER BY idx DESC;
'''

STATEMENT_9_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c, d, e, f, g, h, i) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c, d, e, f, g, h, i) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c, d, e, f, g, h, i) AS (
    SELECT idx, 
           a - {} * {}(2 * x8 * (a * x8 + b * x7 + c * x6 + d * x5 + e * x4 + f * x3 + g * x2 + h * x1 + i - y)), 
           b - {} * {}(2 * x7 * (a * x8 + b * x7 + c * x6 + d * x5 + e * x4 + f * x3 + g * x2 + h * x1 + i - y)), 
           c - {} * {}(2 * x6 * (a * x8 + b * x7 + c * x6 + d * x5 + e * x4 + f * x3 + g * x2 + h * x1 + i - y)), 
           d - {} * {}(2 * x5 * (a * x8 + b * x7 + c * x6 + d * x5 + e * x4 + f * x3 + g * x2 + h * x1 + i - y)), 
           e - {} * {}(2 * x4 * (a * x8 + b * x7 + c * x6 + d * x5 + e * x4 + f * x3 + g * x2 + h * x1 + i - y)), 
           f - {} * {}(2 * x3 * (a * x8 + b * x7 + c * x6 + d * x5 + e * x4 + f * x3 + g * x2 + h * x1 + i - y)), 
           g - {} * {}(2 * x2 * (a * x8 + b * x7 + c * x6 + d * x5 + e * x4 + f * x3 + g * x2 + h * x1 + i - y)),
           h - {} * {}(2 * x1 * (a * x8 + b * x7 + c * x6 + d * x5 + e * x4 + f * x3 + g * x2 + h * x1 + i - y)),
           i - {} * {}(2 * (a * x8 + b * x7 + c * x6 + d * x5 + e * x4 + f * x3 + g * x2 + h * x1 + i - y))
    FROM current_gd, points
    GROUP BY idx, a, b, c, d, e, f, g, h, i
  )
  SELECT idx + 1, a, b, c, d, e, f, g, h, i
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd ORDER BY idx DESC;
'''

STATEMENT_10_PARAM = '''
WITH RECURSIVE gd (idx, a, b, c, d, e, f, g, h, i, j) AS (
SELECT * FROM gd_start
UNION ALL
(WITH current_gd (idx, a, b, c, d, e, f, g, h, i, j) AS (
    SELECT * FROM gd
    ), subresult (idx, a, b, c, d, e, f, g, h, i, j) AS (
    SELECT idx, 
           a - {} * {}(2 * x9 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
           b - {} * {}(2 * x8 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
           c - {} * {}(2 * x7 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
           d - {} * {}(2 * x6 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
           e - {} * {}(2 * x5 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
           f - {} * {}(2 * x4 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
           g - {} * {}(2 * x3 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
           h - {} * {}(2 * x2 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)), 
           i - {} * {}(2 * x1 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y)),
           j - {} * {}(2 * (a * x9 + b * x8 + c * x7 + d * x6 + e * x5 + f * x4 + g * x3 + h * x2 + i * x1 + j - y))
    FROM current_gd, points
    GROUP BY idx, a, b, c, d, e, f, g, h, i, j
  )
  SELECT idx + 1, a, b, c, d, e, f, g, h, i, j
  FROM subresult
  WHERE idx < {}
  )
)
SELECT * FROM gd ORDER BY idx DESC;
'''

CONFIG = {
    'param_value': 0.75,
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
            'types': ['double', 'float', 'bfloat'],
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
            'statement': STATEMENT_2_PARAM,
            'p_amount': 10,
            'param_amount': 2,
            'ignore': False,
            'use_max_points': True
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
            'p_amount': 10000000,
            'param_amount': 3,
            'ignore': True,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_4_PARAM,
            'p_amount': 10000000,
            'param_amount': 4,
            'ignore': True,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_5_PARAM,
            'p_amount': 10000000,
            'param_amount': 5,
            'ignore': True,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_6_PARAM,
            'p_amount': 10000000,
            'param_amount': 6,
            'ignore': True,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_7_PARAM,
            'p_amount': 10000000,
            'param_amount': 7,
            'ignore': True,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_8_PARAM,
            'p_amount': 10000000,
            'param_amount': 8,
            'ignore': True,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_9_PARAM,
            'p_amount': 100000000,
            'param_amount': 9,
            'ignore': True,
            'use_max_points': False
        },
        {
            'iterations': 100,
            'lr': 0.05,
            'statement': STATEMENT_10_PARAM,
            'p_amount': 100000000,
            'param_amount': 10,
            'ignore': True,
            'use_max_points': False
        }
    ] 
}