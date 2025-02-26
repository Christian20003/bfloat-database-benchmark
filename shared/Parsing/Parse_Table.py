import numpy as np
import re

def parse_table_output(output: str, total_columns: int, start: int, stop: int) -> np.ndarray:
    '''
    This function parses the table output of the database into numpy array. This function
    only works if all columns are numeric values.

    :param output: The output string from the database executable.
    :param total_columns: The number of output columns. 
    :param start: The first column which should be extracted.
    :param stop: The last column which should be extracted.

    :return: A numpy array containing all extracted values.
    '''
    
    print('Parse the output into correct format')
    output = output.decode('utf-8')
    end = output.index('{')
    database_result = re.findall(r'-?\d+\.\d+|-?\d+', output[:end])
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