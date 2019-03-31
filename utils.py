#!/usr/bin/env python
# -*- coding: utf-8 -*-
import geopy.distance
import numpy as np
import pandas as pd

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


def get_borders():
    """ Given a series of datasets return the maximum and minimum
    latitude and longitude.

    @return: border_d. A dictionary populated by maximum and minimum latitude
    and longitude
    """
    dfs = []

    dictionaries = ['berlin_atms', 'berlin_gas_stations',
                    'berlin_restaurants', 'berlin_stations',
                    'berlin_supermarkets']

    for dictionary in dictionaries:
        df = pd.read_json('datasets/{}.json'.format(dictionary),
                          orient='records')
        dfs.append(df)

    # Concat dataframes
    full_df = pd.concat(dfs)

    borders_d = {'max_lat': full_df['lat'].max(),
                 'min_lat': full_df['lat'].min(),
                 'max_lon': full_df['lon'].max(),
                 'min_lon': full_df['lon'].min()}

    return borders_d


def create_divisions(gap):
    """ Creates a list of latitude or longitude values (expressed in
    degrees), separated by a specified distance in meters.

    @param: gap Step size in meters.

    @return: lat_list, lon_list.
    """
    borders_d = get_borders()  # Extracts borders.

    # Gets the separation between the lower and the higher value of
    # latitude in degrees
    coords_1 = (borders_d['min_lat'],
                (borders_d['max_lon'] + borders_d['min_lon']) / 2)
    coords_2 = (borders_d['max_lat'],
                (borders_d['max_lon'] + borders_d['min_lon']) / 2)
    lat_width = geopy.distance.distance(coords_1, coords_2).m
    lat_difference = borders_d['max_lat'] - borders_d['min_lat']
    lat_gap = (gap * (lat_difference)) / lat_width

    # Gets the separation between the lower and the higher value of
    # longitude in degrees
    coords_1 = (borders_d['min_lon'],
                (borders_d['max_lat'] + borders_d['min_lat']) / 2)
    coords_2 = (borders_d['max_lon'],
                (borders_d['max_lat'] + borders_d['min_lat']) / 2)
    lon_width = geopy.distance.distance(coords_1, coords_2).m
    lon_difference = borders_d['max_lon'] - borders_d['min_lon']
    lon_gap = (gap * (lon_difference)) / lon_width

    lat_list = np.arange(borders_d['min_lat'] - lat_gap,
                         borders_d['max_lat'], lat_gap)
    lon_list = np.arange(borders_d['min_lon'] - lon_gap,
                         borders_d['max_lon'], lon_gap)

    return(lat_list, lon_list)


def look_spots(i_df, first_lat, last_lat, first_lon, last_lon):
    """

    @param: id_f.
    @param: first_lat.
    @param: first_lon.
    @param: last_lon.

    @retun: i_df_spots. A Pandas Dataframe p
    """
    i_df_spots = i_df[i_df['lat'] > first_lat]
    i_df_spots = i_df_spots[last_lat > i_df_spots['lat']]
    i_df_spots = i_df_spots[i_df_spots['lon'] > first_lon]
    i_df_spots = i_df_spots[last_lon > i_df_spots['lon']]

    return(i_df_spots)
