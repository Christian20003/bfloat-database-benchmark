import matplotlib.pyplot as plt

COLORS = ['maroon', 'cornflowerblue', 'forestgreen', 'orange', 'mediumorchid', 'yellow']
STYLES = ['solid', 'dotted', 'dashed', 'dashdot', (0, (3, 5, 1, 5, 1, 5))]
MARKERS = ['o', '^', 's', '*','v']

def plot_data(data: dict, x_label: str, y_label: str, file_name: str, legend_loc: str = 'lower left', x_as_log: bool = True, y_as_log: bool = False) -> None:
    '''
    This function plots some given data with the help of matplotlib. An entry of the data should have the following structure:
        label_name:
            x: List[number]
            y: List[number]
            color: str
            style: str
            marker: str
    
    :param data: The dictionary containing all data described above.
    :param x_label: The label of the x-axis.
    :param y_label: The laben of the y-axis.
    :param file_name: The name of the file where this plot should be stored.
    :param legend_loc: The position of the plot legend (use syntax of matplotlib) (Default: upper left)
    :param x_as_log: If the x-axis should be as logerithmic scale (Default: True)
    :param y_as_log: If the y-axis should be as logerithmic scale (Default: False)
    '''

    f = plt.figure()
    f.set_figwidth(12)
    f.set_figheight(8)
    ylimit = 0
    y_max = 0
    for key, value in data.items():
        plt.plot(value['x'], value['y'], color=value['color'], linestyle=value['style'], marker=value['marker'], label=key, linewidth=2)
        ylimit = max(value['y']) / 10 if max(value['y']) / 10 > ylimit else ylimit
        y_max = max(value['y'])
    columns = 4
    mode = 'expand' if len(data) > 4 else 'default'
    plt.tick_params(which='minor', bottom=False, top=False, left=False, right=False)
    plt.legend(loc=legend_loc, bbox_to_anchor=(0, 1, 1, 0.2), mode=mode, ncol=columns, fontsize=10, handletextpad=0.5)
    plt.subplots_adjust(left=0.15, right=0.85, top=0.75, bottom=0.15)
    plt.ylim(bottom=-ylimit)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if x_as_log:
        plt.xscale('log')
    if y_as_log:
        plt.yscale('log')
    plt.savefig(file_name)
    #plt.show()
    plt.clf()