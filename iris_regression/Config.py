import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

import Settings

DUCK_DB_DATABASE_FILE = 'iris.db'
UMBRA_DB_DATABASE_FILE = 'iris'
POSTGRES_DB_DATABASE_FILE = 'iris'
STATEMENT_FILE = 'Statement.sql'

CONFIG = {
    'learning_rate': 0.01,
    'databases': [
        {
            'name': 'duckdb',
            'create_csv': True,
            'ignore': False,
            'csv_file': 'DuckDB_Iris_Results.csv',
            'csv_header': [
                'Type', 
                'Network_Size', 
                'Data_Size', 
                'Iterations', 
                'Execution', 
                'Heap', 
                'RSS', 
                'DuckDB', 
                'Tensorflow'
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
            'csv_file': 'Umbra_Iris_Results.csv',
            'csv_header': [
                'Type', 
                'Network_Size', 
                'Data_Size', 
                'Iterations',  
                'Execution', 
                'Heap', 
                'RSS', 
                'Loss', 
                'Umbra', 
                'Tensorflow'
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
            'csv_file': 'Postgres_Iris_Results.csv',
            'csv_header': [
                'Type', 
                'Network_Size', 
                'Data_Size', 
                'Iterations', 
                'Execution', 
                'Heap', 
                'RSS', 
                'Loss', 
                'Postgres', 
                'Tensorflow'
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
            'iterations': 100,
            'network_size': 100,
            'data_size': 150,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 100,
            'data_size': 300,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 100,
            'data_size': 600,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 100,
            'data_size': 1200,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 100,
            'data_size': 2400,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 100,
            'data_size': 4800,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 300,
            'data_size': 150,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 300,
            'data_size': 300,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 300,
            'data_size': 600,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 300,
            'data_size': 1200,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 300,
            'data_size': 2400,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 300,
            'data_size': 4800,
            'ignore': False
        }
    ] 
}
STATEMENT = '''
with recursive w (iter,id,i,j,v) as (
  (select 0,0,* from w_xh union select 0,1,* from w_ho)
  union all
  (
  with w_now as (
     SELECT * from w
  ), a_xh(i,j,v) as (
     SELECT m.i, n.j, 1/(1+exp(-SUM (m.v*n.v)))
     FROM img AS m INNER JOIN w_now AS n ON m.j=n.i
     WHERE n.id=0 and n.iter=(select max(iter) from w_now) -- w_xh
     GROUP BY m.i, n.j
  ), a_ho(i,j,v) as (
     SELECT m.i, n.j, 1/(1+exp(-SUM (m.v*n.v))) --sig(SUM (m.v*n.v))
     FROM a_xh AS m INNER JOIN w_now AS n ON m.j=n.i
     WHERE n.id=1 and n.iter=(select max(iter) from w_now)  -- w_ho
     GROUP BY m.i, n.j
  ), l_ho(i,j,v) as (
     select m.i, m.j, 2*(m.v-n.v)
     from a_ho AS m INNER JOIN one_hot AS n ON m.i=n.i AND m.j=n.j
  ), d_ho(i,j,v) as (
     select m.i, m.j, m.v*n.v*(1-n.v)
     from l_ho AS m INNER JOIN a_ho AS n ON m.i=n.i AND m.j=n.j
  ), l_xh(i,j,v) as (
     SELECT m.i, n.i as j, (SUM (m.v*n.v)) -- transpose
     FROM d_ho AS m INNER JOIN w_now AS n ON m.j=n.j
     WHERE n.id=1 and n.iter=(select max(iter) from w_now)  -- w_ho
     GROUP BY m.i, n.i
  ), d_xh(i,j,v) as (
     select m.i, m.j, m.v*n.v*(1-n.v)
     from l_xh AS m INNER JOIN a_xh AS n ON m.i=n.i AND m.j=n.j
  ), d_w(id,i,j,v) as (
     SELECT 0, m.j as i, n.j, (SUM (m.v*n.v))
     FROM img AS m INNER JOIN d_xh AS n ON m.i=n.i
     GROUP BY m.j, n.j
     union
     SELECT 1, m.j as i, n.j, (SUM (m.v*n.v))
     FROM a_xh AS m INNER JOIN d_ho AS n ON m.i=n.i
     GROUP BY m.j, n.j
  )
  select iter+1, w.id, w.i, w.j, w.v - 0.01 * d_w.v
  from w_now as w, d_w
  where iter < {} and w.id=d_w.id and w.i=d_w.i and w.j=d_w.j
  )
)

SELECT MAX(precision) FROM (
    SELECT iter, count(*)::float/(select count(distinct i) from one_hot) AS precision
    FROM (
       SELECT *, rank() over (partition by m.i,iter order by v desc) as rank
       FROM (
          SELECT m.i, n.j, 1/(1+exp(-SUM (m.v*n.v))) as v, m.iter
          FROM (
             SELECT m.i, n.j, 1/(1+exp(-SUM (m.v*n.v))) as v, iter
             FROM img AS m INNER JOIN w AS n ON m.j=n.i
             WHERE n.id=0 -- and n.iter=(select max(iter) from w)
             GROUP BY m.i, n.j, iter ) AS m INNER JOIN w AS n ON m.j=n.i
          WHERE n.id=1 and n.iter=m.iter
          GROUP BY m.i, n.j, m.iter
       ) m ) pred,
       (SELECT *, rank() over (partition by m.i order by v desc) as rank FROM one_hot m) test
    WHERE pred.i=test.i and pred.rank = 1 and test.rank=1
    GROUP BY iter, pred.j=test.j
    HAVING (pred.j=test.j)=true
    ORDER BY iter);\n
'''
