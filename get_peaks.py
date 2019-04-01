#!/usr/bin/env python
# -*- coding: utf-8 -*-
import geocoder
import numpy as np
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
import matplotlib.pyplot as plt

from utils import create_divisions

"""
   Copyright 2019 Samuel Góngora García
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
:Author:
    Samuel Góngora García (s.gongoragarcia@gmail.com)
"""
__author__ = 's.gongoragarcia@gmail.com'


def main():
    """
    2*supermarkets + 2*stations + atms + restaurants + gas_stations
    """
    neighborhood_size = 10
    threshold = 20

    lat_divisions, lon_divisions = create_divisions(gap=200)

    datasets_factors = [2, 1, 2, 2, 2]
    datasets = ['atms', 'gas_stations', 'restaurants',
                'stations', 'supermarkets']
    datasets_dict = {}

    for idx_dataset, dataset in enumerate(datasets):
        datasets_dict[dataset] = np.genfromtxt('{}.csv'.format(dataset),
                                               delimiter=',')
        with np.nditer(datasets_dict[dataset], op_flags=['readwrite']) as it:
            for x in it:
                x[...] = datasets_factors[idx_dataset] * x

    datasets_list = []
    for key_ in datasets_dict.keys():
        datasets_list.append(datasets_dict[key_])

    data = sum(datasets_list)

    data_max = filters.maximum_filter(data, neighborhood_size)
    maxima = (data == data_max)
    data_min = filters.minimum_filter(data, neighborhood_size)
    diff = ((data_max - data_min) > threshold)
    maxima[diff == 0] = 0

    labeled, num_objects = ndimage.label(maxima)
    slices = ndimage.find_objects(labeled)
    x, y = [], []
    for dy, dx in slices:
        x_center = (dx.start + dx.stop - 1) / 2
        x.append(x_center)
        y_center = (dy.start + dy.stop - 1) / 2
        y.append(y_center)

    plt.imshow(data)
    plt.autoscale(False)
    plt.plot(x, y, 'ro')

    for i in range(0, len(x), 1):
        g = geocoder.osm([lat_divisions[int(y[i])],
                          lon_divisions[int(x[i])]], method='reverse')
        print(g.address)

    lon_list = lon_divisions[np.arange(0, lon_divisions.size,
                                       int(lon_divisions.size / 10))]
    lon_list = list(np.around(lon_list, 2))
    lat_list = lat_divisions[np.arange(0, lat_divisions.size,
                                       int(lat_divisions.size / 10))]
    lat_list = list(np.around(lat_list, 2))

    # Create longitude ticks
    plt.xticks(np.arange(0, lon_divisions.size, int(lon_divisions.size / 10)),
               lon_list)
    plt.yticks(np.arange(0, lat_divisions.size, int(lat_divisions.size / 10)),
               lat_list)
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
