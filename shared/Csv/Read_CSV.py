from typing import List
import csv

def process_data(header: List[str], body: List[List[str]]) -> dict:
    '''
    This function process CSV data into a dictionary format.

    :param header: A list of headers from the CSV file.
    :param body: A list of data entries from the CSV file.

    :returns: A dictionary containing all data from the CSV file. The row number defines the
    key of a specific row (beginning with 1) and inside the access of values is possible
    through the use of the header keys.
    '''
    result = {}
    for entry_idx, entry in enumerate(body):
        entry_data = {}
        for head_idx, head in enumerate(header):
            entry_data.update({
                head: entry[head_idx]
            })
        result.update({
            entry_idx + 1: entry_data
        })
    return result

def read_csv_file(file_name: str) -> dict:
    '''
    This function reads the content from the provided CSV file.

    :param file_name: The name of the file.

    :returns: A dictionary containing all data from the CSV file. The row number defines the
    key of a specific row (beginning with 1) and inside the access of values is possible
    through the use of the header keys.
    '''
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        body = [row for row in reader]
        return process_data(header, body)
