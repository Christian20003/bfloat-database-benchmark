import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Parsing')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Types')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))

from Config import CONFIG
from Point import Point
from Plot import plot_results
from typing import List, Tuple
from Csv import init_csv_file, write_to_csv
from Parse_Args import parse_args
from Parse_Memory import parse_memory_metrics
from Parse_Time import parse_time_metrics
from Parse_Table import parse_table_output
from Execute import time_benchmark, memory_benchmark
from Format import print_warning, print_information, print_success, print_title
from Helper import remove_files, execute_sql, generate_csv, tfloat_switch
import random

def main():
    args = parse_args('Kmeans')
    types = CONFIG['types']
    init_csv_file('Size', 'correctResult', 'lingoDBResult')
    # Iterate over all benchmarks
    for key, value in CONFIG.items():
        if 'case' not in key:
            continue
        print_title(f'### START BENCHMARKING LINEAR REGRESSION WITH {value["number"]} POINTS ###')
        slope, intercept = generate_regression_line(value['param_upper_bound'], value['param_lower_bound'])
        points = generate_points(value["number"], value["param_upper_bound"], value["param_lower_bound"], slope, intercept, CONFIG['noise_std_dev'])
        for type in types:
            print_information(f'Execute benchmark with type: {type}')
            print_information(f'Create Point-table with {len(points)} entries.')
            create_lr_table(value['lr'], args)
            if type == 'tfloat':
                create_table('points', type, args)
                create_table('pointsdummy', 'float', args)
                insert_points(points, 'pointsdummy', './points.csv', args)
                tfloat_switch('points', 'pointsdummy', args)
            else:
                create_table('points', type, args)
                insert_points(points, 'points', './points.csv', args)
            output = time_benchmark(args)
            results = parse_time_metrics(output)
            values = parse_table_output(output, 3, 1, 2)
            file = memory_benchmark(args, f'{type}{value['number']}')
            results = parse_memory_metrics(results, file)
            eval = evaluate_accuracy(values[0][0], values[0][1], slope, intercept, type)
            write_to_csv(results, 'Regression', type, [value['number'], eval[0], eval[1]])
        print('\n')
    plot_results('Number of points')

def generate_regression_line(upper_bound: int, lower_bound: int) -> Tuple[float, float]:
    '''
    This function generates some random parameter for a linear regression problem (slope and offset).

    :param upper_bound: The maximum value for both parameters.
    :param lower_bound: The minimum value for both parameters.

    :return: A tuple including the slope and the offset of the generated regression line.
    '''

    slope = "{:.4f}".format(random.uniform(upper_bound, lower_bound))
    intercept = "{:.4f}".format(random.uniform(upper_bound, lower_bound))
    return float(slope), float(intercept)


def generate_points(number: int, upper_bound: int, lower_bound: int, slope: float, intercept: float, error_deviation: float) -> List[Point]:
    '''
    This function generates a specified number of random points near a regression line.
    It will further add a random error to the y label.

    :param number: The number of points.
    :param upper_bound: The maximum value for the x value.
    :param lower_bound: The minimum value for the x value.
    :param slope: The slope of the regression line.
    :param intercept: The offset of the regression line.
    :param error_deviation: The deviation of the error in a gaussian distribution.

    :return: A list of point objects.
    '''

    result = []
    for value in range(number):
        x = "{:.4f}".format(random.uniform(upper_bound, lower_bound))
        error = "{:.4f}".format(random.gauss(1, error_deviation))
        y = slope * float(x) + float(intercept) + float(error)
        result.append(Point(value, x, y))
    return result

def create_table(table_name: str, type: str, paths: dict) -> None:
    '''
    This function creates the persistent table for the randomly generates points.

    :param table_name: The name of the table.
    :param type: The current datatype.
    :param paths: A dictionary with paths to all necessary executables and directories.

    :raise RuntimeError: If the table could not be generated.
    '''
    
    files = [f'{table_name}.arrow', f'{table_name}.arrow.sample', f'{table_name}.metadata.json']
    remove_files(files, paths['storage'])

    statements = ['SET persist=1;\n', f'CREATE TABLE {table_name}(id int, x {type}, y {type});\n']
    execute_sql(statements, paths['exe'], paths['storage'])

def create_lr_table(lr: float, paths: dict) -> None:
    '''
    This function creates a learning rate table for a dynamic learning rate.

    :param lr: The learning-rate for this current case.    
    :param paths: A dictionary with paths to all necessary executables and directories.
    '''

    files = ['lr.arrow', 'lr.arrow.sample', 'lr.metadata.json']
    remove_files(files, paths['storage'])
    statements = ['SET persist=1;\n', f'CREATE TABLE lr(rate float);\n', f'INSERT INTO lr(rate) VALUES ({lr});\n']
    execute_sql(statements, paths['exe'], paths['storage'])

def insert_points(points: List[Point], table_name: str, csv_file: str, paths: dict) -> None:
    '''
    This function inserts a specific amount of points into the points table.

    :param points: The randomly generated points.
    :param table_name: The name of the table.
    :param csv_file: The file where the data is stored.
    :param paths: A dictionary with paths to all necessary executables and directories.

    :raise RuntimeError: If the dara could not be inserted.
    '''
    
    print_information(f'Inserting {len(points)} of points (This can take a while)', tabs=1)
    data = [[point.id, point.x, point.y] for point in points]
    generate_csv(csv_file, ['id', 'x', 'y'], data)
    statements = ['SET persist=1;\n']
    copy = f"copy {table_name} from '{csv_file}' delimiter ',' HEADER;\n"
    statements.append(copy)
    execute_sql(statements, paths['exe'], paths['storage'])

def evaluate_accuracy(slope_db: float, intercept_db: float, slope_label: float, intercept_label: float, type: str) -> str:
    '''
    This function evaluates the accuracy of the database result.

    :param slope_db: The slope of the regression line from the database.
    :param intercept_db: The offset of the regression line from the database.
    :param slope_label: The truth slope of the regression line.
    :param intercept_label: The truth offset of the regression line.
    :param type: The datatype of x and y values.

    :returns: Two strings containing the correct result and the database result.
    '''
    
    error_slope = str("{:.4f}".format(slope_label - slope_db))
    error_intercept = str("{:.4f}".format(intercept_label - intercept_db))

    sign_db = '+' if intercept_db > 0 else ''
    sign = '+' if intercept_label > 0 else ''
    print_information(f'The generated truth: {slope_label} * x {sign} {intercept_label}', mark=True, tabs=1)
    print_information(f'Result of Lingo-DB with {type}: {slope_db} * x {sign_db} {intercept_db}', mark=True, tabs=1)
    if error_slope.startswith('0.0000'):
        print_success(f'Slope error: {error_slope}', tabs=2)
    else:
        print_warning(f'Slope error: {error_slope}', tabs=2)
    if error_intercept.startswith('0.0000'):
        print_success(f'Intercept error: {error_intercept}', tabs=2)
    else:
        print_warning(f'Intercept error: {error_intercept}', tabs=2)
    return f'{slope_label} * x {sign} {intercept_label}', f'{slope_db} * x {sign_db} {intercept_db}'

if __name__ == "__main__":
    main()
