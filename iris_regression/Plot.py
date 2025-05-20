import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))

import Plot

if __name__ == "__main__":
    duckdb_file = './DuckDB_Regression_Results.csv'
    umbra_file = './Umbra_Regression_Results.csv'
    postgres_file = './Postgres_Regression_Results.csv'
    scenario_name = 'Regression'
    line_keys = ['Type']
    x_keys = ['Points']

    manipulate = {
        'Execution': {
            'function': lambda x,y: x / y,
            'args': ['Iterations', 'Execution'],
            'types': ['int', 'float']
        }
    }

    duckdb_ignore = {
        'Aggregations': ['standard'],
        'Statement': [2],
        'Iterations': [10],
        'Network_Size': [300]
    }

    ignore = {
        'Parameters': [2],
        'Iterations': [10],
        'Network_Size': [300]
    }

    umbra_rename = {
        'Type': {
            'old': ['float8'],
            'new': ['double']
        }
    }

    postgres_rename = {
        'Type': {
            'old': ['float4', 'float8'],
            'new': ['float', 'double']
        }
    }
        
    time = {
        'file_1': {
            'file': duckdb_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['Execution'],
            },
            'renaming': {},
            'manipulate': manipulate,
            'ignore': duckdb_ignore
        },
        'file_2': {
            'file': umbra_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'Umbra': ['Execution'],
            },
            'renaming': umbra_rename,
            'manipulate': manipulate,
            'ignore': ignore
        },
        'file_3': {
            'file': postgres_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'Postgresql': ['Execution'],
            },
            'renaming': postgres_rename,
            'manipulate': manipulate,
            'ignore': ignore
        }
    }

    rss = {
        'file_1': {
            'file': duckdb_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['RSS'],
            },
            'renaming': {},
            'manipulate': {},
            'ignore': duckdb_ignore
        },
        'file_2': {
            'file': umbra_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'Umbra': ['RSS'],
            },
            'renaming': umbra_rename,
            'manipulate': {},
            'ignore': ignore
        },
        'file_3': {
            'file': postgres_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'Postgresql': ['RSS'],
            },
            'renaming': postgres_rename,
            'manipulate': {},
            'ignore': ignore
        }
    }

    heap = {
        'file_1': {
            'file': duckdb_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['Heap'],
            },
            'renaming': {},
            'manipulate': {},
            'ignore': duckdb_ignore
        },
        'file_2': {
            'file': umbra_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'Umbra': ['Heap'],
            },
            'renaming': umbra_rename,
            'manipulate': {},
            'ignore': ignore
        },
        'file_3': {
            'file': postgres_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'Postgresql': ['Heap'],
            },
            'renaming': postgres_rename,
            'manipulate': {},
            'ignore': ignore
        }
    }
    config_time = {
        'x_label': 'Number of samples',
        'y_label': 'Execution time in iterations / seconds',
        'file_name': f'Execution_{scenario_name}.pdf'
    }
    config_rss = {
        'x_label': 'Number of samples',
        'y_label': 'RSS memors in GB',
        'file_name': f'RSS_{scenario_name}.pdf'
    }
    config_heap = {
        'x_label': 'Number of samples',
        'y_label': 'Heap in GB',
        'file_name': f'Heap_{scenario_name}.pdf'
    }
    Plot.plot_results(time, config_time)
    Plot.plot_results(rss, config_rss)
    Plot.plot_results(heap, config_heap)