import functools
import math
import re
import matplotlib.pyplot as plt
from random import randint


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'x:' + str(self.x) + ' y:' + str(self.y)

    def get_distance(self, point):
        return math.sqrt(((self.x - point.x) ** 2) + ((self.y - point.y) ** 2))


class Cluster:
    def __init__(self, x, y):
        self.center = Point(x, y)
        self.points = []

    def __repr__(self):
        return 'center:' + self.center.__repr__()


def main():
    data_paths = ['birch1.txt', 'birch2.txt', 'birch3.txt', 's1.txt']
    print('chose dataset:')
    for i in range(len(data_paths)):
        print(str(i)+'-'+data_paths[i])
    path_index = int(input())
    file = open('datasets/'+data_paths[path_index], 'r')
    lines = file.readlines()
    file.close()
    print('enter clusters number')
    clusters_number = int(input())
    points = []
    clusters = []
    for x in range(clusters_number):
        cluster = Cluster(randint(0, 10000), randint(0, 10000))
        clusters.append(cluster)
    for line in lines:
        nums = re.split('\\s+', line)
        point = Point(int(nums[1]), int(nums[2]))
        points.append(point)
    lengths = []
    while True:
        add_to_clusters(clusters, points)
        is_end = True
        if len(lengths) == 0:
            is_end = False
        for i in range(len(lengths)):
            if not (lengths[i] == len(clusters[i].points)):
                is_end = False
                break
        if is_end:
            break
        evaluate_new_centers(clusters)
        lengths.clear()
        for cluster in clusters:
            lengths.append(len(cluster.points))
            cluster.points.clear()
    colors = ['black', 'red', 'blue', 'green', 'cyan', 'magenta', 'yellow']
    for i in range(len(clusters)):
        for point in clusters[i].points:
            plt.plot(point.x, point.y, 'o', color=colors[i])
    plt.show()


def evaluate_new_centers(clusters):
    for cluster in clusters:
        if len(cluster.points) > 0:
            cluster.center.y = functools.reduce(lambda a, b: a + b, list(map(lambda q: q.y, cluster.points))) / len(
                cluster.points)
            cluster.center.x = functools.reduce(lambda a, b: a + b, list(map(lambda q: q.x, cluster.points))) / len(
                cluster.points)


def add_to_clusters(clusters, points):
    for point in points:
        best_cluster = None
        for cluster in clusters:
            if best_cluster is None or cluster.center.get_distance(point) < best_cluster.center.get_distance(point):
                best_cluster = cluster
        best_cluster.points.append(point)


main()
