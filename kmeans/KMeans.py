import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Benchmark')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Csv')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/SQL')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared/Print')))

from typing import List
from Config import CONFIG, STATEMENT
import random
import Format
import Database
import Create_CSV
import numpy as np
import tensorflow as tf

def main() -> None:
    databases = CONFIG['databases']
    scenarios = CONFIG['setups']

    generate_statement(CONFIG['iterations'])

    for database in databases:
        if database['create_csv']:
            Create_CSV.create_csv_file(database['csv_file'], database['csv_header'])
        for scenario in scenarios:
            points = generate_points(scenario['p_amount'], scenario['min'], scenario['max'])
            cluster = generate_points(scenario['c_amount'], scenario['min'], scenario['max'])
            for type in database['types']:
                prep_database = Database.Database(database['execution'], database['start_sql'], database['end_sql'])
                prep_database.create_table('points', ['x', 'y'], [type, type])
                prep_database.create_table('clusters_0', ['x', 'y'], [type, type])
                prep_database.insert_from_csv('points', './points.csv', ['x', 'y'], points)
                prep_database.insert_from_csv('cluster_0', './cluster.csv', ['x', 'y'], cluster)
                prep_database.execute_sql()

                time = 0
                memory = 0

                tf_output = kmeans_tensorflow(points, cluster, CONFIG['iterations'], type)
                accuracy = evaluate_accuray(tf_output, _, scenario['min'], scenario['max'])

                Create_CSV.append_row(database['csv_file'], [time, memory])



def generate_points(number: int, min: int, max: int) -> List[List[str]]:
    '''
    This function generates a specified number of random points and stores them as string.

    :param number: The number of points.
    :param min: The maximum value for x and y.
    :param max: The minimum value for x and y.

    :return: A list of point objects.
    '''

    result = []
    for _ in range(number):
        result.append([random.uniform(min, max), random.uniform(min, max)])
    return result

def generate_statement(iterations: int) -> None:
    '''
    This function generates the SQL file.

    :param iterations: The number of iterations in the recursive CTE.
    '''

    with open('./Statement.sql', 'w') as file:
        file.write(STATEMENT.format(iterations, iterations))

def kmeans_tensorflow(points: List[List[str]], cluster: List[List[str]], iterations: int, type: str) -> np.ndarray:
    '''
    This function implements the kmeans algorithm with tensorflow.

    :param points: The list of points which should be assigned to a cluster.
    :param cluster: The list of intial clusters.
    :param iterations: The number of iterations.
    :param type: The datatype for point and cluster values.

    :returns: A numpy array containing all clusters.
    '''

    points = [[float(entry[0]), float(entry[1])] for entry in points]
    cluster = [[float(entry[0]), float(entry[1])] for entry in cluster]
    datatype = tf.bfloat16 if type == 'tfloat' else tf.float32
    tf_points = tf.constant(points, datatype)
    tf_cluster = tf.constant(cluster, datatype)
    for _ in range(iterations):
       # Calculate distances from points to centroids
       distances = tf.reduce_sum(tf.square(tf.expand_dims(tf_points, 1) - tf_cluster), axis=2)
       
       # Assign clusters based on closest centroid
       cluster_assignments = tf.argmin(distances, axis=1)
       # Update centroids
       for i in range(len(cluster)):
           assigned_points = tf.boolean_mask(tf_points, tf.equal(cluster_assignments, i))
           new_centroid = tf.reduce_mean(assigned_points, axis=0)
           tf_cluster[i].assign(new_centroid)

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
        accuracy = (1 - (distances[closest_index] / (max + min)))
        accuracies.append(accuracy)
        Format.print_success(f'Accuracy: {accuracy:.2f}', tabs=2)

        database_result = np.delete(database_result, closest_index, axis=0)
    
    return sum(accuracies) / len(accuracies)

if __name__ == "__main__":
    main()
