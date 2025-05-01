import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Helper')))

from Config import CONFIG, STATEMENT
import random
import Format
import Database
import Create_CSV
import Memory
import Time
import Helper
import numpy as np
import pandas as pd
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

def main() -> None:
    databases = CONFIG['databases']
    scenarios = CONFIG['setups']

    generate_statement(CONFIG['iterations'])

    for database in databases:
        if database['create_csv']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])

    for scenario in scenarios:
        if scenario['ignore']:
            continue
        generate_points(scenario['p_amount'], scenario['min'], scenario['max'], './points.csv')
        generate_points(scenario['c_amount'], scenario['min'], scenario['max'], './clusters.csv')
        for database in databases:
            for type in database['types']:
                Format.print_title(f'START BENCHMARK - KMEANS WITH {scenario["p_amount"]} POINTS AND {scenario["c_amount"]} CLUSTERS')
                prep_database = Database.Database(database['execution'], database['start-sql'], database['end-sql'])
                prep_database.create_table('points', ['id', 'x', 'y'], ['int', type, type])
                prep_database.create_table('clusters_0', ['id', 'x', 'y'], ['int', type, type])
                prep_database.insert_from_csv('points', './points.csv')
                prep_database.insert_from_csv('clusters_0', './clusters.csv')
                prep_database.execute_sql()

                execution_string = database['execution-bench'].format('Statement.sql')
                time, output = Time.benchmark(execution_string, database['name'], 4, [2,3])
                heap, rss = Memory.benchmark(execution_string, f'{database["name"]}_{type}_{scenario["p_amount"]}_{scenario["c_amount"]}')

                tf_output = kmeans_tensorflow('./points.csv', './clusters.csv', CONFIG['iterations'], type)
                accuracy = evaluate_accuray(tf_output, output, scenario['min'], scenario['max'])

                Create_CSV.append_row(database['csv_file'], [type, scenario["p_amount"], scenario["c_amount"], CONFIG['iterations'], time, heap, rss, accuracy, output, tf_output])
                Helper.remove_files(database['files'])
    Helper.remove_files(['./points.csv', './clusters.csv', './Statement.sql'])


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

def generate_statement(iterations: int) -> None:
    '''
    This function generates the SQL file.

    :param iterations: The number of iterations in the recursive CTE.
    '''

    with open('./Statement.sql', 'w') as file:
        file.write(STATEMENT.format(iterations, iterations))

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
    datatype = tf.bfloat16 if type == 'bfloat' else tf.float32
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
    """ kmeans = KMeans(n_clusters=4, init=[[float(entry[1]), float(entry[2])] for entry in cluster], max_iter=iterations)
    kmeans.fit([[float(entry[1]), float(entry[2])] for entry in points])
    print(kmeans.cluster_centers_) """
    return tf_cluster.numpy()

def evaluate_accuray(tensorflow_result: np.ndarray, database_result: np.ndarray, min: int, max: int) -> float:
    '''
    This function evaluates the precision of the database output with the output from tensorflow.

    :param tensorflow_result: The clusters from tensorflow.
    :param database_result: The clusters from the database.
    :param min: The minimum x, y value of a cluster center.
    :param max: The maximum x, y value of a cluster center.

    :returns: The overall accuarcy of the database output compared with the tensorflow output.
    '''

    Format.print_information('Calculating accuracy - This can take some time', mark=True)
    accuracies = []
    # Find the nearest pairs and print the solution of comparison.
    for idx, center in enumerate(tensorflow_result):
        distances = np.linalg.norm(database_result - center, axis=1)
        if len(distances) == 0:
            break
        closest_index = np.argmin(distances)
        closest = database_result[closest_index]

        Format.print_information(f'Cluster {idx + 1}', True, 1)
        Format.print_information(f'Database: {closest}', tabs=2)
        Format.print_information(f'Tensorflow: {center}', tabs=2)

        min = min * -1 if min < 0 else min
        accuracy = (1 - (distances[closest_index] / (max + min))) * 100
        accuracies.append(accuracy)
        Format.print_success(f'Accuracy: {accuracy:.2f}', tabs=2)

        database_result = np.delete(database_result, closest_index, axis=0)
    
    return sum(accuracies) / len(accuracies)

if __name__ == "__main__":
    main()
