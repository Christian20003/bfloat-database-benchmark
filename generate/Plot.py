import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))

import Plotting

if __name__ == "__main__":
    duckdb_file = './data/duckdb/series/attempt_1/Psutil_unlimited/DuckDB_Results.csv'
    umbra_file = './data/duckdb/series/attempt_1/Umbra_Results.csv'
    scenario_name = 'Generation'
    line_keys = ['Type']
    x_keys = ['Entries']

    manipulate = {
        'Execution': {
            'function': lambda x,y: x / y,
            'args': ['Iterations', 'Execution'],
            'types': ['int', 'float']
        }
    }

    duckdb_ignore = {
        'Entries': ['10000000', '100000000', '1000000000'],
        'Array': ['False']
    }

    ignore = {
        'Entries': ['10000000', '100000000', '1000000000'],
        'Array': ['False']
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
            'color': 'maroon',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
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
            'color': 'cornflowerblue',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
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
            'color': 'maroon',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
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
            'color': 'cornflowerblue',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
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
            'color': 'maroon',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['Psutil-VMS'],
            },
            'renaming': {},
            'manipulate': {},
            'ignore': duckdb_ignore
        },
        #'file_2': {
        #    'file': umbra_file,
        #    'line_keys': line_keys,
        #    'color': 'cornflowerblue',
        #    'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
        #    'line_markers': ['o', '^', 's', '*','v', 'D'],
        #    'x_keys': x_keys,
        #    'y_keys': {
        #        'Umbra': ['Psutil-VMS'],
        #    },
        #    'renaming': umbra_rename,
        #    'manipulate': {},
        #    'ignore': ignore
        #}
    }
    config_ht_rss = {
        'x_label': 'Number of entries',
        'y_label': 'Used RSS memory in GB',
        'log_y': False,
        'log_x': True,
        'file_name': f'Heaptrack_RSS_{scenario_name}.pdf'
    }
    config_pu_rss = {
        'x_label': 'Number of entries',
        'y_label': 'Used RSS memory in GB',
        'log_y': False,
        'log_x': True,
        'file_name': f'Psutil_RSS_{scenario_name}.pdf'
    }
    config_pu_vms = {
        'x_label': 'Number of entries',
        'y_label': 'Used VMS memory in GB',
        'log_y': False,
        'log_x': True,
        'file_name': f'Psutil_VMS_{scenario_name}.pdf'
    }
    Plotting.plot_results(ht_rss, config_ht_rss)
    Plotting.plot_results(pu_rss, config_pu_rss)
    Plotting.plot_results(pu_vms, config_pu_vms)