import matplotlib.pyplot as plt

TIME_FILE_NAMES = {
    'y_exec': 'Execution.pdf',
    'y_compiler': 'Compilation.pdf',
    'y_total_time': 'TotalTime.pdf'
}

def plot_time_multiple(data: dict, x_label: str) -> None:
    '''
    This function generates for each result attribute according to time a single plot stored 
    in a seperate file (One plot for compilation, execution and total).

    :param data: The dictionary containing all pre-processed data.
    :param x_label: The label for the x-axis.
    '''

    colors = ['r', 'b', 'g', 'c']
    styles = ['-', ':', '--', '-']
    for y_key, file_value in TIME_FILE_NAMES.items():
        plt.clf()
        style_index = 0
        for type_key, value in data.items():
            if type_key == 'duck_db' and y_key != 'y_total_time':
                continue
            else:
                # plot the data
                plt.plot(value['x_values'], value[y_key], linestyle=styles[style_index], color=colors[style_index], marker='o', label=f'Type: {type_key}')
            style_index += 1
        plt.legend(loc='lower left', bbox_to_anchor=(0, 1, 1, 0.2))
        plt.ylim(bottom=0)
        plt.xlabel(x_label)
        plt.ylabel('Time in ms')
        plt.xscale('log')
        plt.savefig(file_value)

def plot_time_single(data: dict) -> None:
    '''
    This function generates a single plot containing all time metric values.

    :param data: The dictionary containing all pre-processed data.
    '''
    print('Plotting the results into performance.pdf')
    colors = ['r', 'b', 'g', 'c']
    color_index = 0
    plt.clf()
    for key, value in data.items():
        plt.plot(value['x_values'], value['y_compiler'], linestyle='--', color=colors[color_index], marker='o')
        plt.plot(value['x_values'], value['y_exec'], linestyle=':', color=colors[color_index], marker='o')
        plt.plot(value['x_values'], value['y_total_time'], linestyle='-', color=colors[color_index], marker='o')
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