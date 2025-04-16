from typing import List
import csv

def create_csv_file(file_name: str, header: List[str]) -> None:
    '''
    This function creates a new CSV file or overrides an existing CSV file.

    :param file_name: The name of the CSV file (with path).
    :param header: A list of headers of the CSV file.
    '''

    with open(file_name, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(header)

def append_row(file_name: str, data: List[str]) -> None:
    '''
    This function appends a row to a CSV file.

    :param file_name: The name of the CSV file (with path).
    :param data: A list of data which represents a single row in the CSV file.
    '''
    
    with open(file_name, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(data)