import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))

import Plotting

if __name__ == "__main__":
    duckdb_file = './data/duckdb/einstein/final_attempt/DuckDB_Results.csv'
    umbra_file = './data/duckdb/einstein/final_attempt/Umbra_Results.csv'
    postgres_file = './data/duckdb/einstein/final_attempt/Postgresql_Results.csv'
    lingodb_file = './data/duckdb/einstein/final_attempt/LingoDB_Results.csv'
    scenario_name = 'Einstein'
    line_keys = ['Type']
    x_keys = ['MatrixA', 'MatrixB', 'VectorV']

    manipulate = {
        'Execution': {
            'function': lambda a, b, c, d: (a + b + c) / d,
            'args': ['MatrixA', 'MatrixB', 'VectorV', 'Execution'],
            'types': ['int', 'int', 'int', 'float']
        }
    }

    manipulate_memory = {
        'Memory': {
            'function': lambda a: a / (1024*1024),
            'args': ['Memory'],
            'types': ['float']
        }
    }

    manipulate_file_size = {
        'Relation-Size': {
            'function': lambda a: a / (1024),
            'args': ['Relation-Size'],
            'types': ['float']
        }
    }

    duckdb_ignore = {
        #'Vector_V': ['400', '500', '600', '700', '800', '900', '1000', '2500', '5000', '7500', '10000'],
        #'Vector_V': ['10', '20', '30', '40', '50', '60', '1000', '2500', '5000', '7500', '10000'],
        #'VectorV': ['10000'],
        'Aggregation': ['kahan'],
        'Statement': ['2','3','4']
    }

    duckdb_ignore_2 = {
        #'Vector_V': ['80', '90', '100', '200', '300', '400', '500', '600', '700', '800', '900', '1000', '2500', '5000', '7500', '10000'],
        #'Vector_V': ['10', '20', '30', '40', '50', '60', '1000', '2500', '5000', '7500', '10000'],
        #'Vector_V': ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '200', '300', '400', '500', '600', '700', '800'],
        'Aggregation': ['kahan'],
        'Statement': ['1','2','3'],
    }

    ignore = {
        #'Vector_V': ['400', '500', '600', '700', '800', '900', '1000', '2500', '5000', '7500', '10000'],
        #'Vector_V': ['10', '20', '30', '40', '50', '60', '500', '1000', '2500', '5000', '7500', '10000'],
        #'Vector_V': ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '200'],
        #'VectorV': ['10000'],
        'Statement': ['2','3','4'],
        #'Type': ['bfloat']
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
            'manipulate': manipulate,
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
        #        'A*(B*v)': ['Execution'],
        #    },
        #    'renaming': {},
        #    'manipulate': {},
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
            'manipulate': manipulate,
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
            'manipulate': manipulate,
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
            'manipulate': manipulate,
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
        #        'A*(B*v)': ['RSS'],
        #    },
        #    'renaming': {},
        #    'manipulate': {},
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
            'manipulate': manipulate_file_size,
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
            'manipulate': manipulate_file_size,
            'ignore': ignore
        },
    }
    config_time = {
        'x_label': 'Number of tuples',
        'y_label': 'Execution in tuples / seconds',
        'log_y': False,
        'log_x': False,
        'file_name': f'Execution_{scenario_name}.pdf'
    }
    config_memory = {
        'x_label': 'Number of tuples',
        'y_label': 'Used memory in MB',
        'log_y': False,
        'log_x': False,
        'file_name': f'Memory_{scenario_name}.pdf'
    }
    config_relation = {
        'x_label': 'Number of tuples',
        'y_label': 'Relation Size in KB',
        'log_y': False,
        'log_x': False,
        'file_name': f'Relation_{scenario_name}.pdf'
    }
    Plotting.plot_results(time, config_time)
    Plotting.plot_results(memory, config_memory)
    Plotting.plot_results(relation, config_relation)