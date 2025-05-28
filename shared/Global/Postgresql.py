import Settings

POSTGRESQL = {
    'name': 'postgres',
    'create_csv': True,
    'ignore': False,
    'csv_file': 'Postgresql_Results.csv',
    'csv_header': [],
    'files': [Settings.POSTGRESQL_DIR],
    'server-preparation': [
        f'{Settings.POSTGRESQL_DB_PATH}initdb -D {Settings.POSTGRESQL_DIR} -U {Settings.POSTGRESQL_USERNAME}', 
        f'{Settings.POSTGRESQL_DB_PATH}pg_ctl -D {Settings.POSTGRESQL_DIR} start', 
        f'{Settings.POSTGRESQL_DB_PATH}createdb -h {Settings.POSTGRESQL_HOST} -p {Settings.POSTGRESQL_PORT} {Settings.POSTGRESQL_DATABASE_FILE} -U {Settings.POSTGRESQL_USERNAME}', 
        f'{Settings.POSTGRESQL_DB_PATH}pg_ctl -D {Settings.POSTGRESQL_DIR} stop',
    ],
    'client-preparation': f'{Settings.POSTGRESQL_DB_PATH}psql -h {Settings.POSTGRESQL_HOST} -p {Settings.POSTGRESQL_PORT} -U {Settings.POSTGRESQL_USERNAME} -d {Settings.POSTGRESQL_DATABASE_FILE}',
    'time-executable': f'{Settings.POSTGRESQL_DB_PATH}psql -h {Settings.POSTGRESQL_HOST} -p {Settings.POSTGRESQL_PORT} -U {Settings.POSTGRESQL_USERNAME} -d {Settings.POSTGRESQL_DATABASE_FILE} -f {Settings.STATEMENT_FILE}',
    'memory-executable': f'{Settings.POSTGRESQL_DB_PATH}postgres --single {Settings.POSTGRESQL_DATABASE_FILE} -D {Settings.POSTGRESQL_DIR} -p {Settings.POSTGRESQL_PORT} -h {Settings.POSTGRESQL_HOST}',
    'start-sql': [],
    'end-sql': [],
    'types': ['float8', 'float4'],
    'aggregations': ['standard']
}