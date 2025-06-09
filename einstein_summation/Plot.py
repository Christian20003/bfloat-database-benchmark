import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))

import Plotting

if __name__ == "__main__":
    duckdb_file = './data/duckdb/einstein/attempt_3/DuckDB_Results.csv'
    umbra_file = './data/duckdb/einstein/attempt_3/Umbra_Results.csv'
    postgres_file = './data/duckdb/einstein/attempt_3/Postgresql_Results.csv'
    lingodb_file = './data/duckdb/einstein/attempt_3/LingoDB_Results.csv'
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

    manipulate_rss = {
        'Execution': {
            'function': lambda a, b, c, d: (a + b + c) / d,
            'args': ['Matrix_A', 'Matrix_B', 'Vector_V', 'RSS'],
            'types': ['int', 'int', 'int', 'float']
        }
    }

    duckdb_ignore = {
        #'Vector_V': ['400', '500', '600', '700', '800', '900', '1000', '2500', '5000', '7500', '10000'],
        #'Vector_V': ['10', '20', '30', '40', '50', '60', '1000', '2500', '5000', '7500', '10000'],
        'Vector_V': ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '200'],
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
        'Vector_V': ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '200'],
        'Statement': ['4','2','3'],
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
            'manipulate': {},
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

    rss = {
        'file_1': {
            'file': duckdb_file,
            'line_keys': line_keys,
            'color': 'maroon',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['RSS'],
            },
            'renaming': {},
            'manipulate': manipulate_rss,
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
                'PSQL': ['RSS'],
            },
            'renaming': postgres_rename,
            'manipulate': manipulate_rss,
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
                'LingoDB': ['RSS'],
            },
            'renaming': postgres_rename,
            'manipulate': manipulate_rss,
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
                'Umbra': ['RSS'],
            },
            'renaming': umbra_rename,
            'manipulate': manipulate_rss,
            'ignore': ignore
        }
    }

    heap = {
        'file_1': {
            'file': duckdb_file,
            'line_keys': line_keys,
            'color': 'maroon',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'B*v': ['Heap'],
            },
            'renaming': {},
            'manipulate': {},
            'ignore': duckdb_ignore
        },
        'file_2': {
            'file': duckdb_file,
            'line_keys': line_keys,
            'color': 'forestgreen',
            'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
            'line_markers': ['o', '^', 's', '*','v', 'D'],
            'x_keys': x_keys,
            'y_keys': {
                'A*(B*v)': ['Heap'],
            },
            'renaming': {},
            'manipulate': {},
            'ignore': duckdb_ignore_2
        },
        #'file_2': {
        #    'file': postgres_file,
        #    'line_keys': line_keys,
        #    'color': 'forestgreen',
        #    'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
        #    'line_markers': ['o', '^', 's', '*','v', 'D'],
        #    'x_keys': x_keys,
        #    'y_keys': {
        #        'PSQL': ['Heap'],
        #    },
        #    'renaming': postgres_rename,
        #    'manipulate': {},
        #    'ignore': ignore
        #},
        #'file_3': {
        #    'file': lingodb_file,
        #    'line_keys': line_keys,
        #    'color': 'orange',
        #    'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
        #    'line_markers': ['o', '^', 's', '*','v', 'D'],
        #    'x_keys': x_keys,
        #    'y_keys': {
        #        'LingoDB': ['Heap'],
        #    },
        #    'renaming': postgres_rename,
        #    'manipulate': {},
        #    'ignore': ignore
        #},
        #'file_4': {
        #    'file': umbra_file,
        #    'line_keys': line_keys,
        #    'color': 'cornflowerblue',
        #    'line_shapes': ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5)), (0, (3, 5, 1, 5))],
        #    'line_markers': ['o', '^', 's', '*','v', 'D'],
        #    'x_keys': x_keys,
        #    'y_keys': {
        #        'Umbra': ['Heap'],
        #    },
        #    'renaming': umbra_rename,
        #    'manipulate': {},
        #    'ignore': ignore
        #}
    }
    config_time = {
        'x_label': 'Number of tuples',
        'y_label': 'Execution in tuples / seconds',
        'log_y': False,
        'log_x': True,
        'file_name': f'Execution_{scenario_name}.pdf'
    }
    config_rss = {
        'x_label': 'Number of tuples',
        'y_label': 'RSS memory in tuples / memory',
        'log_y': False,
        'log_x': True,
        'file_name': f'RSS_{scenario_name}.pdf'
    }
    config_heap = {
        'x_label': 'Number of tuples',
        'y_label': 'Heap in GB',
        'log_y': False,
        'log_x': True,
        'file_name': f'Heap_{scenario_name}.pdf'
    }
    Plotting.plot_results(time, config_time)
    Plotting.plot_results(rss, config_rss)
    Plotting.plot_results(heap, config_heap)