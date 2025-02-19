from typing import List
import csv

FILE_NAME = 'results.csv'

def init_csv_file():
    '''
    This function initialize the results.csv file with a header (override previous content).
    '''

    with open(FILE_NAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = [
            'Name', 
            'Type', 
            'Size', 
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
            'TotalMemory'
        ]
        writer.writerow(header)

def write_to_csv(results: dict, type: str, size: int):
    '''
    This function writes data to the result.csv file (append).

    :param results: Dictionary including all results which should be written into the file.
    :param type: The data-type which corresponds to the specified results.
    :param size: The size of the input data.
    '''

    print('Write results into results.csv file')
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        data = [
            'KMeans',
            type,
            str(size),
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
            results['memory']['total']
        ]
        writer.writerow(data)

def read_data_from_csv() -> List[List[str]]:
    '''
    This function reads the data from results.csv
    '''
    
    print(f'Read data from {FILE_NAME}')
    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        data = [row for row in reader]
        return data