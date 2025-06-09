import Settings

UMBRA = {
    'name': 'umbra',
    'create_csv': True,
    'ignore': False,
    'csv_file': 'Umbra_Results.csv',
    'csv_header': [],
    'files': [Settings.UMBRA_DIR],
    'server-preparation': [],
    'client-preparation': f'{Settings.UMBRA_DB_PATH} -createdb {Settings.UMBRA_DIR}/{Settings.UMBRA_DATABASE_FILE}',
    'time-executable': f'{Settings.UMBRA_DB_PATH} {Settings.UMBRA_DIR}/{Settings.UMBRA_DATABASE_FILE} {Settings.STATEMENT_FILE}',
    'memory-executable': f'{Settings.UMBRA_DB_PATH} {Settings.UMBRA_DIR}/{Settings.UMBRA_DATABASE_FILE} {Settings.STATEMENT_FILE}',
    'start-sql': [],
    'end-sql': ['\q;'],
    'types': ['float8'],
    'aggregations': ['standard']
}