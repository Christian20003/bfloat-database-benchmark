import sys

sys.path.append('../Csv')

from Transform import transform_data
from Plot_Time import plot_time_multiple
from Plot_Memory import plot_memory_multiple
from Csv import read_data_from_csv

def plot_results():
    data = read_data_from_csv()
    data = transform_data(data)
    plot_time_multiple(data)
    plot_memory_multiple(data)