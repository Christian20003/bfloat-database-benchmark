import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Global')))

from typing import Tuple
from Config import CONFIG, STATEMENT, STATEMENT_FILE
import random
import Format
import Database
import Create_CSV
import Memory
import Time
import Helper
import Settings
import Postgres
import numpy as np
import pandas as pd
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

def main() -> None:
    databases = CONFIG['databases']
    scenarios = CONFIG['setups']
    data_file = './data.csv'
    setup_points_file = './points.csv'
    setup_clusters_file = './clusters.csv'

    generate_points(CONFIG['max_points'], CONFIG['min'], CONFIG['max'], data_file)

    for database in databases:
        if database['create_csv']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    for scenario in scenarios:
        if scenario['ignore']:
            continue
        generate_points(scenario['c_amount'], CONFIG['min'], CONFIG['max'], setup_clusters_file)
        for database in databases:
            if database['ignore']:
                continue
            for type in database['types']:
                for agg in database['aggrations']:
                    print_setting(scenario['p_amount'], scenario['c_amount'], database['name'], type, scenario['iterations'], agg)
                    generate_statement(scenario['iterations'], agg)
                    prepare_benchmark(database, type, scenario['p_amount'], data_file, setup_points_file, setup_clusters_file)

                    time, output = Time.benchmark(database['execution-bench'], database['name'], 4, [2,3])
                    heap, rss = Memory.benchmark(database['name'], database['execution-bench'], f'{database["name"]}_{type}_{scenario["p_amount"]}_{scenario["c_amount"]}_{agg}', [])

                    tf_output = kmeans_tensorflow(setup_points_file, setup_clusters_file, scenario['iterations'], type)
                    tf_reference = kmeans_tensorflow(setup_points_file, setup_clusters_file, scenario['iterations'], 'double')
                    accuracy_db, accuracy_tf = evaluate_accuray(tf_output, output, tf_reference, CONFIG['min'], CONFIG['max'])

                    Create_CSV.append_row(database['csv_file'], [
                        type, 
                        scenario["p_amount"], 
                        scenario["c_amount"], 
                        agg,
                        scenario['iterations'], 
                        time, 
                        heap, 
                        rss, 
                        accuracy_db,
                        accuracy_tf, 
                        output, 
                        tf_output,
                        tf_reference
                    ])
                    if database['name'] == 'postgres' or database['name'] == 'umbra':
                        Helper.remove_dir(database['files'])
                    else:
                        Helper.remove_files(database['files'])
    Helper.remove_files([setup_points_file, setup_clusters_file, STATEMENT_FILE])

def prepare_benchmark(database: dict, type: str, number_points: int, data_file: str, setup_points_file: str, setup_clusters_file: str) -> None:
    '''
    This function prepares the benchmark by creating the database and inserting the data.

    :param database: The database name.
    :param type: The datatype for x and y values.
    :param number_points: The number of points.
    :param data_file: The name of the csv file where the points are stored.
    :param setup_points_file: The name of the setup points file.
    :param setup_clusters_file: The name of the setup clusters file.
    '''

    Format.print_information('Preparing benchmark - This can take some time', mark=True)
    Helper.copy_csv_file(data_file, setup_points_file, number_points + 1)  
    extend_file_path = '.' if database['name'] == 'postgres' else ''
    if database['name'] == 'postgres':
        os.mkdir(Settings.POSTGRESQL_DIR)
        executables = database['prep']
        Postgres.create_database(executables[0], executables[1], executables[2])
    elif database['name'] == 'umbra':
        os.mkdir(Settings.UMBRA_DIR)
    
    prep_database = Database.Database(database['execution'], database['start-sql'], database['end-sql'])
    prep_database.create_table('points', ['id', 'x', 'y'], ['int', type, type])
    prep_database.create_table('clusters_0', ['id', 'x', 'y'], ['int', type, type])
    prep_database.insert_from_csv('points', extend_file_path + setup_points_file)
    prep_database.insert_from_csv('clusters_0', extend_file_path + setup_clusters_file)
    prep_database.execute_sql()

def print_setting(points: int, clusters: int, database: str, type: str, iterations: int, agg_func: str) -> None:
    '''
    This function prints the settings for the current benchmark.

    :param points: The number of points.
    :param clusters: The number of clusters.
    :param database: The database name.
    :param type: The datatype for x and y values.
    :param iterations: The number of update iterations.
    :param agg_func: The aggregation function to be used in the recursive CTE.
    '''
    Format.print_title(f'START BENCHMARK - KMEANS WITH THE FOLLOWING SETTINGS')
    Format.print_information(f'Points: {points}', tabs=1)
    Format.print_information(f'Clusters: {clusters}', tabs=1)
    Format.print_information(f'Database: {database}', tabs=1)
    Format.print_information(f'Type: {type}', tabs=1)
    Format.print_information(f'Iterations: {iterations}', tabs=1)
    Format.print_information(f'Aggregation Function: {agg_func}', tabs=1)

