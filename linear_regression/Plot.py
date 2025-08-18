import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))

import Plotting

if __name__ == "__main__":
    duckdb_file = './data/duckdb/regression/final_attempt/DuckDB_Results.csv'
    umbra_file = './data/duckdb/regression/final_attempt/Umbra_Results.csv'
    postgres_file = './data/duckdb/regression/final_attempt/Postgresql_Results.csv'
    lingodb_file = './data/duckdb/regression/final_attempt/LingoDB_Results.csv'
    scenario_name = 'Regression'
    line_keys = ['Type']
    x_keys = ['Points']
    #x_keys = ['Parameters']

    manipulate_time = {
        'Execution': {
            'function': lambda x,y: x / y,
            'args': ['Iterations', 'Execution'],
            'types': ['int', 'float']
        }
    }

    manipulate_memory = {
        'Memory': {
            'function': lambda x: x / (1024*1024*1024),
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

    duckdb_ignore = {
        'Aggregation': ['kahan'],
        'Parameters': ['3', '4', '5', '6', '7', '8', '9', '10'],
        #'Points': ['10', '1000', '100000', '1000000000']
        #'Points': ['1000000000']
    }
    duckdb_ignore_2 = {
        'Aggregation': ['standard'],
        #'Parameters': ['3', '4', '5', '6', '7', '8', '9', '10'],
        'Points': ['10', '1000', '100000', '1000000000'],
        #'Type': ['double', 'float']
    }

    ignore = {
        'Parameters': ['3', '4', '5', '6', '7', '8', '9', '10'],
        #'Points': ['10', '1000', '100000', '1000000000']
        #'Points': ['1000000000']
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
                #'Standard': ['Execution']
            },
            'renaming': {},
            'manipulate': manipulate_time,
            'ignore': duckdb_ignore
        },
        #'file_2': {
        #    'file': duckdb_file,
        #    'line_keys': line_keys,
        #    'color': 'forestgreen',
        #    'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
        #    'line_markers': ['o', '^', 's', '*','v', 'D'],
        #    'x_keys': x_keys,
        #    'y_keys': {
        #        'Kahan': ['Execution']
        #    },
        #    'renaming': {},
        #    'manipulate': manipulate_time,
        #    'ignore': duckdb_ignore_2
        #},
        'file_2': {
            'file': postgres_file,
            'line_keys': line_keys,
            'color': 'forestgreen',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'PSQL': ['Execution'],
            },
            'renaming': postgres_rename,
            'manipulate': manipulate_time,
            'ignore': ignore
        },
        'file_3': {
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
        'file_4': {
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
                'DuckDB': ['Memory'],
                #'Standard': ['Memory']
            },
            'renaming': {},
            'manipulate': manipulate_memory,
            'ignore': duckdb_ignore
        },
        #'file_2': {
        #    'file': duckdb_file,
        #    'line_keys': line_keys,
        #    'color': 'forestgreen',
        #    'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
        #    'line_markers': ['o', '^', 's', '*','v', 'D'],
        #    'x_keys': x_keys,
        #    'y_keys': {
        #        'Kahan': ['Memory']
        #    },
        #    'renaming': {},
        #    'manipulate': manipulate_memory,
        #    'ignore': duckdb_ignore_2
        #},
        'file_2': {
            'file': postgres_file,
            'line_keys': line_keys,
            'color': 'forestgreen',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'PSQL': ['Memory'],
            },
            'renaming': postgres_rename,
            'manipulate': manipulate_memory,
            'ignore': ignore
        },
        'file_3': {
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
            'manipulate': manipulate_memory,
            'ignore': ignore
        },
        'file_4': {
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
            'manipulate': manipulate_memory,
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
            'ignore': duckdb_ignore
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

    mse = {
        'file_1': {
            'file': duckdb_file,
            'line_keys': line_keys,
            'color': 'maroon',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'Standard': ['MSE'],
            },
            'renaming': {},
            'manipulate': {},
            'ignore': duckdb_ignore
        },
        'file_2': {
            'file': duckdb_file,
            'line_keys': line_keys,
            'color': 'cornflowerblue',
            'line_shapes': ['dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['s', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'Kahan': ['MSE'],
            },
            'renaming': {},
            'manipulate': {},
            'ignore': duckdb_ignore_2
        }
    }

    config_time = {
        'x_label': 'Number of samples',
        'y_label': 'Execution time in iterations / seconds',
        'log_y': False,
        'log_x': True,
        'file_name': f'Execution_{scenario_name}.pdf'
    }
    config_memory = {
        'x_label': 'Number of samples',
        'y_label': 'Memory in GB',
        'log_y': False,
        'log_x': True,
        'file_name': f'Memory_{scenario_name}.pdf'
    }
    config_relation = {
        'x_label': 'Number of samples',
        'y_label': 'Output relation size in KB',
        'log_y': False,
        'log_x': True,
        'file_name': f'Relation_{scenario_name}.pdf'
    }
    config_mse = {
        'x_label': 'Number of samples',
        'y_label': 'Mean-Squared-Error',
        'log_y': False,
        'log_x': True,
        'file_name': f'MSE_{scenario_name}.pdf'
    }
    Plotting.plot_results(time, config_time)
    Plotting.plot_results(memory, config_memory)
    Plotting.plot_results(relation, config_relation)
    Plotting.plot_results(mse, config_mse)