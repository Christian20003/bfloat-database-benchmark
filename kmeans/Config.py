import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

import Settings

DUCK_DB_DATABASE_FILE = 'kmeans.db'
UMBRA_DB_DATABASE_FILE = 'kmeans'
STATEMENT_FILE = 'Statement.sql'

CONFIG = {
    'max_points': 100000000,
    'max': 100,
    'min': -100,
    "databases": [
        {
            'name': 'duckdb',
            'create_csv': True,
            'ignore': False,
            'csv_file': 'DuckDB_Kmeans_Results.csv',
            'csv_header': [
                'Type', 
                'Points', 
                'Cluster',
                'Aggregation', 
                'Iterations', 
                'Execution', 
                'Heap', 
                'RSS', 
                'DuckDB-Accuracy',
                'Tensorflow-Accuracy', 
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
            'aggrations': ['standard', 'kahan'],
        },
        {
            'name': 'umbra',
            'create_csv': True,
            'ignore': True,
            'csv_file': 'Umbra_Kmeans_Results.csv',
            'csv_header': [
                'Type', 
                'Points', 
                'Cluster',
                'Aggregation', 
                'Iterations', 
                'Execution', 
                'Heap', 
                'RSS', 
                'Umbra-Accuracy',
                'Tensorflow-Accuracy', 
                'Umbra', 
                'Tensorflow',
                'Truth'
                ],
            'files': [Settings.UMBRA_DIR],
            'execution': f'{Settings.UMBRA_DB_PATH} -createdb {UMBRA_DB_DATABASE_FILE}',
            'execution-bench': f'{Settings.UMBRA_DB_PATH} {UMBRA_DB_DATABASE_FILE} {STATEMENT_FILE}',
            'start-sql': [],
            'end-sql': ['\q;'],
            'types': ['float8', 'float'],
            'aggregations': ['standard']
        }
    ],
    'setups': [
        # setups with increasing number of points
        {
            'c_amount': 4,
            'p_amount': 10,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 100,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 1000,
            'min': -100,
            'max': 100,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 10000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 100000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 250000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 500000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 750000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 1000000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 2500000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 5000000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 7500000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 10000000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 25000000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 50000000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 75000000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 100000000,
            'iterations': 10,
            'ignore': False
        },
        # setups with increasing number of clusters
        {
            'c_amount': 2,
            'p_amount': 10000000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 3,
            'p_amount': 10000000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 5,
            'p_amount': 10000000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 6,
            'p_amount': 10000000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 7,
            'p_amount': 10000000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 8,
            'p_amount': 10000000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 9,
            'p_amount': 10000000,
            'iterations': 10,
            'ignore': False
        },
        {
            'c_amount': 10,
            'p_amount': 10000000,
            'iterations': 10,
            'ignore': False
        },
        # setups with increasing number of iterations
        {
            'c_amount': 4,
            'p_amount': 10000000,
            'iterations': 1,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 10000000,
            'iterations': 2,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 10000000,
            'iterations': 3,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 10000000,
            'iterations': 4,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 10000000,
            'iterations': 5,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 10000000,
            'iterations': 6,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 10000000,
            'iterations': 7,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 10000000,
            'iterations': 8,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 10000000,
            'iterations': 9,
            'ignore': False
        }
    ]
}
STATEMENT = '''
WITH RECURSIVE points_start (pid, x, y) AS (SELECT * FROM points),
clusters (iter, cid, x, y) AS (
    (SELECT 0, id, x, y FROM clusters_0)
    UNION ALL
    (WITH assignment(iter, cid, x, y) AS (
        SELECT iter, cid, {}(px), {}(py) FROM (
            SELECT iter, pid, p.x AS px, p.y AS py, MIN(cid) AS cid
            FROM points_start p, clusters c
            WHERE NOT EXISTS (
                SELECT * FROM clusters d
                WHERE c.iter = d.iter AND (d.x-p.x)^2 + (d.y-p.y)^2 < (c.x-p.x)^2 + (c.y-p.y)^2
            )
            GROUP BY iter, pid, p.x, p.y
        )
        GROUP BY cid, iter),
        add_missing(iter, cid, x, y) AS (
            (SELECT * FROM assignment)
            UNION ALL
            (SELECT MAX(iter), cid, x, y FROM clusters WHERE cid NOT IN (SELECT cid FROM assignment) GROUP BY cid, x, y)
        )
    SELECT iter+1, cid, x, y
    FROM add_missing
    WHERE iter < {}
    )
)
SELECT * FROM clusters ORDER BY cid DESC;
'''

'''

WITH RECURSIVE
points_start (pid, x, y) AS (SELECT * FROM points limit 1000000),
clusters (iter, cid, x, y) AS (
    (SELECT 0, id, x, y FROM clusters_0)
    UNION ALL
    SELECT iter+1, cid, AVG(px), AVG(py) FROM (
        SELECT iter, pid, p.x AS px, p.y AS py, MIN(cid) AS cid
        FROM points_start p, clusters c
        WHERE NOT EXISTS (
            SELECT * FROM clusters d
            WHERE c.iter = d.iter AND (d.x-p.x)^2 + (d.y-p.y)^2 < (c.x-p.x)^2 + (c.y-p.y)^2
        )
        GROUP BY iter, pid, p.x, p.y
    ) AS result
    WHERE iter < 10
    GROUP BY cid, iter
)
SELECT * FROM clusters WHERE iter = 10 ORDER BY cid;

'''