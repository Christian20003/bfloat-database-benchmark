import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from Statements import *
import DuckDB
import Umbra
import Postgresql
import LingoDB

csv_header = [
    'Type',
    'Aggregation',
    'Statement', 
    'Matrix_A', 
    'Matrix_B', 
    'Vector_V', 
    'Execution', 
    'Heap', 
    'RSS', 
    'Database-L2-Norm',
    'Tensorflow-L2-Norm', 
    'Database-MSE',
    'Tensorflow-MSE',
    'Database-Sum', 
    'Tensorflow-Sum'
]

duckdb = DuckDB.DUCKDB
duckdb['csv_header'] = csv_header
umbra = Umbra.UMBRA
umbra['csv_header'] = csv_header
postgresql = Postgresql.POSTGRESQL
postgresql['csv_header'] = csv_header
lingodb = LingoDB.LINGODB
lingodb['csv_header'] = csv_header

CONFIG = {
    'databases': [
        duckdb,
        umbra,
        postgresql,
        lingodb
    ],
    'setups': [
        {
            'dimension_1': 10,
            'dimension_2': 10,
            'dimension_3': 10,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 20,
            'dimension_2': 20,
            'dimension_3': 20,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 30,
            'dimension_2': 30,
            'dimension_3': 30,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 40,
            'dimension_2': 40,
            'dimension_3': 40,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 60,
            'dimension_2': 60,
            'dimension_3': 60,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 70,
            'dimension_2': 70,
            'dimension_3': 70,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 80,
            'dimension_2': 80,
            'dimension_3': 80,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 90,
            'dimension_2': 90,
            'dimension_3': 90,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 100,
            'dimension_2': 100,
            'dimension_3': 100,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 200,
            'dimension_2': 200,
            'dimension_3': 200,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 300,
            'dimension_2': 300,
            'dimension_3': 300,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 400,
            'dimension_2': 400,
            'dimension_3': 400,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 500,
            'dimension_2': 500,
            'dimension_3': 500,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 600,
            'dimension_2': 600,
            'dimension_3': 600,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 700,
            'dimension_2': 700,
            'dimension_3': 700,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 800,
            'dimension_2': 800,
            'dimension_3': 800,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 900,
            'dimension_2': 900,
            'dimension_3': 900,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 1000,
            'dimension_2': 1000,
            'dimension_3': 1000,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 2500,
            'dimension_2': 2500,
            'dimension_3': 2500,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 5000,
            'dimension_2': 5000,
            'dimension_3': 5000,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 7500,
            'dimension_2': 7500,
            'dimension_3': 7500,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
        {
            'dimension_1': 10000,
            'dimension_2': 10000,
            'dimension_3': 10000,
            'statements': [
                {
                    'number': 1,
                    'statement': STATEMENT_1
                },
                {
                    'number': 2,
                    'statement': STATEMENT_2
                },
                {
                    'number': 3,
                    'statement': STATEMENT_3
                },
                {
                    'number': 4,
                    'statement': STATEMENT_4
                }
            ],
            'ignore': False
        },
    ]
}
