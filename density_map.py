#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from multiprocessing import Process
import numpy as np

from prepare_dataframe import extract_df_atms, extract_df_restaurants
from prepare_dataframe import extract_df_stations, extract_df_supermarkets
from prepare_dataframe import extract_df_gas_stations
from utils import create_divisions, look_spots

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


def initial(datasets):
    """ This initial function is intended to load the input datasets and
    launch the process needed for the analysis.

    @param: datasets. A list with the names of datasets to be analysed.
    """
    df_dict = {'atms': extract_df_atms(),
               'gas_stations': extract_df_gas_stations(),
               'restaurants': extract_df_restaurants(cuisine='all',
                                                     wheelchair=False),
               'stations': extract_df_stations(wheelchair=False),
               'supermarkets': extract_df_supermarkets()}

    # Using create_divisions function we will get two numpy arrays
    # spaced by gap value (in meters).
    lat_divisions, lon_divisions = create_divisions(gap=200)

    # In order to reduce the time needed for this process five different
    # threads will be launched.
    density_j = []
    for proc in range(0, len(datasets), 1):
        density_p = Process(target=get_density, args=(datasets[proc],
                                                      df_dict[datasets[proc]],
                                                      lat_divisions,
                                                      lon_divisions))
        density_j.append(density_p)
        density_p.start()

        active_density = list([job.is_alive() for job in density_j])
    # Checks if the processes are complete.
    while True in active_density:
        active_density = list([job.is_alive() for job in density_j])
        pass


def get_density(proc, df, lat_divisions, lon_divisions):
    """ The values of lat_divisions and lon_divisions represent a grid.
    This function goes through all the grid looking for ATMs, gas
    stations, restaurants, stations or supermarkets. The total number of
    spots contained in each cell will be add to array_density object.

    @param: proc. A string with the name of the dataframe to be processed.
    @param: df. A dataframe object with value data.
    @param: lat_divisions. An array with all the latitude divisions.
    @param: lon_divisions. An array with all the longitude divisions.
    """
    array_density = np.zeros(shape=(lat_divisions.size, lon_divisions.size))

    for idx_lat, lat_division in enumerate(lat_divisions[:-1]):
        for idx_lon, lon_division in enumerate(lon_divisions[:-1]):
            df_sources = look_spots(df, lat_divisions[idx_lat],
                                    lat_divisions[idx_lat + 1],
                                    lon_divisions[idx_lon],
                                    lon_divisions[idx_lon + 1])

            if not df_sources.empty:
                array_density[idx_lat, idx_lon] = df_sources['lat'].size

    # Saves the dataframe in a .csv file.
    np.savetxt('{}.csv'.format(proc), array_density, delimiter=",")


def draw_density(datasets):
    """ On we have the spots contained in each cell these values will be
    plot in a pdf file called density_plots.pdf.

    @param: datasets. A list with the names of datasets to be analysed.
    """
    lat_divisions, lon_divisions = create_divisions(gap=200)

    with PdfPages('density_plots.pdf') as pdf:
        for dataset in datasets:
            plt.figure(figsize=(16.53, 11.69))  # for landscape

            density_data = np.genfromtxt('{}.csv'.format(dataset),
                                         delimiter=',')

            plt.imshow(density_data)  # Plots the array values as an image
            plt.title(dataset)

            # To have a clear vision of where the locations are x/y labels
            # will be labeled with degrees values
            lon_list = lon_divisions[np.arange(0, lon_divisions.size,
                                               int(lon_divisions.size / 10))]
            lon_list = list(np.around(lon_list, 2))
            lat_list = lat_divisions[np.arange(0, lat_divisions.size,
                                               int(lat_divisions.size / 10))]
            lat_list = list(np.around(lat_list, 2))

            # Create longitude ticks
            plt.xticks(np.arange(0, lon_divisions.size,
                                 int(lon_divisions.size / 10)),
                       lon_list)
            # Create latitude ticks
            plt.yticks(np.arange(0, lat_divisions.size,
                                 int(lat_divisions.size / 10)),
                       lat_list)
            plt.grid(True)
            pdf.savefig()
            plt.close()


if __name__ == '__main__':
    datasets = ['atms', 'gas_stations', 'restaurants',
                'stations', 'supermarkets']
    initial(datasets)
    draw_density(datasets)
