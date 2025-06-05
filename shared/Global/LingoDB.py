import Settings

LINGODB = {
    'name': 'lingodb',
    'create_csv': False,
    'ignore': True,
    'csv_file': 'LingoDB_Results.csv',
    'csv_header': [],
    'files': [Settings.LINGODB_DIR],
    'server-preparation': [],
    'client-preparation': f'{Settings.LINGODB_DB_PATH}sql {Settings.LINGODB_DIR}',
    'time-executable': f'{Settings.LINGODB_DB_PATH}run-sql {Settings.STATEMENT_FILE} {Settings.LINGODB_DIR}',
    'memory-executable': f'{Settings.LINGODB_DB_PATH}run-sql {Settings.STATEMENT_FILE} {Settings.LINGODB_DIR}',
    'start-sql': ['SET persist=1;\n'],
    'end-sql': ['exit'],
    'types': ['float8', 'float4', 'bfloat'],
    'aggregations': ['standard']
}