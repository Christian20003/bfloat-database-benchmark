CONFIG = {
    "iterations": 10,
    "databases": [
        {
            'name': 'duckdb',
            'create_csv': True,
            'csv_file': 'DuckDB_Kmeans_Results.csv',
            'csv_header': ['Type', 'Points', 'Cluster', 'Iterations', 'Execution', 'Heap', 'RSS', 'Accuracy', 'DuckDB', 'Tensorflow'],
            'files': ['./kmeans.db'],
            'execution': '/home/proglin/duckdb/build/release/duckdb kmeans.db',
            'execution-bench': '/home/proglin/duckdb/build/release/duckdb -json -f {} kmeans.db',
            'start-sql': [],
            'end-sql': ['.exit'],
            'types': ['float', 'bfloat']
        }
    ],
    'setups': [
        {
            'c_amount': 4,
            'p_amount': 10,
            'min': -10,
            'max': 10,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 100,
            'min': -10,
            'max': 10,
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
            'min': -100,
            'max': 100,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 100000,
            'min': -100,
            'max': 100,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 1000000,
            'min': -500,
            'max': 500,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 10000000,
            'min': -500,
            'max': 500,
            'ignore': False
        },
        {
            'c_amount': 4,
            'p_amount': 100000000,
            'min': -1000,
            'max': 1000,
            'ignore': False
        }
    ]
}
STATEMENT = '''
WITH RECURSIVE 
points_start (pid, x, y) AS (SELECT * FROM points),
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
    WHERE iter < {}
    GROUP BY cid, iter
)
SELECT * FROM clusters WHERE iter = {} ORDER BY cid;
'''