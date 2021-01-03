import numpy as np
import matplotlib.pyplot as plt

def distance(a, b):
    return np.linalg.norm(a-b)

def loadData(filename):
    return np.loadtxt(filename)

def kMeans(k, eps = 0):
    dataset = loadData('S1.txt')
    dist = distance
    i, j = dataset.shape
    print(i, ' ', j)
    centroids = dataset[np.random.randint(0, i-1, size=k)]
    nearest = np.zeros((i, 1))
    prev_centroids = np.zeros((centroids.shape))
    norm = dist(centroids, prev_centroids)
    steps=0
    while norm > eps:
        norm = dist(centroids, prev_centroids)
        prev_centroids = centroids
        steps=steps+1
        for ind, val in enumerate(dataset):
            distances = np.zeros((k, 1))
            for indC, centr in enumerate(centroids):
                distances[indC] = dist(val, centr)
            nearest[ind] = np.argmin(distances)

        tmp_centroids = np.zeros((k, j))

        for index in range(len(centroids)):
            kValues = [u for u in range(len(nearest)) if nearest[u] == index]
            centroid = np.mean(dataset[kValues], axis=0)
            tmp_centroids[index, :] = centroid
        centroids = tmp_centroids

        print(steps)
    return centroids, nearest

def draw(dataset, nearest, centroids):
    fig, ax = plt.subplots()
    for index in range(dataset.shape[0]):
        kValues = [i for i in range(len(nearest)) if nearest[i] == index]
        c = np.random.rand(3,)
        for indVal in kValues:
            ax.plot(dataset[indVal , 0], dataset[indVal , 1], marker='o', color=c)
    for ind in range(centroids.shape[0]):
            ax.plot(centroids[ind, 0], centroids[ind, 1], marker='o', color='k')
    plt.show()

dataset = loadData('S1.txt')
centroids, nearest = kMeans(15)
draw(dataset, nearest, centroids)
