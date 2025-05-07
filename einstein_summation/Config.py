import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

import Settings

DUCK_DB_DATABASE_FILE = 'einstein.db'
UMBRA_DB_DATABASE_FILE = 'einstein'
POSTGRES_DB_DATABASE_FILE = 'einstein'
STATEMENT_FILE = 'Statement.sql'

CONFIG = {
    'databases': [
        {
            'name': 'duckdb',
            'create_csv': True,
            'ignore': False,
            'csv_file': 'DuckDB_Einstein_Results.csv',
            'csv_header': [
                'Type', 
                'Matrix_A', 
                'Matrix_B', 
                'Vector_V', 
                'Execution', 
                'Heap', 
                'RSS', 
                'Loss', 
                'DuckDB-Sum', 
                'Tensorflow-Sum'
                ],
            'files': [f'./{DUCK_DB_DATABASE_FILE}'],
            'execution': f'{Settings.DUCK_DB_PATH} {DUCK_DB_DATABASE_FILE}',
            'execution-bench': f'{Settings.DUCK_DB_PATH} -json -f {STATEMENT_FILE} {DUCK_DB_DATABASE_FILE}',
            'start-sql': [],
            'end-sql': ['.exit'],
            'types': ['float', 'bfloat']
        },
        {
            'name': 'umbra',
            'create_csv': True,
            'ignore': True,
            'csv_file': 'Umbra_Einstein_Results.csv',
            'csv_header': [
                'Type', 
                'Matrix_A', 
                'Matrix_B', 
                'Vector_V', 
                'Execution', 
                'Heap', 
                'RSS', 
                'Loss', 
                'Umbra-Sum', 
                'Tensorflow-Sum'
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
            'csv_file': 'Postgres_Einstein_Results.csv',
            'csv_header': [
                'Type', 
                'Matrix_A', 
                'Matrix_B', 
                'Vector_V', 
                'Execution', 
                'Heap', 
                'RSS', 
                'Loss', 
                'Postgres-Sum', 
                'Tensorflow-Sum'
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
        {
            'dimension_1': 10,
            'dimension_2': 10,
            'dimension_3': 10,
            'ignore': False
        },
        {
            'dimension_1': 20,
            'dimension_2': 20,
            'dimension_3': 20,
            'ignore': False
        },
        {
            'dimension_1': 30,
            'dimension_2': 30,
            'dimension_3': 30,
            'ignore': False
        },
        {
            'dimension_1': 40,
            'dimension_2': 40,
            'dimension_3': 40,
            'ignore': False
        },
        {
            'dimension_1': 60,
            'dimension_2': 60,
            'dimension_3': 60,
            'ignore': False
        },
        {
            'dimension_1': 70,
            'dimension_2': 70,
            'dimension_3': 70,
            'ignore': False
        },
        {
            'dimension_1': 80,
            'dimension_2': 80,
            'dimension_3': 80,
            'ignore': False
        },
        {
            'dimension_1': 90,
            'dimension_2': 90,
            'dimension_3': 90,
            'ignore': False
        },
        {
            'dimension_1': 100,
            'dimension_2': 100,
            'dimension_3': 100,
            'ignore': False
        },
        {
            'dimension_1': 200,
            'dimension_2': 200,
            'dimension_3': 200,
            'ignore': False
        },
        {
            'dimension_1': 300,
            'dimension_2': 300,
            'dimension_3': 300,
            'ignore': False
        },
        {
            'dimension_1': 400,
            'dimension_2': 400,
            'dimension_3': 400,
            'ignore': False
        },
        {
            'dimension_1': 500,
            'dimension_2': 500,
            'dimension_3': 500,
            'ignore': False
        },
        {
            'dimension_1': 600,
            'dimension_2': 600,
            'dimension_3': 600,
            'ignore': False
        },
        {
            'dimension_1': 700,
            'dimension_2': 700,
            'dimension_3': 700,
            'ignore': False
        },
        {
            'dimension_1': 800,
            'dimension_2': 800,
            'dimension_3': 800,
            'ignore': False
        },
        {
            'dimension_1': 900,
            'dimension_2': 900,
            'dimension_3': 900,
            'ignore': False
        },
        {
            'dimension_1': 1000,
            'dimension_2': 1000,
            'dimension_3': 1000,
            'ignore': False
        },
        {
            'dimension_1': 2500,
            'dimension_2': 2500,
            'dimension_3': 2500,
            'ignore': False
        },
        {
            'dimension_1': 5000,
            'dimension_2': 5000,
            'dimension_3': 5000,
            'ignore': False
        },
        {
            'dimension_1': 7500,
            'dimension_2': 7500,
            'dimension_3': 7500,
            'ignore': False
        },
        {
            'dimension_1': 10000,
            'dimension_2': 10000,
            'dimension_3': 10000,
            'ignore': False
        },
    ]
}
STATEMENT = '''
WITH A(rowIndex, columnIndex, val) AS (SELECT * FROM matrixa),
    B(rowIndex, columnIndex, val) AS (SELECT * FROM matrixb),
    v(rowIndex, val) AS (SELECT rowIndex, val FROM vectorv)
    SELECT A.rowIndex AS rowIndex, SUM(A.val * B.val * v.val) AS val
    FROM A, B, v
    WHERE A.columnIndex = B.columnIndex AND B.rowIndex = v.rowIndex
    GROUP BY A.rowIndex
    ORDER BY A.rowIndex;
'''