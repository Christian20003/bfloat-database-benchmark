import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Csv')))

from typing import List
from Read_CSV import read_csv_file
from Create_Plot import plot_data, COLORS, STYLES, MARKERS
import itertools

def remove_entries(data: dict, ignore: dict) -> dict:
    '''
    This function removes all entries from the data dictionary which should be ignored
    in the current plot. The entries are defined in the ignore dictionary. The key of the
    ignore dictionary defines the key in the data dictionary which should be checked.
    The value of the ignore dictionary defines the possible values which should be ignored.

    :param data: The data which includes all information from a CSV file.
    :param ignore: A dictionary which defines the keys and values that should be ignored.

    :returns: The data dictionary without the ignored entries.
    '''

    if not ignore:
        return data
    for key, value in data.items():
        for ignore_key, ignore_values in ignore.items():
            if key == ignore_key and value[ignore_key] in ignore_values:
                del data[key]
    return data

def manipulate_entries(data: dict, manipulate: dict) -> dict:
    '''
    This function manipulates the entries in the data dictionary according to the
    manipulate dictionary. The key of the manipulate dictionary defines the key in the
    data dictionary which should be manipulated. The value of the manipulate dictionary
    defines the function that should be applied to the value of the key in the data
    dictionary. The manipulate dictionary should be defined in the following way:
    {
        'function': function,
        'args': [arg_1, arg_2, ...],
        'types': [type_1, type_2, ...]
    }

    :param data: The data which includes all information from a CSV file.
    :param manipulate: A dictionary which defines the keys and values that should be manipulated.

    :returns: The data dictionary with the manipulated entries.
    '''

    if not manipulate:
        return data
    for key, value in data.items():
        for manipulate_key, manipulate_values in manipulate.items():
            if key == manipulate_key:
                function = manipulate_values['function']
                types = manipulate_values['types']
                args = manipulate_values['args']
                arg_values = []
                for idx, arg in enumerate(args):
                    if types[idx] == 'int':
                        arg_values.append(int(value[arg]))
                    elif types[idx] == 'float':
                        arg_values.append(float(value[arg]))
                    else:
                        raise ValueError(f"Unsupported type: {types[idx]}")
                value[manipulate_key] = function(*arg_values)
    return data

def rename_entries(data: dict, renaming: dict) -> dict:
    '''
    This function renames the entries in the data dictionary according to the
    renaming dictionary. The key of the renaming dictionary defines the key in the
    data dictionary which should be renamed. The value of the renaming dictionary
    defines the new name of the key in the data dictionary.

    :param data: The data which includes all information from a CSV file.
    :param renaming: A dictionary which defines the keys and values that should be renamed.

    :returns: The data dictionary with the renamed entries.
    '''
    
    if not renaming:
        return data
    for key, value in data.items():
        for rename_key, rename_values in renaming.items():
            if key == rename_key:
                for idx, old_value in enumerate(rename_values['old']):
                    if value[rename_key] == old_value:
                        value[rename_key] = rename_values['new'][idx]
    return data

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
    color_idx = 0
    style_idx = 0
    marker_idx = 0
    for _, value in data_config.items():
        x_keys = value['x_keys']
        y_keys = value['y_keys']
        line_keys = value['line_keys']
        data = read_csv_file(value['file'])
        data = remove_entries(data, value['ignore'])
        data = rename_entries(data, value['renaming'])
        data = manipulate_entries(data, value['manipulate'])
        key_combinations = get_key_values(line_keys, data)
        for combination in key_combinations:
            for y_name, y_key in y_keys.items():
                try:
                    x_values = extract_coordinate_values(x_keys, combination, data)
                    y_values = extract_coordinate_values(y_key, combination, data)
                    sorted_values = sorted(zip(x_values, y_values))
                    x_values, y_values = zip(*sorted_values)
                    label = ' '.join(f'{key}: {combination[key]},' for key in line_keys)
                    label = label[:-1]
                    label = label + f' in {y_name}'
                    final_data.update({
                        label: {
                            'x': list(x_values),
                            'y': list(y_values),
                            'color': COLORS[color_idx],
                            'style': STYLES[style_idx],
                            'marker': MARKERS[marker_idx]
                        }
                    })
                except ValueError:
                    continue
                style_idx += 1
            marker_idx += 1
        color_idx += 1
    plot_data(final_data, plot_config['x_label'], plot_config['y_label'], plot_config['file_name'])

if __name__ == "__main__":
    file_name = './shared/Plot/DuckDB_Regression_Results.csv'
    scenario_name = 'Regression'
    line_keys = ['Type'] if 'Iris' not in file_name else ['Type', 'Network_Size']
    x_keys = []
    if 'Iris' in file_name:
        x_keys = ['Data_Size']
    elif 'Einstein' in file_name:
        x_keys = ['Matrix_A', 'Matrix_B', 'Vector_V']
    else:
        x_keys = ['Points']
    time = {
        'file_1': {
            'file': file_name,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['Execution'],
            },
            'renaming': {
                'Type': {
                    'old': ['float4'],
                    'new': ['float']
                }
            },
            'manipulate': {
                'Execution': {
                    'function': lambda x,y: x / y,
                    'args': ['Execution', 'Iterations'],
                    'types': ['float', 'int']
                }
            },
            'ignore': {
                'Aggregations': ['standard']
            }
        }
    }
    rss = {
        'file_1': {
            'file': file_name,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['RSS'],
            }
        }
    }
    heap = {
        'file_1': {
            'file': file_name,
            'line_keys': line_keys,
            'x_keys': x_keys,
            'y_keys': {
                'DuckDB': ['Heap'],
            }
        }
    }
    config_time = {
        'x_label': 'Number of samples',
        'y_label': 'Execution time in seconds',
        'file_name': f'Execution_{scenario_name}.pdf'
    }
    config_rss = {
        'x_label': 'Number of samples',
        'y_label': 'RSS memors in GB',
        'file_name': f'RSS_{scenario_name}.pdf'
    }
    config_heap = {
        'x_label': 'Number of samples',
        'y_label': 'Heap in GB',
        'file_name': f'Heap_{scenario_name}.pdf'
    }
    plot_results(time, config_time)
    plot_results(rss, config_rss)
    plot_results(heap, config_heap)
