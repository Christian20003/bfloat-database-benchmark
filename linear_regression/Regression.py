import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))

from typing import List, Tuple
from Config import CONFIG, STATEMENT
import random
import Format
import Helper
import Database
import Create_CSV
import numpy as np
import tensorflow as tf

def main():
    databases = CONFIG['databases']
    scenarios = CONFIG['setups']

    for database in databases:
        if database['create_csv']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    for scenario in scenarios:
        if scenario['ignore']:
            continue
        generate_statement(scenario['lr'], CONFIG['iterations'])
        slope, intercept = generate_regression_line(scenario['max'], scenario['min'])
        points = generate_points(scenario['p_amount'], scenario['max'], scenario['min'], slope, intercept)
        points = normalize_points(points)
        for database in databases:
            for type in database['types']:
                prep_database = Database.Database(database['execution'], database['start_sql'], database['end_sql'])
                prep_database.create_table('points', ['x', 'y'], [type, type])
                prep_database.insert_from_csv('points', './points.csv', ['x', 'y'], points)
                prep_database.execute_sql()

                time = 0
                memory = 0

                tf_slope, tf_intercept = regression_tensorflow(points, scenario['lr'], CONFIG['iterations'], type)
                db_mape, tf_mape = evaluate_accuray(points, _, _, tf_slope, tf_intercept, type)

                Create_CSV.append_row(database['csv_file'], [time, memory])
                Helper.remove_files(database['files'], './')

def generate_statement(learning_rate: float, iterations: int) -> None:
    '''
    This function generates the SQL file.

    :param iterations: The number of iterations in the recursive CTE.
    :param learning_rate: The learning rate for the grandient descent algorithm.
    '''

    with open('./Statement.sql', 'w') as file:
        file.write(STATEMENT.format(learning_rate, learning_rate, iterations, iterations))

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


def generate_points(number: int, upper_bound: int, lower_bound: int, slope: float, intercept: float) -> List[List[float]]:
    '''
    This function generates a specified number of random points near a regression line.
    It will further add a random error to the y label.

    :param number: The number of points.
    :param upper_bound: The maximum value for the x value.
    :param lower_bound: The minimum value for the x value.
    :param slope: The slope of the regression line.
    :param intercept: The offset of the regression line.

    :return: A list of point objects.
    '''

    result = []
    for value in range(number):
        x = "{:.4f}".format(random.uniform(upper_bound, lower_bound))
        error = "{:.4f}".format(random.uniform(upper_bound / 10, lower_bound / 10))
        y = slope * float(x) + float(intercept) + float(error)
        result.append([x, y])
    return result

def normalize_points(points: List[List[float]]) -> List[List[float]]:
    '''
    This function normalizes all x values from each point based on the maximum and minimum x values.

    :param points: A list of points which should be normalized.

    :returns: A list of normalized points.
    '''

    max = max([entry[0] for entry in points])
    min = min([entry[0] for entry in points])
    return [[((entry[0] - min) / (max - min)), entry[1]] for entry in points]
    
def regression_tensorflow(points: List[List[float]], learning_rate: float, iterations: int, type: str) -> Tuple[float, float]:
    '''
    This function calculates the regression line parameters with tensorflow.

    :param points: The points for the regression problem.
    :param learning_rate: The learning rate for the simple gradient descent algorithm.
    :param iterations: The number of update iterations.
    :param type: The datatype for x and y values.

    :returns: The calculated slope and intercept of the regression line.
    '''

    datatype = tf.bfloat16 if type == 'tfloat' else tf.float32
    tf_X = tf.constant([entry[0] for entry in points], datatype)
    tf_Y = tf.constant([entry[1] for entry in points], datatype)
    slope = tf.Variable(1.0)
    intercept = tf.Variable(1.0)
    lr = tf.Variable(learning_rate)

    for _ in range(iterations):
        Y_pred = slope * tf_X + intercept
        loss = Y_pred - tf_Y
        dev_slope = tf.reduce_mean(2 * tf_X * loss)
        dev_intercept = tf.reduce_mean(2 * loss)
        slope = slope - lr * dev_slope
        intercept = intercept - lr * dev_intercept

    return slope.numpy(), intercept.numpy()

def evaluate_accuracy(points: List[List[float]], slope_db: float, intercept_db: float, slope_tf: float, intercept_tf: float, type: str) -> Tuple[float, float]:
    '''
    This function evaluates the accuracy of the database and tensorflow by calculating the MAPE score.

    :param points: The points for the linear regression problem.
    :param slope_db: The slope of the regression line from the database.
    :param intercept_db: The offset of the regression line from the database.
    :param slope_tf: The slope of the regression line from tensorflow.
    :param intercept_tf: The offset of the regression line from tensorflow.
    :param type: The datatype of x and y values.

    :returns: Two floats containing the MAPE score of the database and tensorflow.
    '''
    
    points_X = np.array([entry[0] for entry in points])
    points_Y = np.array([entry[1] for entry in points])
    db_pred = slope_db * points_X + intercept_db
    tf_pred = slope_tf * points_X + intercept_tf

    db_mape = (1 / len(points)) * np.sum(np.absolute((points_Y - db_pred) / points_Y)) * 100
    tf_mape = (1 / len(points)) * np.sum(np.absolute((points_Y - tf_pred) / points_Y)) * 100

    slope_db_sign = '' if slope_db >= 0 else '-'
    intercept_db_sign = '' if intercept_db >= 0 else '-'
    slope_db = slope_db * -1 if slope_db < 0 else slope_db
    intercept_db = intercept_db * -1 if intercept_db < 0 else intercept_db
    Format.print_information(f'Result of Database with {type}: {slope_db_sign} {slope_db} * x {intercept_db_sign} {intercept_db}', mark=True, tabs=1)
    Format.print_information(f'It reached an accuracy of {db_mape}%', mark=True, tabs=2)

    slope_tf_sign = '' if slope_tf >= 0 else '-'
    intercept_tf_sign = '' if intercept_tf >= 0 else '-'
    slope_tf = slope_tf * -1 if slope_tf < 0 else slope_tf
    intercept_tf = intercept_tf * -1 if intercept_tf < 0 else intercept_tf
    Format.print_information(f'Result of Tensorflow with {type}: {slope_tf_sign} {slope_tf} * x {intercept_tf_sign} {intercept_tf}', mark=True, tabs=1)
    Format.print_information(f'It reached an accuracy of {tf_mape}%', mark=True, tabs=2)

    return db_mape, tf_mape

if __name__ == "__main__":
    main()
