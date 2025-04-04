import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Parsing')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Plot')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Types')))

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
from Format import print_error, print_warning, print_information, print_success, print_title
import random
import subprocess
import os
import time

def main():
    args = parse_args('Kmeans')
    types = CONFIG['types']
    init_csv_file()
    # Iterate over all benchmarks
    for key, value in CONFIG.items():
        if 'case' not in key:
            continue
        print_title(f'### START BENCHMARKING LINEAR REGRESSION WITH {value["number"]} POINTS ###')
        slope, intercept = generate_regression_line(value['param_upper_bound'], value['param_lower_bound'])
        points = generate_points(value["number"], value["param_upper_bound"], value["param_lower_bound"], slope, intercept, CONFIG['noise_std_dev'])
        for type in types:
            print_information(f'Execute benchmark with type: {type}')
            create_tables(points, type, args, value['lr'])
            output = time_benchmark(args)
            results = parse_time_metrics(output)
            values = parse_table_output(output, 3, 1, 2)
            file = memory_benchmark(args, f'{type}{value['number']}')
            results = parse_memory_metrics(results, file)
            eval = evaluate_accuracy(values[0][0], values[0][1], slope, intercept, type)
            write_to_csv(results, 'Regression', type, value['number'], eval)
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

def points_to_sql(points: List[Point], table_name: str) -> str:
    '''
    This function changes the transforms list of point objects into a sql insert statement.

    :param points: The list of points which should be converted.
    :param table_name: The name of the table in which they should be inserted.

    :return: A string which defines the insert statement for all points.
    '''
    result = f'INSERT INTO {table_name}(id, x, y) VALUES '
    for idx, point in enumerate(points):
        result += point.to_sql_value()
        if idx != points.__len__() - 1:
            result += ","
    result += ";"
    return result

def create_tables(points: List[Point], type: str, paths: dict, lr: float) -> None:
    '''
    This function creates the persistent table for the randomly generates points.

    :param points: A list of randomly created points.
    :param type: The current datatype.
    :param paths: A dictionary with paths to all necessary executables and directories.
    :param lr: The learning-rate for this current case.

    :raise RuntimeError: If the table could not be generated.
    '''
    
    print_information(f'Create Point-table with {len(points)} entries.')
    remove_tables(paths)
    # Define all statements to create tables with the help of LingoDB
    persist = 'SET persist=1;\n'
    create_points = f'CREATE TABLE Points(id int, x {type}, y {type});\n'
    create_lr = f'CREATE TABLE lr(rate float);\n'
    insert_lr = f'INSERT INTO lr(rate) VALUES ({lr});\n'
    number_tuples = len(points) if len(points) <= 1000 else 1000
    database = subprocess.Popen(
        [paths['exe'], paths['storage']], 
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # Create all table and insert cluster values
    statements = [persist, create_points, create_lr, insert_lr]
    for statement in statements:
        database.stdin.write(statement)
        database.stdin.flush()
    # Insert point values. Limit to 1000 at a time, otherwise LingoDB stops working
    for index in range(0, len(points), number_tuples):
        insert = points_to_sql(points[index:index + number_tuples], "Points")
        database.stdin.write(f'{insert}\n')
        database.stdin.flush()
        # Print after some steps the progress
        inserted = (index + number_tuples)*100/len(points)
        if inserted % 10 == 0:
            print_information(f'{inserted}% tuples inserted', tabs=1)
    _, error = database.communicate()
    if error:
        print_error('Something went wrong by creating the table', error)

def remove_tables(paths: dict) -> None:
    '''
    This function removes all table files which stores the randomly created points.

    :param paths: A dictionary with paths to all necessary executables and directories.

    :raise RuntimeError: If the corresponding files could not be removed. 
    '''
    
    files = ['points.arrow', 'points.arrow.sample', 'points.metadata.json', 'lr.arrow', 'lr.arrow.sample', 'lr.metadata.json']
    for file in files:
        try:
            os.unlink(os.path.join(paths['storage'], file))
        except FileNotFoundError:
            print_warning(f'{file} does not exist. Ignore deletion')
        except Exception as e:
            print_error(f'Failed to remove {file}', e)
    # Ensure files are removed
    time.sleep(2)

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
