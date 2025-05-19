import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

import Settings

DUCK_DB_DATABASE_FILE = 'einstein.db'
UMBRA_DB_DATABASE_FILE = 'einstein'
POSTGRES_DB_DATABASE_FILE = 'einstein'
STATEMENT_FILE = 'Statement.sql'

STATEMENT_1 = '''
SELECT matrixa.rowIndex AS rowIndex, {}(matrixa.val * matrixb.val * vectorv.val) AS val
FROM matrixa, matrixb, vectorv
WHERE matrixa.columnIndex = matrixb.columnIndex AND matrixb.rowIndex = vectorv.rowIndex
GROUP BY matrixa.rowIndex
ORDER BY matrixa.rowIndex;'''

STATEMENT_2 = '''
SELECT matrixa.rowIndex AS rowIndex, (matrixa.val * matrixb.val * vectorv.val) AS val
FROM matrixa, matrixb, vectorv
WHERE matrixa.columnIndex = matrixb.columnIndex AND matrixb.rowIndex = vectorv.rowIndex
ORDER BY matrixa.rowIndex;'''

STATEMENT_3 = '''
WITH result(rowIndex, val) AS (
    SELECT matrixb.columnIndex, {}(vectorv.val * matrixb.val) AS val
    FROM vectorv, matrixb
    WHERE vectorv.rowIndex = matrixb.rowIndex
    GROUP BY matrixb.columnIndex
) SELECT * FROM result;'''

STATEMENT_4 = '''
WITH result(rowIndex, val) AS (
    SELECT matrixb.columnIndex, {}(vectorv.val * matrixb.val) AS val
    FROM vectorv, matrixb
    WHERE vectorv.rowIndex = matrixb.rowIndex
    GROUP BY matrixb.columnIndex
) SELECT matrixa.rowIndex AS rowIndex, {}(result.val * matrixA.val) AS val
  FROM result, matrixa WHERE result.rowIndex = matrixa.columnIndex 
  GROUP BY matrixa.rowIndex;'''

