from typing import List
from Csv import read_data_from_csv
import matplotlib.pyplot as plt

# ['Name', 'Type', 'Points', 'QOpt', 'lowerRelAlg', 'lowerSubOp', 'lowerDB', 'lowerDSA', 'lowerToLLVM', 'toLLVMIR', 'llvmOptimize', 'llvmCodeGen', 'executionTime', 'total']
def transform_data(data: List[List[str]]):
    print('Transform relevant data')
    result = {}
    types = []
    types = [element[1] for element in data if element[1] not in types]
    for type in types:
        entries = [element for element in data if element[1] == type]
        entries = sorted(entries, key=lambda x: int(x[2]))
        x_values = [int(element[2]) for element in entries]
        y_compiler = [sum(float(element[i]) for i in range(3, 12)) for element in entries]
        y_exec = [float(element[12]) for element in entries]
        y_total = [float(element[13]) for element in entries]
        result.update({
            type: {
                'x_values': x_values,
                'y_compiler': y_compiler,
                'y_exec': y_exec,
                'y_total': y_total
            }
        })
    return result

def plot(data: dict):
    print('Plotting the results into performance.pdf')
    colors = ['r', 'b', 'g', 'c', 'y', 'm']
    color_index = 0
    for key, value in data.items():
        plt.plot(value['x_values'], value['y_compiler'], linestyle='--', color=colors[color_index], marker='o')
        plt.plot(value['x_values'], value['y_exec'], linestyle=':', color=colors[color_index], marker='o')
        plt.plot(value['x_values'], value['y_total'], linestyle='-', color=colors[color_index], marker='o')
        plt.plot([], [], color=colors[color_index], label=f'Type: {key}')
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
    plot(data)