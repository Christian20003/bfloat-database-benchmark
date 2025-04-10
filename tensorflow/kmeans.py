from random import random
from sklearn.cluster import KMeans
import numpy as np
import tensorflow as tf

def calculate_distance(point, cluster):
    pow = tf.constant([2, 2], tf.float64)
    squared_error = tf.pow(tf.cast(tf.subtract(cluster, point), tf.float64), pow)
    distance = tf.reduce_sum(tf.cast(squared_error, tf.bfloat16))
    return distance.numpy()

def init_assignments(amount):
    assignment = {}
    for value in range(amount):
        assignment.update({value: []})
    return assignment

def calc_centers(assignment: dict, clusters):
    for key, value in assignment.items():
        sum = tf.constant([0, 0], tf.bfloat16)
        length = tf.constant([len(value), len(value)], tf.bfloat16)
        for point in value:
            sum = tf.add(sum, point)
        clusters[key] = tf.divide(sum, length)
    return clusters

points_np = []
clusters_np = []
points = []
clusters = []
assignment = {}

for point in range(1000):
    x = random()
    y = random()
    points_np.append([x,y])
    points.append(tf.constant([x, y], tf.bfloat16))
for cluster in range(4):
    x = random()
    y = random()
    clusters_np.append([x,y])
    clusters.append(tf.constant([x, y], tf.bfloat16))

for iter in range(10):
    assignment = init_assignments(4)
    for point in points:
        assign = [0, clusters[0]]
        for idx, cluster in enumerate(clusters):
            if idx != 0:
                distance1 = calculate_distance(point, cluster)
                distance2 = calculate_distance(point, assign[1])
                if distance1 < distance2:
                    assign = [idx, cluster]
        list = assignment.get(assign[0])
        list.append(point)
        assignment.update({assign[0]: list})
    clusters = calc_centers(assignment, clusters)

points_np = np.asarray(points_np)
clusters_np = np.asanyarray(clusters_np)
kmeans = KMeans(n_clusters=4, init=clusters_np, n_init=1, max_iter=10)
kmeans.fit(points_np)
print(kmeans.cluster_centers_)
print([cluster.numpy() for cluster in clusters])