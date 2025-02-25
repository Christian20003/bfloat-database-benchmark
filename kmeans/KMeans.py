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
from Format import color
from sklearn.cluster import KMeans
import numpy as np
import random
import subprocess
import os
import time

def main():
    args = parse_args()
    types = CONFIG['types']
    iterations = CONFIG['iterations']
    init_csv_file()
    # Iterate over all cluser benchmarks
    for key, value in CONFIG.items():
        if 'cluster' not in key:
            continue
        print(f'{color.BOLD}### START BENCHMARKING KMEANS WITH {value["number"]} POINTS ###{color.END}\n')
        points = generate_points(value["number"], value["x_upper_bound"], value["y_upper_bound"], value["x_lower_bound"], value["y_lower_bound"])
        cluster = generate_points(value["cluster"], value["x_upper_bound"], value["y_upper_bound"], value["x_lower_bound"], value["y_lower_bound"])
        # Iterate over all specified types
        for type in types:
            print(f'{color.BLUE}Execute benchmark with type: {type}{color.END}')
            create_tables(points, cluster, type, args)
            output = time_benchmark(args)
            results = parse_time_metrics(output, value['cluster'])
            clusters = parse_table_output(output)
            memory_benchmark(args)
            results = parse_memory_metrics(results)
            write_to_csv(results, type, value['number'])
            evaluate_accuray(points, cluster, clusters, iterations, type)
        print('\n')
    plot_results()

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
    print(f'Generate {number} random points')
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

def create_tables(points: List[Point], clusters: List[Point], type: str, paths: Tuple[str, str, str]):
    '''
    This function creates the persistent tables for the randomly generates points and clusters.

    :param points: A list of randomly created points.
    :param clusters: A list of randomly created cluster centers.
    :param type: The current datatype.
    :param paths: A tuple with the path to the executable.

    :raise RuntimeError: If the tables could not be generated.
    '''
    
    print(f'Create Point-table with {len(points)} entries and Cluster-table with {len(clusters)} entries.')
    remove_tables(paths)
    # Define all statements to create tables with the help of LingoDB
    persist = 'SET persist=1;\n'
    create_points = f'CREATE TABLE Points(id int, x {type}, y {type});\n'
    create_clusters = f'CREATE TABLE Clusters_0(id int, x {type}, y {type});\n'
    insert_clusters = f'{points_to_sql(clusters, "Clusters_0")}\n'
    number_tuples = len(points) if len(points) <= 1000 else 1000
    database = subprocess.Popen(
        [f'{paths[0]}/sql', paths[1]], 
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
        if ((index + number_tuples)*100/len(points)) % 10 == 0:
            print(f'\t{(index + number_tuples)*100/len(points)}% tuples inserted')
    _, error = database.communicate()
    if error:
        raise RuntimeError(f'{color.RED}Something went wrong by creating the table: \n {error}{color.END}')
    print('Tables generated and filled successfully')

def remove_tables(paths: Tuple[str, str, str]):
    '''
    This function removes all table files which stores the randomly created points and cluster centers

    :param paths: A tuple with the path to the directory of the persistent database.

    :raise RuntimeError: If the corresponding files could not be removed. 
    '''
    
    try:
        os.unlink(os.path.join(paths[1], 'points.arrow'))
        os.unlink(os.path.join(paths[1], 'points.arrow.sample'))
        os.unlink(os.path.join(paths[1], 'points.metadata.json'))
    except FileNotFoundError:
        print(f'{color.YELLOW}Points table does not exist. Ignore deletion{color.END}')
    except Exception as e:
        raise RuntimeError(f'{color.RED}Failed to remove Points table files{color.END}', e)
    try:
        os.unlink(os.path.join(paths[1], 'clusters_0.arrow'))
        os.unlink(os.path.join(paths[1], 'clusters_0.arrow.sample'))
        os.unlink(os.path.join(paths[1], 'clusters_0.metadata.json'))
    except FileNotFoundError:
        print(f'{color.YELLOW}Cluster table does not exist. Ignore deletion{color.END}')
    except Exception as e:
        raise RuntimeError(f'{color.RED}Failed to remove Cluster table files{color.END}', e)
    # Ensure files are removed
    time.sleep(2)

def evaluate_accuray(points: List[Point], cluster: List[Point], result: np.ndarray, iterations: int, type: str):
    '''
    This function evaluates the precision of the database output with the KMeans algorithm of 'Sklearn'.

    :param points: The list of randomly generated points.
    :param cluster: The list of randomly generated cluster centers.
    :param result: A numpy array containing the clusters from after the database execution.
    :param iterations: The number of iterations of the KMeans algorithm.
    :param type: The datatype of the current running benchmark.
    '''

    print('Evaluate accuracy of the database output with the sklearn algorithm')
    # Prepare and execute Kmeans from sklearn
    points = points_to_numpy(points)
    cluster = points_to_numpy(cluster)
    kmeans = KMeans(n_clusters=cluster.shape[0], init=cluster, n_init=1, max_iter=iterations)
    kmeans.fit(points)
    centers = kmeans.cluster_centers_
    # Find the nearest pairs and print the solution of comparison.
    for idx, center in enumerate(centers):
        distance = np.linalg.norm(result - center, axis=1)
        if len(distance) == 0:
            break
        closest_index = np.argmin(distance)
        closest = result[closest_index]
        print(f'\t{color.UNDERLINE} Cluster {idx + 1} {color.END}')
        print(f'\t\tLingo-DB with {type}: {closest}')
        print(f'\t\tSklearn with float: {center}')
        value = f'{distance[closest_index]:.2f}'
        font_color = color.GREEN if value.startswith('0.00') else color.YELLOW
        print(f'\t\t{font_color} Distance: {distance[closest_index]:.2f} {color.END}')
        result = np.delete(result, closest_index, axis=0)

if __name__ == "__main__":
    main()
