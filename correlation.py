#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import json
from collections import defaultdict

import geocoder
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from scipy.spatial.distance import cdist

from prepare_dataframe import extract_df_restaurants

# Restaurants with more than fifteen entries at database
cuisines = ['arab', 'asia', 'austria', 'burger', 'china', 'coffee',
            'croatia', 'france', 'germany', 'greece', 'india',
            'international', 'italy', 'japan', 'korea', 'mediterranean',
            'mexico', 'spain', 'steak', 'thailand', 'turkey', 'veggie',
            'vietnam']

# cuisines = ['asia']

with open('synonyms.json', 'r') as fp:
    synonyms_dict = json.load(fp)

clusters_number = 4  # By now!

for cuisine in cuisines:
    restaurants_df = extract_df_restaurants(cuisine, wheelchair=False)
    if len(restaurants_df.index) >= 15:
        X = np.array(restaurants_df[["lon", "lat"]])

        kmeans = KMeans(n_clusters=clusters_number).fit(X)
        centroids = kmeans.cluster_centers_

        # Predicting the clusters
        labels = kmeans.predict(X)
        # Getting the cluster centers
        C = kmeans.cluster_centers_

        # Get the address of centroids
        for i in range(0, C[:, 0].size, 1):
            g = geocoder.osm([C[:, 1][i], C[:, 0][i]], method='reverse')
            print(g.address)

        closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)

        clusters_indices = defaultdict(list)
        for index, c in enumerate(kmeans.labels_):
            clusters_indices[c].append(index)

        plt.scatter(X[:, 0], X[:, 1], color='red', s=20)
        plt.scatter(C[:, 0], C[:, 1], marker='*', color='blue', s=40)

        plt.grid(True)
        plt.title('cuisine {}'.format(cuisine))
        plt.show()

        # k means determine k
        res = list()
        n_cluster = range(2, 20)
        for n in n_cluster:
            kmeans = KMeans(n_clusters=n)
            kmeans.fit(X)
            res.append(np.average(np.min(cdist(X, kmeans.cluster_centers_, 'euclidean'), axis=1)))

        plt.plot(n_cluster, res)
        plt.title('elbow curve')
        plt.show()
