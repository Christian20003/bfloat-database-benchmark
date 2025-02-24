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
    '''
    This function parses the output of the memory benchmark into the provided results dictionary.
    The output data will be read from a generated file. The resulting dictionary will contain the
    heap, stack and total memory at the time of highest consumption.

    :param results: The dictionary containing all benchmark results.

    :return: The updated dictionary.
    '''
    print('Parse the output into correct format')
    heap = []
    stack = []
    # Extract all values
    with open('kmeans', 'r') as file:
        line = file.readline()
        while line:
            try:
                index = line.find('=')
                if 'mem_heap_B' in line:
                    heap.append(int(line[index + 1:]))
                if 'mem_heap_extra_B' in line:
                    heap[len(heap) - 1] += int(line[index + 1:])
                if 'mem_stacks_B' in line:
                    stack.append(int(line[index + 1:]))
            except ValueError:
                pass
            line = file.readline()
    # Identify max values
    results['memory'] = {}
    results['memory']['heap'] = 0
    results['memory']['stack'] = 0
    results['memory']['total'] = 0
    index = 0
    while index < len(heap):
        if heap[index] + stack[index] > results['memory']['total']:
            results['memory']['heap'] = heap[index]
            results['memory']['stack'] = stack[index]
            results['memory']['total'] = heap[index] + stack[index]
        index += 1
    return results
