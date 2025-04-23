CONFIG = {
    'iterations': 5,
    'databases': [
        {
            'name': 'duckdb',
            'create_csv': True,
            'csv_file': 'DuckDB_Regression_Results.csv',
            'csv_header': ['Type', 'Points', 'Iterations', 'Execution', 'Memory', 'Accuracy', 'DuckDB', 'Tensorflow', 'Truth'],
            'files': ['regression.db'],
            'execution': '/home/goellner/.duckdb/cli/1.2.2/duckdb regression.db',
            'execution-bench': '/home/goellner/.duckdb/cli/1.2.2/duckdb -f {} regression.db',
            'start-sql': '',
            'end-sql': '.exit',
            'types': ['float', 'tfloat']
        }
    ],
    'setups': [
        {
            'lr': 0.01,
            'p_amount': 10,
            'max': 10,
            'min': -10,
            'ignore': False
        },
        {
            'lr': 0.01,
            'p_amount': 100,
            'max': 50,
            'min': -50,
            'ignore': False
        },
        {
            'lr': 0.01,
            'p_amount': 1000,
            'max': 100,
            'min': -100,
            'ignore': False
        },
        {
            'lr': 0.01,
            'p_amount': 10000,
            'max': 200,
            'min': -200,
            'ignore': False
        },
        {
            'lr': 0.01,
            'p_amount': 100000,
            'max': 300,
            'min': -300,
            'ignore': False
        },
        {
            'lr': 0.01,
            'p_amount': 1000000,
            'max': 300,
            'min': -300,
            'ignore': False
        },
        {
            'lr': 0.01,
            'p_amount': 2500000,
            'max': 300,
            'min': -300,
            'ignore': False
        },
        {
            'lr': 0.01,
            'p_amount': 5000000,
            'max': 300,
            'min': -300,
            'ignore': False
        },
    ] 
}

STATEMENT = '''
WITH RECURSIVE gd (idx, a, b) AS (
    SELECT 0, 1, 1
UNION ALL
    SELECT idx + 1, a - {} * avg(2 * x * (a * x + b - y)), b - {} * avg(2 * (a * x + b - y))
    FROM gd, points 
    WHERE idx < {} GROUP BY idx, a, b
)
SELECT * FROM gd WHERE idx = {};
'''