def generate_points(number: int, min: int, max: int, file_name: str) -> None:
    '''
    This function generates a specified number of random points.
    Finally all points will be written into the given csv file.

    :param number: The number of points.
    :param min: The maximum value for x and y.
    :param max: The minimum value for x and y.
    :param file_name: The name of the csv file.

    :return: A list of point objects.
    '''

    result = []
    for value in range(number):
        result.append([value, random.uniform(min, max), random.uniform(min, max)])
    Create_CSV.create_csv_file(file_name, ['id', 'x', 'y'])
    Create_CSV.append_rows(file_name, result)
    result.clear()

def generate_statement(iterations: int, agg_func: str) -> None:
    '''
    This function generates the SQL file.

    :param iterations: The number of iterations in the recursive CTE.
    :param agg_func: The aggregation function to use.
    '''

    agg_func = 'AVG' if agg_func == 'standard' else 'FAVG'
    with open(STATEMENT_FILE, 'w') as file:
        file.write(STATEMENT.format(agg_func, agg_func, iterations, iterations))

def kmeans_tensorflow(points_csv: str, cluster_csv: str, iterations: int, type: str) -> np.ndarray:
    '''
    This function implements the kmeans algorithm with tensorflow.

    :param points_csv: The name of the csv file where the points are stored.
    :param cluster_csv: The name of the csv file where the clusters are stored.
    :param iterations: The number of iterations.
    :param type: The datatype for point and cluster values.

    :returns: A numpy array containing all clusters.
    '''

    Format.print_information('Calculating tensorflow result - This can take some time', mark=True)
    points = pd.read_csv(points_csv).to_numpy()
    cluster = pd.read_csv(cluster_csv).to_numpy()
    datatype = None
    if type == 'bfloat':
        datatype = tf.bfloat16
    elif type == 'float' or type == 'float4':
        datatype = tf.float32
    elif type == 'double' or type == 'float8':
        datatype = tf.float64
    tf_points = tf.Variable([[float(entry[1]), float(entry[2])] for entry in points], dtype=datatype)
    tf_cluster = tf.Variable([[float(entry[1]), float(entry[2])] for entry in cluster], dtype=datatype)
    for _ in range(iterations):
       # Calculate distances from points to centroids
       distances = tf.reduce_sum(tf.square(tf.expand_dims(tf_points, 1) - tf_cluster), axis=2)
       
       # Assign clusters based on closest centroid
       cluster_assignments = tf.argmin(distances, axis=1)
       # Update centroids
       for i in range(len(cluster)):
            assigned_points = tf.boolean_mask(tf_points, tf.equal(cluster_assignments, i))
            if not tf.equal(tf.size(assigned_points), 0):
                new_centroid = tf.reduce_mean(assigned_points, axis=0)
                tf_cluster[i].assign(new_centroid)
    return tf_cluster.numpy()

def evaluate_accuray(tensorflow_result: np.ndarray, database_result: np.ndarray, reference: np.ndarray, min: int, max: int) -> Tuple[float, float]:
    '''
    This function evaluates the precision of the database output with the output from tensorflow.

    :param tensorflow_result: The clusters from tensorflow.
    :param database_result: The clusters from the database.
    :param reference: The reference clusters.
    :param min: The minimum x, y value of a cluster center.
    :param max: The maximum x, y value of a cluster center.

    :returns: The accuracy of the database and tensorflow result.
    '''

    Format.print_information('Calculating accuracy - This can take some time', mark=True)
    accuracies_db = []
    accuracies_tf = []
    # Find the nearest pairs and print the solution of comparison.
    for idx, center in enumerate(reference):
        distances_db = np.linalg.norm(database_result - center, axis=1)
        distances_tf = np.linalg.norm(tensorflow_result - center, axis=1)
        if len(distances_db) == 0:
            break
        closest_index_db = np.argmin(distances_db)
        closest_index_tf = np.argmin(distances_tf)
        closest_db = database_result[closest_index_db]
        closest_tf = tensorflow_result[closest_index_tf]

        Format.print_information(f'Cluster {idx + 1}', True, 1)
        Format.print_success(f'Database: {closest_db}', tabs=2)
        Format.print_success(f'Tensorflow: {closest_tf}', tabs=2)
        Format.print_success(f'Reference: {center}', tabs=2)

        min = min * -1 if min < 0 else min
        accuracy_db = (1 - (distances_db[closest_index_db] / (max + min))) * 100
        accuracy_tf = (1 - (distances_tf[closest_index_tf] / (max + min))) * 100
        accuracies_db.append(accuracy_db)
        accuracies_tf.append(accuracy_tf)

        database_result = np.delete(database_result, closest_index_db, axis=0)
        tensorflow_result = np.delete(tensorflow_result, closest_index_tf, axis=0)
    
    return sum(accuracies_db) / len(accuracies_db), sum(accuracies_tf) / len(accuracies_tf)

if __name__ == "__main__":
    main()
