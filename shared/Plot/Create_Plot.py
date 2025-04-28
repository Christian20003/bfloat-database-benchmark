import matplotlib.pyplot as plt

COLORS = ['maroon', 'cornflowerblue', 'forestgreen', 'orange', 'mediumorchid']
STYLES = ['solid', 'dashed', 'dotted', 'dashdot', (0, (3, 5, 1, 5, 1, 5))]

def plot_data(data: dict, x_label: str, y_label: str, file_name: str, legend_loc: str = 'lower left', x_as_log: bool = True, y_as_log: bool = False) -> None:
    '''
    This function plots some given data with the help of matplotlib. An entry of the data should have the following structure:
        label_name:
            x: List[number]
            y: List[number]
            diff_color: bool
            diff_style: bool
    
    :param data: The dictionary containing all data described above.
    :param x_label: The label of the x-axis.
    :param y_label: The laben of the y-axis.
    :param file_name: The name of the file where this plot should be stored.
    :param legend_loc: The position of the plot legend (use syntax of matplotlib) (Default: upper left)
    :param x_as_log: If the x-axis should be as logerithmic scale (Default: True)
    :param y_as_log: If the y-axis should be as logerithmic scale (Default: False)
    '''

    color_idx = 0
    style_idx = 0
    for key, value in data.items():
        plt.plot(value['x'], value['y'], color=COLORS[color_idx], linestyle=STYLES[style_idx], marker='o', label=key)
        if value['diff_color']:
            color_idx += 1
        if value['diff_style']:
            style_idx += 1
        if color_idx > len(COLORS):
            color_idx = 0
        if style_idx > len(STYLES):
            style_idx = 0
    columns = 1 if len(data) < 2 else 4
    plt.legend(loc=legend_loc, bbox_to_anchor=(0, 1, 1, 0.2), mode='expand', ncol=columns)
    plt.ylim(bottom=0)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if x_as_log:
        plt.xscale('log')
    if y_as_log:
        plt.yscale('log')
    plt.savefig(file_name)