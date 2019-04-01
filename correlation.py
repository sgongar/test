#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import json
from collections import Counter, defaultdict

from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from scipy.spatial.distance import cdist

from prepare_dataframe import extract_df_restaurants, extract_df_stations

# Restaurants with more than fifteen entries at database
cuisines = ['arab', 'asia', 'austria', 'burger', 'china', 'coffee',
            'croatia', 'france', 'germany', 'greece', 'india',
            'international', 'italy', 'japan', 'korea', 'mediterranean',
            'mexico', 'spain', 'steak', 'thailand', 'turkey', 'veggie',
            'vietnam']

# cuisines = ['italy']

with open('synonyms.json', 'r') as fp:
    synonyms_dict = json.load(fp)

clusters_number = 7  # By now!

for cuisine in cuisines:
    restaurants_df = extract_df_restaurants(cuisine, wheelchair=True)
    stations_df = extract_df_stations(wheelchair=True)
    if len(restaurants_df.index) >= 15:
        X = np.array(restaurants_df[["lon", "lat"]])

        kmeans = KMeans(n_clusters=clusters_number).fit(X)
        centroids = kmeans.cluster_centers_

        # Predicting the clusters
        labels = kmeans.predict(X)
        # Getting the cluster centers
        C = kmeans.cluster_centers_

        # Vemos el representante del grupo, el usuario cercano a su centroid
        closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)

        clusters_indices = defaultdict(list)
        for index, c in enumerate(kmeans.labels_):
            clusters_indices[c].append(index)

        # print(clusters_indices[0])

        # for cluster in clusters_indices:  

        plt.scatter(X[:, 0], X[:, 1], color='red', s=20)
        plt.scatter(C[:, 0], C[:, 1], marker='*', color='blue', s=40)

        # plt.scatter(stations_df['lon'], stations_df['lat'], color='green',
        #             s=20)

        # Plots relations between centroids and restaurants
        # for idx, centroid in enumerate(centroids):
        #     x, y = centroid[0], centroid[1]
        #     for restaurant in clusters_indices[idx]:
        #         print(restaurant)

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
