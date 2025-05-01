CONFIG = {
    'learning_rate': 0.01,
    'databases': [
        {
            'name': 'duckdb',
            'create_csv': True,
            'csv_file': 'DuckDB_Iris_Results.csv',
            'csv_header': ['Type', 'Network_Size', 'Data_Size', 'Iterations', 'Execution', 'Heap', 'RSS', 'DuckDB', 'Tensorflow'],
            'files': ['./iris.db'],
            'execution': '/home/proglin/duckdb/build/release/duckdb iris.db',
            'execution-bench': '/home/proglin/duckdb/build/release/duckdb -json -f {} iris.db',
            'start-sql': [],
            'end-sql': ['.exit'],
            'types': ['float', 'bfloat']
        }
    ],
    'setups': [
        {
            'iterations': 100,
            'network_size': 20,
            'data_size': 150,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 20,
            'data_size': 300,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 20,
            'data_size': 600,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 20,
            'data_size': 1200,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 50,
            'data_size': 150,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 50,
            'data_size': 300,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 50,
            'data_size': 600,
            'ignore': False
        },
        {
            'iterations': 100,
            'network_size': 50,
            'data_size': 1200,
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
