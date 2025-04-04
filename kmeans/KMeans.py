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
from sklearn.cluster import KMeans
import numpy as np
import random
import subprocess
import os
import time

def main():
    args = parse_args('Kmeans')
    types = CONFIG['types']
    iterations = CONFIG['iterations']
    init_csv_file()
    # Iterate over all cluser benchmarks
    for key, value in CONFIG.items():
        if 'cluster' not in key:
            continue
        print_title(f'### START BENCHMARKING KMEANS WITH {value["number"]} POINTS ###')
        points = generate_points(value["number"], value["x_upper_bound"], value["y_upper_bound"], value["x_lower_bound"], value["y_lower_bound"])
        cluster = generate_points(value["cluster"], value["x_upper_bound"], value["y_upper_bound"], value["x_lower_bound"], value["y_lower_bound"])
        # Iterate over all specified types
        for type in types:
            print_information(f'Execute benchmark with type: {type}')
            create_tables(points, cluster, type, args)
            output = time_benchmark(args)
            results = parse_time_metrics(output)
            clusters = parse_table_output(output, 4, 2, 3)
            file = memory_benchmark(args, f'{type}{value['number']}')
            results = parse_memory_metrics(results, file)
            eval = evaluate_accuray(points, cluster, clusters, iterations, type)
            write_to_csv(results, 'KMeans', type, value['number'], eval)
        print('\n')
    plot_results('Number of points')

def generate_points(number: int, x_upper: int, y_upper: int, x_lower: int, y_lower: int) -> List[Point]:
    '''
    This function generates a specified number of random points.

    :param number: The number of points.
    :param x_upper: The maximum value for x.
    :param y_upper: The maximum value for y.
    :param x_lower: The minimum value for x.
    :param y_lower: The minimum value for y.

    :return: A list of point objects.
    '''

    result = []
    for value in range(number):
        x = "{:.4f}".format(random.uniform(x_lower, x_upper))
        y = "{:.4f}".format(random.uniform(y_lower, y_upper))
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

def points_to_numpy(points: List[Point]) -> np.ndarray:
    '''
    This function changes the given list of point objects to a numpy array.

    :param points: The list of points which should be converted.

    :return: All points in a 2 dimensional numpy array.
    '''

    coordinates = []
    for point in points:
        coordinates.append([point.x, point.y])
    return np.array(coordinates, dtype=float)

def create_tables(points: List[Point], clusters: List[Point], type: str, paths: dict):
    '''
    This function creates the persistent tables for the randomly generates points and clusters.

    :param points: A list of randomly created points.
    :param clusters: A list of randomly created cluster centers.
    :param type: The current datatype.
    :param paths: A dictionary with paths to all necessary executables and directories.

    :raise RuntimeError: If the tables could not be generated.
    '''
    
    print_information(f'Create Point-table with {len(points)} entries and Cluster-table with {len(clusters)} entries.')
    remove_tables(paths)
    # Define all statements to create tables with the help of LingoDB
    persist = 'SET persist=1;\n'
    create_points = f'CREATE TABLE Points(id int, x {type}, y {type});\n'
    create_clusters = f'CREATE TABLE Clusters_0(id int, x {type}, y {type});\n'
    insert_clusters = f'{points_to_sql(clusters, "Clusters_0")}\n'
    number_tuples = len(points) if len(points) <= 1000 else 1000
    database = subprocess.Popen(
        [paths['exe'], paths['storage']], 
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # Create all table and insert cluster values
    statements = [persist, create_points, create_clusters, insert_clusters]
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

def remove_tables(paths: dict):
    '''
    This function removes all table files which stores the randomly created points and cluster centers

    :param paths: A dictionary with paths to all necessary executables and directories.

    :raise RuntimeError: If the corresponding files could not be removed. 
    '''
    
    files = ['points.arrow', 'points.arrow.sample', 'points.metadata.json', 'clusters_0.arrow', 'clusters_0.arrow.sample', 'clusters_0.metadata.json']
    for file in files:
        try:
            os.unlink(os.path.join(paths['storage'], file))
        except FileNotFoundError:
            print_warning(f'{file} does not exist. Ignore deletion')
        except Exception as e:
            print_error(f'Failed to remove {file}', e)
    # Ensure files are removed
    time.sleep(2)

def evaluate_accuray(points: List[Point], cluster: List[Point], result: np.ndarray, iterations: int, type: str) -> Tuple[str, str]:
    '''
    This function evaluates the precision of the database output with the KMeans algorithm of 'Sklearn'.

    :param points: The list of randomly generated points.
    :param cluster: The list of randomly generated cluster centers.
    :param result: A numpy array containing the clusters from the database execution.
    :param iterations: The number of iterations of the KMeans algorithm.
    :param type: The datatype of the current running benchmark.

    :returns: Two strings containing the correct result from numpy and the database result.
    '''

    # Prepare and execute Kmeans from sklearn
    points = points_to_numpy(points)
    cluster = points_to_numpy(cluster)
    kmeans = KMeans(n_clusters=cluster.shape[0], init=cluster, n_init=1, max_iter=iterations)
    kmeans.fit(points)
    centers = kmeans.cluster_centers_
    correct = np.array_str(centers)
    calculation = np.array_str(result)
    # Find the nearest pairs and print the solution of comparison.
    for idx, center in enumerate(centers):
        distance = np.linalg.norm(result - center, axis=1)
        if len(distance) == 0:
            break
        closest_index = np.argmin(distance)
        closest = result[closest_index]

        value = f'{distance[closest_index]:.2f}'
        print_information(f'Cluster {idx + 1}', True, 1)
        print_information(f'Lingo-DB with {type}: {closest}', tabs=2)
        print_information(f'Sklearn with float: {center}', tabs=2)
        if value.startswith('0.00'):
            print_success(f'Distance: {distance[closest_index]:.2f}', tabs=2)
        else:
            print_warning(f'Distance: {distance[closest_index]:.2f}', tabs=2)

        result = np.delete(result, closest_index, axis=0)
    return correct, calculation


if __name__ == "__main__":
    main()
