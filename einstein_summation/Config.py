CONFIG = {
    "max": 10,
    "min": -10,
    'databases': [
        {
            'name': 'duckdb',
            'create_csv': True,
            'csv_file': 'DuckDB_Einstein_Results.csv',
            'csv_header': ['Type', 'Matrix_A', 'Matrix_B', 'Vector_V', 'Execution', 'Memory', 'Loss', 'DuckDB', 'Tensorflow'],
            'files': ['einstein.db'],
            'execution': '/home/goellner/.duckdb/cli/1.2.2/duckdb einstein.db',
            'execution-bench': '/home/goellner/.duckdb/cli/1.2.2/duckdb -f {} einstein.db',
            'start-sql': [],
            'end-sql': ['.exit'],
            'types': ['float', 'tfloat']
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
            'dimension_1': 100,
            'dimension_2': 100,
            'dimension_3': 100,
            'ignore': False
        },
        {
            'dimension_1': 1000,
            'dimension_2': 1000,
            'dimension_3': 1000,
            'ignore': False
        },
        {
            'dimension_1': 10000,
            'dimension_2': 10000,
            'dimension_3': 10000,
            'ignore': False
        },
        {
            'dimension_1': 100000,
            'dimension_2': 100000,
            'dimension_3': 100000,
            'ignore': False
        },
        {
            'dimension_1': 1000000,
            'dimension_2': 1000000,
            'dimension_3': 1000000,
            'ignore': False
        },
        {
            'dimension_1': 2500000,
            'dimension_2': 2500000,
            'dimension_3': 2500000,
            'ignore': False
        },
        {
            'dimension_1': 5000000,
            'dimension_2': 5000000,
            'dimension_3': 5000000,
            'ignore': False
        },
        {
            'dimension_1': 10000000,
            'dimension_2': 10000000,
            'dimension_3': 10000000,
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