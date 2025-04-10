import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Csv')))

from typing import List
from Read_CSV import read_csv_file

def get_unique_values(key: str, data: dict) -> List[str]:
    result = []
    for key, value in data:
        if value[key] not in result:
            result.append(value[key])
    return result

def plot_results(config: dict, keys: List[str], sub_keys: List[str], merged_values: List[List[str]]) -> None:
    for key, value in config:
        file_name = value['file']
        line_keys = value['line_keys'] # List[str] -> siehe iris
        x_keys = value['x_keys'] # Size sowie 
        y_keys = value['y_keys'] # Comp, Exe, DuckDB...
    data = read_csv_file(file_name)
    unique_values = [get_unique_values(key) for key in keys]


if __name__ == "__main__":
    plot_results('./test.csv', ['Type'])
