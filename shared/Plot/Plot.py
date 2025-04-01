import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Csv')))

from Transform import transform_data
from Plot_Time import plot_time_multiple
from Plot_Memory import plot_memory_multiple
from Csv import read_data_from_csv

def plot_results(x_label: str) -> None:
    '''
    This function plots the result from result.csv into the following files:
        Time:
            - Execution
            - Compilation
            - Total
        Memory:
            - Stack
            - Heap
            - Total

    :param x_label: The name of the x-axis of each plot
    '''
    data = read_data_from_csv()
    data = transform_data(data)
    plot_time_multiple(data, x_label)
    plot_memory_multiple(data, x_label)