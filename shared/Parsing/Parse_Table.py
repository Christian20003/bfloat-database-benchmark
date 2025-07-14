from typing import List
import numpy as np
import re
import json

def output_to_numpy(database_name: str, output: str, total_columns: int, relevant_columns: List[int]) -> np.ndarray:
    '''
    This function parses the database output into a numpy array.

    :param database_name: The name of the database.
    :param output: The output of the database.
    :param total_columns: The number of columns in the output.
    :param relevant_columns: The number of the columns which should be considered in the resulting array.

    :returns: The output as numpy array.
    '''
    
    output = output.decode('utf-8')
    if database_name == 'duckdb':
        return raw_to_numpy(output, relevant_columns, 1, 0)
    if database_name == 'umbra':
        return raw_to_numpy(output, relevant_columns, 0, 0)
    if database_name == 'postgres':
        return raw_to_numpy(output, relevant_columns, 1, 2)
    if database_name == 'lingodb':
        return raw_to_numpy(output, relevant_columns, 2, 4)

def json_to_numpy(output: str, relevant_columns: List[int]) -> np.ndarray:
    '''
    This function parses a json output from a database into a numpy array by
    considering only specified columns.

    :param output: The json output of the database.
    :param relevant_columns: The columns wich should be extracted.

    :returns: The output as numpy array. 
    '''

    json_obj = json.loads(output)
    json_obj = json.loads(json.dumps(sorted(json_obj, key=custom_sort)))
    result = []
    for item in json_obj:
        index = 0
        row = []
        for _, value in item.items():
            if index in relevant_columns:
                row.append(float(value))
            index += 1
        if len(row) != 0:
            result.append(row)
    return np.array(result)

def raw_to_numpy(output: str, relevant_columns: List[int], ignore_lines_start: int, ignore_lines_end: int) -> np.ndarray:
    '''
    This function parses a box-string output from a database into a numpy array by
    considering only specified columns.

    :param output: The json output of the database.
    :param relevant_columns: The columns wich should be extracted.
    :param ignore_lines_start: How many lines of the output at the beginning should be ignored.
    :param ignore_lines_end: How many lines of the output at the end should be ignored.

    :returns: The output as numpy array. 
    '''
    
    lines = output.splitlines()
    lines = [entry for idx, entry in enumerate(lines) if ignore_lines_start < idx < len(lines) - ignore_lines_end]
    table = [re.findall(r'-?\d+\.\d+e[+-]?\d+|-?\d+\.\d+|-?\d+', line) for line in lines]
    table = [entry for entry in table if len(entry) != 0]
    table = sorted(table, key=lambda x: int(x[0]))
    result = []
    for idx, column in enumerate(table):
        result.append([float(column[i]) for i in relevant_columns])
    return np.array(result)

def custom_sort(item: dict) -> int:
    first_key = list(item.keys())[0]
    return item[first_key]