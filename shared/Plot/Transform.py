from typing import List, Tuple

TYPE_INDEX = 1
POINT_INDEX = 2
START_COMP_INDEX = 3
STOP_COMP_INDEX = 12
TOTAL_TIME_INDEX = 13
HEAP_INDEX = 14
STACK_INDEX = 15
TOTAL_MEMORY_INDEX = 16

def check_structure(data: List[List[str]]) -> None:
    '''
    This function checks if the incoming csv content has the correct structure.

    :param data: A list of all entries from a csv file (without header).

    :raise ValueError: If the provided content does not fulfill the requirements.
    '''
    for list in data:
        if len(list) < 17:
            raise ValueError(f'Expected a list of length 17, but got instead a list with {len(list)} entries.')

def get_unique_types(data: List[List[str]]) -> List[str]:
    '''
    This function extracts all unique types from the incoming csv content.

    :param data: A list of all entries from a csv file (without header).

    :return: A list with all unique types.
    '''
    types = []
    types = [element[TYPE_INDEX] for element in data if element[TYPE_INDEX] not in types]
    return types

def extract_entries(type: str, data: List[List[str]]) -> List[List[str]]:
    '''
    This function extracts all entries which corresponds to the provided type and sort them
    after the number of points.

    :param type: The type to which the entries should be extracted.
    :param data: A list of all entries from a csv file (without header).

    :return: A modified list from a csv file.
    '''
    entries = [element for element in data if element[TYPE_INDEX] == type]
    entries = sorted(entries, key=lambda x: int(x[POINT_INDEX]))
    return entries

def extract_time_data(data: List[List[str]]) -> Tuple[List[float], List[float], List[float]]:
    '''
    This function returns the time data for a specific type (compilation, execution and 
    total time).

    :param data: A list of entries related to a specific type from a csv file (without header).

    :return: A tuple with three elements for each time metric.
    '''
    y_compiler = [sum(float(element[i]) for i in range(START_COMP_INDEX, STOP_COMP_INDEX)) for element in data]
    y_exec = [float(element[STOP_COMP_INDEX]) for element in data]
    y_total_time = [float(element[TOTAL_TIME_INDEX]) for element in data]
    return y_compiler, y_exec, y_total_time

def extract_memory_data(data: List[List[str]]) -> Tuple[List[float], List[float], List[float]]:
    '''
    This function returns the memory data for a specific type (heap, stack and 
    total memory).

    :param data: A list of entries related to a specific type from a csv file (without header).

    :return: A tuple with three elements for each memory metric.
    '''
    gb = 1024*1024*1024
    y_heap = [float(element[HEAP_INDEX]) / gb for element in data]
    y_stack = [float(element[STACK_INDEX]) / gb for element in data]
    y_total_memory = [float(element[TOTAL_MEMORY_INDEX]) / gb for element in data]
    return y_heap, y_stack, y_total_memory

def extract_duck_db(data: List[List[str]]):
    gb = 1024*1024*1024
    y_total_time = [float(element[17]) for element in data]
    y_total_memory = [float(element[18]) / gb for element in data]
    return y_total_time, y_total_memory
 
def transform_data(data: List[List[str]]) -> dict:
    '''
    This function transforms the given data into a more processable format (for matplotlib).
    The resulting dictionary will include each type with multiple arrays representing
    x and y values.

    :param data: A list of entries from a csv file.

    :return: A dictionary containing all relevant data according time and memory in an array
             like structure.
    :raise ValueError: If the provided content does not fulfill the requirements.
    '''

    check_structure(data)
    result = {}
    types = get_unique_types(data)    
    for type in types:
        entries = extract_entries(type, data)
        x_values = [int(element[POINT_INDEX]) for element in entries]
        y_compiler, y_exec, y_total_time = extract_time_data(entries)
        y_heap, y_stack, y_total_memory = extract_memory_data(entries)
        result.update({
            type: {
                'x_values': x_values,
                'y_compiler': y_compiler,
                'y_exec': y_exec,
                'y_total_time': y_total_time,
                'y_heap': y_heap,
                'y_stack': y_stack,
                'y_total_memory': y_total_memory
            }
        })
    entries = extract_entries('float', data)
    duck_db_time, duck_db_memory = extract_duck_db(entries)
    x_values = [int(element[POINT_INDEX]) for element in entries]
    result.update({
        'duck_db': {
            'x_values': x_values,
            'y_total_time': duck_db_time,
            'y_total_memory': duck_db_memory
        }
    })
    return result