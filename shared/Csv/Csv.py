from typing import List
import csv

FILE_NAME = 'results.csv'

def init_csv_file(additional_header: List[str]) -> None:
    '''
    This function initialize the results.csv file with a header (override previous content).

    :param addition_header: A list of headers which should be added to the csv file.
    '''

    with open(FILE_NAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = [
            'Name', 
            'Type', 
            'QueryOptimization', 
            'LowerRelAlgDialect', 
            'LowerSubOpDialect', 
            'LowerDBDialect', 
            'LowerDSADialect', 
            'LowerToLLVMDialect', 
            'ToLLVMIR', 
            'LlvmOptimize', 
            'LlvmCodeGen', 
            'ExecutionTime', 
            'TotalTime',
            'Heap',
            'Stack',
            'TotalMemory',
            'DuckDBTime',
            'DuckDBMemory'
        ]
        header = header + additional_header
        writer.writerow(header)

def write_to_csv(results: dict, name: str, type: str, additional_results: List) -> None:
    '''
    This function writes data to the result.csv file (append).

    :param results: Dictionary including all results which should be written into the file.
    :param name: The name of the benchmark.
    :param type: The data-type which corresponds to the specified results.
    :param additional_results: Furhter data which should be added to the csv file.
    '''

    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        data = [
            name,
            type,
            results['times']['QOpt'],
            results['times']['lowerRelAlg'],
            results['times']['lowerSubOp'],
            results['times']['lowerDB'],
            results['times']['lowerDSA'],
            results['times']['lowerToLLVM'],
            results['times']['toLLVMIR'],
            results['times']['llvmOptimize'],
            results['times']['llvmCodeGen'],
            results['times']['executionTime'],
            results['times']['total'],
            results['memory']['heap'],
            results['memory']['stack'],
            results['memory']['total'],
            results['duckdbt'],
            results['duckdbm']
        ]
        data = data + additional_results
        writer.writerow(data)

def read_data_from_csv() -> List[List[str]]:
    '''
    This function reads the data from results.csv
    '''
    
    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        data = [row for row in reader]
        return data
