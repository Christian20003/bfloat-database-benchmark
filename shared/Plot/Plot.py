import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Csv')))

from Transform import transform_data
from Plot_Time import plot_time_multiple
from Plot_Memory import plot_memory_multiple
from Csv import read_data_from_csv

def plot_results(x_label: str):
    data = read_data_from_csv()
    data = transform_data(data)
    plot_time_multiple(data, x_label)
    plot_memory_multiple(data, x_label)