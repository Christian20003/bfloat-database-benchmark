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
        return json_to_numpy(output, relevant_columns)
    if database_name == 'umbra':
        return raw_to_numpy(output, relevant_columns, 0, 0)
    if database_name == 'postgres':
        return raw_to_numpy(output, relevant_columns, 1, 2)

def json_to_numpy(output: str, relevant_columns: List[int]) -> np.ndarray:
    '''
    This function parses a json output from a database into a numpy array by
    considering only specified columns.

    :param output: The json output of the database.
    :param relevant_columns: The columns wich should be extracted.

    :returns: The output as numpy array. 
    '''

    json_obj = json.loads(output)
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
    result = [
        [float(columns[i]) for i in relevant_columns]
        for number, line in enumerate(lines)
        if ignore_lines_start < number < len(lines) - ignore_lines_end
        for columns in [re.findall(r'-?\d+\.\d+e[+-]?\d+|-?\d+\.\d+|-?\d+', line)]
    ]
    return np.array(result)

def parse_table_output(output: str, total_columns: int, start: int, stop: int) -> np.ndarray:
    '''
    This function parses the table output of the database into a numpy array. This function
    only works if all columns are numeric values. Each row will be an element in the numpy array.

    :param output: The output string from the database executable.
    :param total_columns: The number of output columns. 
    :param start: The first column which should be extracted (Start with 0).
    :param stop: The last column which should be extracted (Start with 0).

    :return: A numpy array containing all extracted values.
    '''
    
    output = output.decode('utf-8')
    end = output.index('{')
    # Extract all numbers from the output table
    database_result = re.findall(r'-?\d+\.\d+e[+-]?\d+|-?\d+\.\d+|-?\d+', output[:end])
    data = []
    for index in range(0, len(database_result), total_columns):
        if index + stop < len(database_result):
            row = []
            for entry in range(start, stop + 1):
                row.append(float(database_result[index + entry]))
            if len(row) == 1:
                data.append(row[0])
            else:
                data.append(row)
    result = np.array(data, dtype=float)
    return result
