import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))

import Plotting

if __name__ == "__main__":
    duckdb_file = './DuckDB_Einstein_Results.csv'
    umbra_file = './Umbra_Einstein_Results.csv'
    postgres_file = './Postgres_Einstein_Results.csv'
    lingodb_file = './LingoDB_Einstein_Results.csv'
    scenario_name = 'Einstein'
    line_keys = ['Type']
    x_keys = ['Matrix_A', 'Matrix_B', 'Vector_V']

    manipulate = {
        'Execution': {
            'function': lambda a, b, c, d: (a + b + c) / d,
            'args': ['Matrix_A', 'Matrix_B', 'Vector_V', 'Execution'],
            'types': ['int', 'int', 'int', 'float']
        }
    }

    duckdb_ignore = {
        #'Vector_V': ['1000', '2500', '5000', '7500', '10000'],
        'Aggregation': ['kahan'],
        'Statement': ['2','3','4']
    }

    ignore = {
        #'Vector_V': ['1000', '2500', '5000', '7500', '10000'],
        'Statement': ['2','3','4']
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
            'manipulate': {},
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
            'manipulate': {},
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
            'manipulate': {},
            'ignore': ignore
        },
        'file_4': {
            'file': lingodb_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'LingoDB': ['Execution'],
            },
            'renaming': postgres_rename,
            'manipulate': {},
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
        },
        'file_4': {
            'file': lingodb_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'LingoDB': ['RSS'],
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
        },
        'file_4': {
            'file': lingodb_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'LingoDB': ['Heap'],
            },
            'renaming': postgres_rename,
            'manipulate': {},
            'ignore': ignore
        }
    }
    config_time = {
        'x_label': 'Number of samples',
        'y_label': 'Execution time in seconds',
        'log_y': False,
        'log_x': True,
        'file_name': f'Execution_{scenario_name}.pdf'
    }
    config_rss = {
        'x_label': 'Number of samples',
        'y_label': 'RSS memors in GB',
        'log_y': False,
        'log_x': True,
        'file_name': f'RSS_{scenario_name}.pdf'
    }
    config_heap = {
        'x_label': 'Number of samples',
        'y_label': 'Heap in GB',
        'log_y': False,
        'log_x': True,
        'file_name': f'Heap_{scenario_name}.pdf'
    }
    Plotting.plot_results(time, config_time)
    Plotting.plot_results(rss, config_rss)
    Plotting.plot_results(heap, config_heap)