CONFIG = {
    'databases': [
        {
            'name': 'duckdb',
            'create_csv': True,
            'ignore': True,
            'csv_file': 'DuckDB_Einstein_Results.csv',
            'csv_header': [
                'Type',
                'Aggregation',
                'Statement', 
                'Matrix_A', 
                'Matrix_B', 
                'Vector_V', 
                'Execution', 
                'Heap', 
                'RSS', 
                'DuckDB-L2-Norm',
                'Tensorflow-L2-Norm', 
                'DuckDB-MSE',
                'Tensorflow-MSE',
                'DuckDB-Sum', 
                'Tensorflow-Sum'
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
            'csv_file': 'Umbra_Einstein_Results.csv',
            'csv_header': [
                'Type',
                'Aggregation',
                'Statement', 
                'Matrix_A', 
                'Matrix_B', 
                'Vector_V', 
                'Execution', 
                'Heap', 
                'RSS', 
                'Umbra-L2-Norm',
                'Tensorflow-L2-Norm', 
                'Umbra-MSE',
                'Tensorflow-MSE',
                'Umbra-Sum', 
                'Tensorflow-Sum'
                ],
            'files': [Settings.UMBRA_DIR],
            'execution': f'{Settings.UMBRA_DB_PATH} -createdb {Settings.UMBRA_DIR}/{UMBRA_DB_DATABASE_FILE}',
            'execution-bench': f'{Settings.UMBRA_DB_PATH} {Settings.UMBRA_DIR}/{UMBRA_DB_DATABASE_FILE} {STATEMENT_FILE}',
            'start-sql': [],
            'end-sql': ['\q;'],
            'types': ['float']
        },
        {
            'name': 'postgres',
            'create_csv': True,
            'ignore': True,
            'csv_file': 'Postgres_Einstein_Results.csv',
            'csv_header': [
                'Type',
                'Aggregation',
                'Statement', 
                'Matrix_A', 
                'Matrix_B', 
                'Vector_V', 
                'Execution', 
                'Heap', 
                'RSS', 
                'Postgres-L2-Norm',
                'Tensorflow-L2-Norm', 
                'Postgres-MSE',
                'Tensorflow-MSE',
                'Postgres-Sum', 
                'Tensorflow-Sum'
                ],
            'files': [Settings.POSTGRESQL_DIR],
            'prep': [
                f'{Settings.POSTGRESQL_DB_PATH}initdb -D {Settings.POSTGRESQL_DIR} -U {Settings.POSTGRESQL_USERNAME}', 
                f'{Settings.POSTGRESQL_DB_PATH}pg_ctl -D {Settings.POSTGRESQL_DIR} start', 
                f'{Settings.POSTGRESQL_DB_PATH}createdb -h {Settings.POSTGRESQL_HOST} -p {Settings.POSTGRESQL_PORT} {POSTGRES_DB_DATABASE_FILE} -U {Settings.POSTGRESQL_USERNAME}', 
                f'{Settings.POSTGRESQL_DB_PATH}pg_ctl -D {Settings.POSTGRESQL_DIR} stop',
                f'{Settings.POSTGRESQL_DB_PATH}postgres -D {Settings.POSTGRESQL_DIR} -p {Settings.POSTGRESQL_PORT} -h {Settings.POSTGRESQL_HOST}'],
            'execution': f'{Settings.POSTGRESQL_DB_PATH}psql -h {Settings.POSTGRESQL_HOST} -p {Settings.POSTGRESQL_PORT} -U {Settings.POSTGRESQL_USERNAME} -d {POSTGRES_DB_DATABASE_FILE}',
            'execution-bench': f'{Settings.POSTGRESQL_DB_PATH}psql -h {Settings.POSTGRESQL_HOST} -p {Settings.POSTGRESQL_PORT} -U {Settings.POSTGRESQL_USERNAME} -d {POSTGRES_DB_DATABASE_FILE} -f {STATEMENT_FILE}',
            'start-sql': [],
            'end-sql': [],
            'types': ['float']
        }
    ],
    'setups': [
        {
            'dimension_1': 10,
            'dimension_2': 10,
            'dimension_3': 10,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 20,
            'dimension_2': 20,
            'dimension_3': 20,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 30,
            'dimension_2': 30,
            'dimension_3': 30,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 40,
            'dimension_2': 40,
            'dimension_3': 40,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 60,
            'dimension_2': 60,
            'dimension_3': 60,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 70,
            'dimension_2': 70,
            'dimension_3': 70,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 80,
            'dimension_2': 80,
            'dimension_3': 80,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 90,
            'dimension_2': 90,
            'dimension_3': 90,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 100,
            'dimension_2': 100,
            'dimension_3': 100,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 200,
            'dimension_2': 200,
            'dimension_3': 200,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 300,
            'dimension_2': 300,
            'dimension_3': 300,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 400,
            'dimension_2': 400,
            'dimension_3': 400,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 500,
            'dimension_2': 500,
            'dimension_3': 500,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 600,
            'dimension_2': 600,
            'dimension_3': 600,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 700,
            'dimension_2': 700,
            'dimension_3': 700,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 800,
            'dimension_2': 800,
            'dimension_3': 800,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 900,
            'dimension_2': 900,
            'dimension_3': 900,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 1000,
            'dimension_2': 1000,
            'dimension_3': 1000,
            'statements': [
                STATEMENT_1,
                STATEMENT_2,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 2500,
            'dimension_2': 2500,
            'dimension_3': 2500,
            'statements': [
                STATEMENT_1,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 5000,
            'dimension_2': 5000,
            'dimension_3': 5000,
            'statements': [
                STATEMENT_1,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 7500,
            'dimension_2': 7500,
            'dimension_3': 7500,
            'statements': [
                STATEMENT_1,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
        {
            'dimension_1': 10000,
            'dimension_2': 10000,
            'dimension_3': 10000,
            'statements': [
                STATEMENT_1,
                STATEMENT_3,
                STATEMENT_4
            ],
            'ignore': False
        },
    ]
}
