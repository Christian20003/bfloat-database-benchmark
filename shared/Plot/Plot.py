import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Csv')))

from typing import List
from Read_CSV import read_csv_file
from Create_Plot import plot_data
import itertools

def get_unique_values(key: str, data: dict) -> List[str]:
    '''
    This function extracts all unique options for a specified key in the data dictionary.

    :param key: The name of the key which stores the possible value.
    :param data: The data which includes all information from a CSV file.

    :returns: A list of all possible values for that key, occuring in the data dictionary.
    '''

    result = []
    for _, value in data.items():
        if value[key] not in result:
            result.append(value[key])
    return result

def get_key_values(keys: List[str], data: dict) -> List[dict]:
    '''
    This function extracts all possible options for the specifed keys in the data dictionary.
    Every option from one key will be mapped with all other options from different keys. An element
    will have the following structure: \n
        {
            key_1_name: key_1_value_1,
            key_2_name: key_2_value_1,
        }

    :param keys: A list including all keys that should be considered.
    :param data: The data which includes all information from a CSV file.

    :returns: A list of dictionaries representing each possible value combination
              of these different keys. 
    '''

    values = [get_unique_values(key, data) for key in keys]
    merged_tuples = list(itertools.product(*values))
    merged_lists = [list(combination) for combination in merged_tuples]
    result = []
    for combination in merged_lists:
        key_data = {}
        for idx, key in enumerate(keys):
            key_data.update({key: combination[idx]})
        result.append(key_data)
    return result

def extract_coordinate_values(keys: List[str], data_keys: dict, data: dict) -> List:
    '''
    This function extracts all values for a specific axis. This will add up all the values 
    stored in the specified keys.

    :param keys: A list of keys that stores values which should be added to an axis value.
    :param data_keys: A dictionary which includes all key features that specific entities from
                      the data dictionary must fulfill to be recognized.
    :param data: The data which includes all information from a CSV file.

    :returns: A List of all extracted values for an axis.
    '''
    
    result = []
    for entry_key, entry_value in data.items():
        valid = all(entry_value[data_key] == data_value for data_key, data_value in data_keys.items())
        if valid:
            value = sum(float(entry_value[key]) for key in keys)
            result.append(value)
    return result

def plot_results(data_config: dict, plot_config: dict) -> None:
    final_data = {}
    for _, value in data_config.items():
        x_keys = value['x_keys'] # Size sowie           List[str]
        y_keys = value['y_keys'] # Comp, Exe, DuckDB... dict{}
        line_keys = value['line_keys']
        data = read_csv_file(value['file'])
        key_combinations = get_key_values(line_keys, data)
        for combination in key_combinations:
            for y_name, y_key in y_keys.items():
                try:
                    x_values = extract_coordinate_values(x_keys, combination, data)
                    y_values = extract_coordinate_values(y_key, combination, data)
                    y_values = [value/(1024*1024*1024) for value in y_values]
                    sorted_values = sorted(zip(x_values, y_values))
                    x_values, y_values = zip(*sorted_values)
                    label = ' '.join(f'{key}: {combination[key]}' for key in line_keys)
                    label = label + f' in {y_name}'
                    final_data.update({
                        label: {
                            'x': list(x_values),
                            'y': list(y_values),
                            'diff_color': True,
                            'diff_style': False
                        }
                    })
                except ValueError:
                    continue
    plot_data(final_data, plot_config['x_label'], plot_config['y_label'], plot_config['file_name'])

if __name__ == "__main__":
    data = {
        'file_1': {
            'file': './test.csv',
            'line_keys': ['Type'],
            'x_keys': ['Size'],
            'y_keys': {
                'LingoDB': ['TotalMemory'],
                'DuckDB': ['DuckDBMemory']
            }
        }
    }
    config = {
        'x_label': 'Number of tuples',
        'y_label': 'Memory in GB',
        'file_name': 'Execution.pdf'
    }
    plot_results(data, config)
