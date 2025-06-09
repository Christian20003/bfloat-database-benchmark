import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))

import Plot

if __name__ == "__main__":
    duckdb_file = './DuckDB_Results.csv'
    umbra_file = './Umbra_Results.csv'
    scenario_name = 'Generation'
    line_keys = ['Type']
    x_keys = ['Rows']

    manipulate = {
        'Execution': {
            'function': lambda x,y: x / y,
            'args': ['Iterations', 'Execution'],
            'types': ['int', 'float']
        }
    }

    duckdb_ignore = {
        
    }

    ignore = {
        
    }

    umbra_rename = {
        'Type': {
            'old': ['float8'],
            'new': ['double']
        }
    }

    ht_rss = {
        'file_1': {
            'file': duckdb_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['Heaptrack-RSS'],
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
                'Umbra': ['Heaptrack-RSS'],
            },
            'renaming': umbra_rename,
            'manipulate': {},
            'ignore': ignore
        }
    }

    pu_rss = {
        'file_1': {
            'file': duckdb_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['Psutil-RSS'],
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
                'Umbra': ['Psutil-RSS'],
            },
            'renaming': umbra_rename,
            'manipulate': {},
            'ignore': ignore
        }
    }

    pu_vms = {
        'file_1': {
            'file': duckdb_file,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['Psutil-VMS'],
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
                'Umbra': ['Psutil-VMS'],
            },
            'renaming': umbra_rename,
            'manipulate': {},
            'ignore': ignore
        }
    }
    config_ht_rss = {
        'x_label': 'Number of rows',
        'y_label': 'Used RSS memory in GB',
        'file_name': f'Heaptrack_RSS_{scenario_name}.pdf'
    }
    config_pu_rss = {
        'x_label': 'Number of rows',
        'y_label': 'Used RSS memory in GB',
        'file_name': f'Psutil_RSS_{scenario_name}.pdf'
    }
    config_pu_vms = {
        'x_label': 'Number of rows',
        'y_label': 'Used VMS memory in GB',
        'file_name': f'Psutil_VMS_{scenario_name}.pdf'
    }
    Plot.plot_results(ht_rss, config_ht_rss)
    Plot.plot_results(pu_rss, config_pu_rss)
    Plot.plot_results(pu_vms, config_pu_vms)