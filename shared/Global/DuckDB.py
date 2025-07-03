import Settings

DUCKDB = {
    'name': 'duckdb',
    'create_csv': True,
    'ignore': False,
    'csv_file': 'DuckDB_Results.csv',
    'csv_header': [],
    'files': [f'./{Settings.DUCK_DB_DATABASE_FILE}'],
    'server-preparation': [],
    'client-preparation': f'{Settings.DUCK_DB_PATH} {Settings.DUCK_DB_DATABASE_FILE}',
    'time-executable': f'{Settings.DUCK_DB_PATH} -f {Settings.STATEMENT_FILE} {Settings.DUCK_DB_DATABASE_FILE}',
    'memory-executable': f'{Settings.DUCK_DB_PATH} {Settings.DUCK_DB_DATABASE_FILE}',
    'start-sql': [],
    'end-sql': ['.exit'],
    'types': ['double', 'float', 'bfloat'],
    'aggregations': ['standard', 'kahan']
}