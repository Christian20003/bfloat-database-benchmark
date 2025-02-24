from typing import List
from Csv import read_data_from_csv
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import numpy as np

COLORS = ['r', 'b', 'g', 'c']
STYLES = ['-', ':', '--', '-']
TIME_FILE_NAMES = ['Execution.pdf', 'Compilation.pdf', 'TotalTime.pdf']
MEMORY_FILE_NAMES = ['Heap.pdf', 'Stack.pdf', 'TotalMemory.pdf']

# Expected header:
# ['Name', 'Type', 'Size', 'QueryOptimization', 'LowerRelAlgDialect', 'LowerSubOpDialect', 'LowerDBDialect', 'LowerDSADialect', 'LowerToLLVMDialect', 'ToLLVMIR', 'LlvmOptimize', 'LlvmCodeGen', 'ExecutionTime', 'TotalTime', 'Heap', 'Stack', 'TotalMemory']
def transform_data(data: List[List[str]]):
    '''
    This function transforms the given data into a more processable format (for matplotlib).
    The resulting dictionary will include each type with multiple arrays representing
    x and y values.

    :param data: A list of entries from a csv file.

    :return: A dictionary containing all relevant data according time and memory in an array
             like structure.
    '''
    print('Transform relevant data')
    result = {}
    # Identify all tested types
    types = [element[1] for element in data if element[1] not in types]
    for type in types:
        # Identify all entries belonging to the current type
        entries = [element for element in data if element[1] == type]
        entries = sorted(entries, key=lambda x: int(x[2]))
        # Identify all x and y values and merge them into a single array
        x_values = [int(element[2]) for element in entries]
        y_compiler = [sum(float(element[i]) for i in range(3, 12)) for element in entries]
        y_exec = [float(element[12]) for element in entries]
        y_total_time = [float(element[13]) for element in entries]
        y_heap = [float(element[14]) / 1024^2 for element in entries]
        y_stack = [float(element[15]) / 1024^2 for element in entries]
        y_total_memory = [float(element[16]) / 1024^2 for element in entries]
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
    return result

def plot_time_multiple(data: dict):
    '''
    This function generates for each result attribute according to time a single plot stored 
    in a seperate file (One plot for compilation, execution and total).

    :param data: The dictionary containing all pre-processed data.
    '''
    for index, result in enumerate(TIME_FILE_NAMES):
        data_key = 'y_exec' if index == 0 else 'y_compiler' if index == 1 else 'y_total_time'
        style_index = 0
        for key, value in data.items():
            # smooth the curve
            x = np.array(value['x_values'])
            y = np.array(value[data_key])
            spline = make_interp_spline(x, y)
            x_new = np.linspace(x.min(), x.max(), 300)
            y_new = spline(x_new)
            # plot the data
            plt.plot(x_new, y_new, linestyle=STYLES[style_index], color=COLORS[style_index], marker='o', label=f'Type: {key}')
        plt.legend(loc='lower left', bbox_to_anchor=(0, 1, 1, 0.2), mode='expand', ncol=4)
        plt.xlabel('Number of points')
        plt.ylabel('Time in ms')
        plt.xscale('log')
        plt.savefig(result)

def plot_memory_multiple(data: dict):
    '''
    This function generates for each result attribute according to memory a single plot stored 
    in a seperate file (One plot for heap, stack and total).

    :param data: The dictionary containing all pre-processed data.
    '''
    for index, result in enumerate(TIME_FILE_NAMES):
        data_key = 'y_heap' if index == 0 else 'y_stack' if index == 1 else 'y_total_memory'
        style_index = 0
        for key, value in data.items():
            # smooth the curve
            x = np.array(value['x_values'])
            y = np.array(value[data_key])
            spline = make_interp_spline(x, y)
            x_new = np.linspace(x.min(), x.max(), 300)
            y_new = spline(x_new)
            # plot the data
            plt.plot(x_new, y_new, linestyle=STYLES[style_index], color=COLORS[style_index], marker='o', label=f'Type: {key}')
        plt.legend(loc='lower left', bbox_to_anchor=(0, 1, 1, 0.2), mode='expand', ncol=4)
        plt.xlabel('Number of points')
        plt.ylabel('Used memory in MB')
        plt.xscale('log')
        plt.savefig(result)

def plot_time_single(data: dict):
    print('Plotting the results into performance.pdf')
    color_index = 0
    for key, value in data.items():
        plt.plot(value['x_values'], value['y_compiler'], linestyle='--', color=COLORS[color_index], marker='o')
        plt.plot(value['x_values'], value['y_exec'], linestyle=':', color=COLORS[color_index], marker='o')
        plt.plot(value['x_values'], value['y_total_time'], linestyle='-', color=COLORS[color_index], marker='o')
        plt.plot([], [], color=COLORS[color_index], label=f'Type: {key}')
        color_index += 1
    plt.plot([], [], linestyle='--', color='k', label='Compilation')
    plt.plot([], [], linestyle=':', color='k', label='Execution')
    plt.plot([], [], linestyle='-', color='k', label='Total')
    plt.legend(loc='lower left', bbox_to_anchor=(0, 1, 1, 0.2), mode='expand', ncol=4)
    plt.xlabel('Number of points')
    plt.ylabel('Time in ms')
    plt.xscale('log')
    plt.savefig('performance.pdf')
    #plt.show()

def plot_results():
    data = read_data_from_csv()
    data = transform_data(data)
    plot_time_multiple(data)
    plot_memory_multiple(data)