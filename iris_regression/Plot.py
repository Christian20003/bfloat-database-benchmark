import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))

import Plotting

if __name__ == "__main__":
    duckdb_file = './data/duckdb/iris/really_final/DuckDB_Results.csv'
    umbra_file = './data/duckdb/iris/really_final/Umbra_Results.csv'
    lingodb_file = './data/duckdb/iris/really_final/LingoDB_Results.csv'
    scenario_name = 'Regression'
    line_keys = ['Type']
    x_keys = ['Data_Size']
    #x_keys = ['Network_Size']
    #x_keys = ['Iterations']

    manipulate_time = {
        'Execution': {
            'function': lambda x,y: x / y,
            'args': ['Iterations', 'Execution'],
            'types': ['int', 'float']
        }
    }

    manipulate_memory = {
        'Memory': {
            'function': lambda x: x / (1024*1024),
            'args': ['Memory'],
            'types': ['float']
        }
    }

    manipulate_relation = {
        'Relation-Size': {
            'function': lambda x: x / (1024),
            'args': ['Relation-Size'],
            'types': ['float']
        }
    }

    ignore = {
        'Iterations': ['1', '5', '10', '15'],
        'Network_Size': ['100', '200', '400'],
        #'Data_Size': ['150', '300', '600']
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
            'color': 'maroon',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['Execution'],
            },
            'renaming': {},
            'manipulate': manipulate_time,
            'ignore': ignore
        },
        'file_2': {
            'file': lingodb_file,
            'line_keys': line_keys,
            'color': 'orange',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'LingoDB': ['Execution'],
            },
            'renaming': postgres_rename,
            'manipulate': manipulate_time,
            'ignore': ignore
        },
        'file_3': {
            'file': umbra_file,
            'line_keys': line_keys,
            'color': 'cornflowerblue',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'Umbra': ['Execution'],
            },
            'renaming': umbra_rename,
            'manipulate': manipulate_time,
            'ignore': ignore
        }
    }

    memory = {
        'file_1': {
            'file': duckdb_file,
            'line_keys': line_keys,
            'color': 'maroon',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['Memory']
            },
            'renaming': {},
            'manipulate': {},
            'ignore': ignore
        },
        'file_2': {
            'file': lingodb_file,
            'line_keys': line_keys,
            'color': 'orange',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'LingoDB': ['Memory'],
            },
            'renaming': postgres_rename,
            'manipulate': {},
            'ignore': ignore
        },
        'file_3': {
            'file': umbra_file,
            'line_keys': line_keys,
            'color': 'cornflowerblue',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'Umbra': ['Memory'],
            },
            'renaming': umbra_rename,
            'manipulate': {},
            'ignore': ignore
        }
    }

    relation = {
        'file_1': {
            'file': duckdb_file,
            'line_keys': line_keys,
            'color': 'maroon',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['Relation-Size'],
            },
            'renaming': {},
            'manipulate': manipulate_relation,
            'ignore': ignore
        },
        'file_2': {
            'file': lingodb_file,
            'line_keys': line_keys,
            'color': 'orange',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'LingoDB': ['Relation-Size'],
            },
            'renaming': postgres_rename,
            'manipulate': manipulate_relation,
            'ignore': ignore
        }
    }

    acc = {
        'file_1': {
            'file': duckdb_file,
            'line_keys': line_keys,
            'color': 'maroon',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['Accuracy'],
            },
            'renaming': {},
            'manipulate': {},
            'ignore': ignore
        }
    }

    config_time = {
        'x_label': 'Number of samples',
        'y_label': 'Throughput (iteratations / seconds)',
        'log_y': False,
        'log_x': False,
        'file_name': f'Execution_{scenario_name}.pdf'
    }
    config_memory = {
        'x_label': 'Number of samples',
        'y_label': 'Used memory in GB',
        'log_y': False,
        'log_x': False,
        'file_name': f'Memory_{scenario_name}.pdf'
    }
    config_relation = {
        'x_label': 'Number of samples',
        'y_label': 'Relation Size in KB',
        'log_y': False,
        'log_x': False,
        'file_name': f'Relation_{scenario_name}.pdf'
    }
    config_acc = {
        'x_label': 'Number of samples',
        'y_label': 'Accuracy',
        'log_y': False,
        'log_x': False,
        'file_name': f'Accuracy_{scenario_name}.pdf'
    }
    Plotting.plot_results(time, config_time)
    Plotting.plot_results(memory, config_memory)
    Plotting.plot_results(relation, config_relation)
    Plotting.plot_results(acc, config_acc)