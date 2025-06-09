import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

import DuckDB
import Umbra

HEADER = [
    'Type',
    'Rows',
    'Heaptrack-RSS',
    'Psutil-RSS',
    'Psutil-VMS'
]

duckdb = DuckDB.DUCKDB
umbra = Umbra.UMBRA
duckdb['csv_header'] = HEADER
umbra['csv_header'] = HEADER

CONFIG = {
    'databases': [
        duckdb,
        umbra
    ],
    'setups': [
        {
            'rows': 1000
        },
        {
            'rows': 10000
        },
        {
            'rows': 100000
        },
        {
            'rows': 1000000
        },
        {
            'rows': 10000000
        },
        {
            'rows': 100000000
        },
        {
            'rows': 1000000000
        }
    ]
}