from typing import Tuple
import json
import re
import numpy as np

def parse_time_output(output: str, columns: int) -> Tuple[dict, np.ndarray]:
    '''
    This function parses the output of the database into a python processible structure.

    :param output: The output string from the database executable.
    :param columns: The number of output columns. 

    :return: A tuple with the performance values as dictionary and a numpy array
             containing all relevant values from the output table.
    '''
    
    print('Parse the output into correct format')
    output = output.decode('utf-8')
    # Extract json object from output string (with performance metrics)
    json_index = output.index('{')
    json_str = output[json_index:]
    json_str = json_str.replace('\t', ' ').replace('\n', ' ').replace(' ', '')
    json_obj = json.loads(json_str)
    # Extract all relevant data from output table
    database_result = re.findall(r'-?\d+\.\d+|-?\d+', output[:json_index])
    data = []
    for index in range(2, database_result.__len__(), columns):
        cluster = [float(database_result[index]), float(database_result[index + 1])]
        data.append(cluster)
    clusters = np.array(data, dtype=float)
    return (json_obj, clusters)

def parse_memory_output(results: dict) -> dict:
    heap = []
    stack = []
    with open('massif.out.kmeans', 'r') as file:
        line = file.readline()
        while line:
            index = re.findall('=', line)
            if 'mem_heap_B' in line:
                heap.append(int(line[index + 1:]))
            if 'mem_heap_extra_B' in line:
                heap[len(heap) - 1] += int(line[index + 1:])
            if 'mem_stacks_B' in line:
                stack.append(int(line[index + 1:]))
            line = file.readline()
    
    