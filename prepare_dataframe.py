#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import json

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


def create_synonyms_dictionary():
    """ Creates a file in json format with all the synonyms associated to
    the different types of restaurants.
    This function only should be run one time since this data can be
    accesed from synonyms.json file.
    """
    synonyms_dict = {'afghanistan': ['afghan'],
                     'argentine': ['argentinisches', 'argentinian'],
                     'armenia': ['armenian', 'armenean'],
                     'australia': ['australian'],
                     'austria': ['austrian'],
                     'bosnia': ['bosnian'],
                     'brazil': ['brazilian'],
                     'china': ['chinese', 'cantonese', 'China'],
                     'cyprus': ['cyprian'],
                     'croatia': ['croatian'],
                     'cuba': ['cuban'],
                     'egypt': ['egyptian', 'egypt'],
                     'france': ['french'],
                     'georgia': ['georgie', 'georgian'],
                     'germany': ['deutsch', 'german', 'rhenish', 'sausage',
                                 'swabian', 'bavarian', 'thuringian', 'Weine',
                                 'altbayerisch', 'regional'],
                     'greece': ['greek'],
                     'hungary': ['hungarian'],
                     'india': ['indian', 'Indische', 'Indisch'],
                     'indonesia': ['indonesian', 'indonesia'],
                     'iran': ['persisch', 'iranian', 'persian'],
                     'israel': ['israeli'],
                     'italy': ['italian', 'Pizza', 'pizza', 'pasta'],
                     'jamaica': ['Jamaican'],
                     'japan': ['sushi', 'japanese', 'ramen', 'suhi'],
                     'korea': ['korean', 'koreanisch'],
                     'latvia': ['latvian'],
                     'macedonian': ['macedonian'],
                     'malaysia': ['malaysian'],
                     'mexico': ['mexican'],
                     'morocco': ['moroccan'],
                     'norway': ['norgewian'],
                     'philippines': ['filipino', 'philippinisch',
                                     'phillipinian'],
                     'poland': ['polish'],
                     'russia': ['russian'],
                     'singapore': ['singaporean', 'Singapuri', 'singapore'],
                     'slovak_slow_food': ['slovak_slow_food'],
                     'syria': ['syrian'],
                     'spain': ['spanish', 'tapas'],
                     'sudan': ['sudanese'],
                     'switzerland': ['swiss'],
                     'taiwan': ['taiwanese'],
                     'thailand': ['thai'],
                     'turkey': ['turkish', 'kebab'],
                     'ukraine': ['ukrainian'],
                     'uzbekistan': ['uzbek'],
                     'vietnam': ['vietnamese', 'Vietnamesische', 'vietnam',
                                 'viet-food', 'viet'],
                     'arab': ['Arab', 'arab', 'arabic', 'arabisch'],
                     'nepal': ['nepalese', 'nepal', 'nepali'],
                     'yugoslavia': ['yugoslavian'],
                     'lebanon': ['libanese', 'lebanese'],
                     'caribbean': ['caribbean'],
                     'trinidad': ['trinidad'],
                     'jewish': ['jewish'],
                     'pakistan': ['pakistani'],
                     'peru': ['peruvian'],
                     'tibet': ['tibetan'],
                     'laos': ['laotian', 'laos'],
                     'indochina': ['indochinese'],
                     'portugal': ['portuguese'],
                     'catalonia': ['catalan'],
                     'bulgaria': ['bulgarien', 'bulgarian'],
                     'africa': ['Afrikanisches', 'african'],
                     'anatolia': ['anatolian'],
                     'asia': ['asian'],
                     'balkan': ['balkan'],
                     'mediterranean': ['mediterranean'],
                     'scandinavia': ['scandinavian'],
                     'hawaii': ['Hawaiian', 'hawaiian'],
                     'veggie': ['vegetarian', 'vegan'],
                     'soup': ['soup', 'soups'],
                     'steak': ['steak', 'steak_house'],
                     'seafood': ['seafood'],
                     'breakfast': ['breakfast'],
                     'coffee': ['coffee_shop', 'cafe'],
                     'bbq': ['bbq', 'barbacue'],
                     'potato': ['potato'],
                     'latin': ['latin-american', 'latin_american',
                               'lateinamerikanische'],
                     'salad': ['salad', 'salads'],
                     'bagel': ['bagel'],
                     'burger': ['burger'],
                     'canteen': ['canteen'],
                     'chicken': ['chicken'],
                     'fastfood': ['fastfood'],
                     'gourmet': ['gourmet'],
                     'hummus': ['hummus'],
                     'ice_cream': ['ice_cream'],
                     'international': ['international'],
                     'lunch': ['lunch'],
                     'pubfood': ['pubfood'],
                     'other': ['other'],
                     'oriental': ['oriental'],
                     'sandwich': ['sandwich'],
                     'southern_states': ['southern_states'],
                     'alpine_hut': ['alpine_hut'],
                     'modern_european_cusine': ['modern_european_cusine'],
                     'crepe': ['crepe'],
                     'fine_dining': ['fine_dining'],
                     'New_London_Cuisine': ['New_London_Cuisine'],
                     'frites': ['frites'],
                     'soul_food': ['soul_food'],
                     'fondue': ['fondue'],
                     'Dumplings': ['Dumplings'],
                     'wine_tavern': ['wine_tavern'],
                     'ayurvedisch': ['ayurvedisch'],
                     'bierverkostung': ['bierverkostung'],
                     'casual_fine_dining': ['casual_fine_dining'],
                     'verschieden': ['verschieden'],
                     'fish': ['fish']}

    with open('synonyms.json', 'w') as fp:
        json.dump(synonyms_dict, fp, sort_keys=True, indent=4)


def categorise_cuisine(cuisine):
    """ Loads the synonyms of restaurants denominations and returns a list
    with all the synonyms associated to a type of cuisine.

    @param: cuisine. A string of the cuisine denomination.

    @return: tags. A list populated by all the synonyms.
    """
    tags = []

    with open('synonyms.json', 'r') as fp:
        synonyms_dict = json.load(fp)

    for key_ in synonyms_dict.keys():
        for synonym in synonyms_dict[key_]:
            if synonym in cuisine:
                tags.append(key_)

    tags = list(set(tags))

    return tags


def create_dict(keys_list):
    """ Creates a dictionary from a given list of keys """
    dict_ = {}
    for key_ in keys_list:
        dict_[key_] = []

    return dict_


def extract_df_restaurants(cuisine, wheelchair):
    """ Extracts all valuable data from original .json file of restaurants
    information. If cuisine or wheelchair parameters are given this function
    can filter the input data by wheelchair accessibility or any particular
    cuisine.

    @param: cuisine.
    @param: wheelchair. A boolean variable to determine if the dataframe 
    returned will be filtered by wheelchair accessibility.

    @return: restaurants_df. A dataframe which contains all valuable
    information about restaurants.
    """
    restaurants_df = pd.read_json('datasets/berlin_restaurants.json',
                                  orient='records')
    tags = restaurants_df['tags']

    tags_dict = create_dict(['amenity', 'cuisine', 'toilets:wheelchair',
                             'wheelchair', 'opening_hours'])

    for row in tags:
        for tag in tags_dict:
            if tag in row.keys():
                if tag is 'cuisine':
                    tags_dict[tag].append(categorise_cuisine(row[tag]))
                else:
                    tags_dict[tag].append(row[tag])
            else:
                tags_dict[tag].append([])

    # Categorise cuisine
    # If cuisine parameter is 'all' no filter process is performed.
    bool_cuisine_list = []
    for tags_cuisine in tags_dict['cuisine']:
        if cuisine is not 'all':
            if cuisine in tags_cuisine:  # Checks if is our cuisine
                bool_cuisine_list.append(True)
            else:  # If not rejects the restaurant
                bool_cuisine_list.append(False)
        else:
            bool_cuisine_list.append(True)

    # Categorise wheelchair
    bool_wheelchair_list = []
    for tag_wheelchair in tags_dict['wheelchair']:
        if tag_wheelchair == 'yes':
            bool_wheelchair_list.append(True)
        else:
            bool_wheelchair_list.append(False)

    # Create Series
    amenity_series = pd.Series(tags_dict['amenity'], name='amenity')
    cuisine_series = pd.Series(tags_dict['cuisine'], name='cuisine')
    bool_cuisine_series = pd.Series(bool_cuisine_list, name='cuisine_bool')
    toilets_wheelchair_series = pd.Series(tags_dict['toilets:wheelchair'],
                                          name='toilets:wheelchair')
    wheelchair_series = pd.Series(tags_dict['wheelchair'], name='wheelchair')
    bool_wheelchair_list = pd.Series(bool_wheelchair_list,
                                     name='wheelchair_bool')
    opening_hours_series = pd.Series(tags_dict['opening_hours'],
                                     name='opening_hours')

    restaurants_df = pd.concat([restaurants_df['id'], restaurants_df['lat'],
                                restaurants_df['lon'], amenity_series,
                                cuisine_series, bool_cuisine_series,
                                toilets_wheelchair_series,
                                wheelchair_series, bool_wheelchair_list,
                                opening_hours_series],
                               axis=1)

    # Filter by cuisine
    restaurants_df = restaurants_df[restaurants_df['cuisine_bool']]

    # Filter by wheelchair
    if wheelchair:
        restaurants_df = restaurants_df[restaurants_df['wheelchair_bool']]

    return restaurants_df


def extract_df_atms(wheelchair):
    """ Extracts all valuable data from original .json file of ATMS location.

    @param: wheelchair. A boolean variable to determine if the dataframe
    returned will be filtered by wheelchair accessibility.

    @return: atms_df. A dataframe which contains all valuable
    information about ATMs.
    """
    atms_df = pd.read_json('datasets/berlin_atms.json', orient='records')
    tags = atms_df['tags']

    tags_dict = create_dict(['wheelchair'])

    bool_wheelchair_list = []
    for row in tags:
        if 'wheelchair' in row.keys():
            tags_dict['wheelchair'].append(row['wheelchair'])
            if row['wheelchair'] == 'yes':
                bool_wheelchair_list.append(True)
            elif row['wheelchair'] == 'limited':
                bool_wheelchair_list.append(True)
            elif row['wheelchair'] == 'no':
                bool_wheelchair_list.append(False)
        else:
            tags_dict['wheelchair'].append(None)
            bool_wheelchair_list.append(False)

    # Create Series
    wheelchair_series = pd.Series(tags_dict['wheelchair'], name='wheelchair')
    bool_wheelchair_list = pd.Series(bool_wheelchair_list,
                                     name='wheelchair_bool')
    atms_df = pd.concat([atms_df['id'], atms_df['lat'], atms_df['lon'],
                         wheelchair_series, bool_wheelchair_list], axis=1)

    # Filter by wheelchair
    if wheelchair:
        atms_df = atms_df[atms_df['wheelchair_bool']]

    return atms_df


def extract_df_stations(wheelchair):
    """ Extracts all valuable data from original .json file of stations.
    Information about bus, tram, U-Bahn and S-Bahn stations is given.

    @param: wheelchair. A boolean variable to determine if the dataframe
    returned will be filtered by wheelchair accessibility.

    @return: stations_df. A dataframe with all chosen information.
    """
    stations_df = pd.read_json('datasets/berlin_stations.json',
                               orient='records')
    tags = stations_df['tags']

    tags_dict = create_dict(['wheelchair'])

    bool_wheelchair_list = []
    for row in tags:
        if 'wheelchair' in row.keys():
            tags_dict['wheelchair'].append(row['wheelchair'])
            if row['wheelchair'] == 'yes':
                bool_wheelchair_list.append(True)
            elif row['wheelchair'] == 'limited':
                bool_wheelchair_list.append(True)
            elif row['wheelchair'] == 'no':
                bool_wheelchair_list.append(False)
        else:
            tags_dict['wheelchair'].append(None)
            bool_wheelchair_list.append(False)

    # Create Series
    wheelchair_series = pd.Series(tags_dict['wheelchair'], name='wheelchair')
    bool_wheelchair_list = pd.Series(bool_wheelchair_list,
                                     name='wheelchair_bool')

    stations_df = pd.concat([stations_df['id'], stations_df['lat'],
                             stations_df['lon'], wheelchair_series,
                             bool_wheelchair_list], axis=1)

    # Filter by wheelchair
    if wheelchair:
        stations_df = stations_df[stations_df['wheelchair_bool']]

    return stations_df


def extract_df_gas_stations():
    """ Extracts all valuable data from original .json file of gas stations.

    Wheelchair access is not so relevant for this kind of spots.

    @return: gas_stations_df. A dataframe with all valuable information.
    """
    gas_stations_df = pd.read_json('datasets/berlin_gas_stations.json',
                                   orient='records')

    return gas_stations_df


def extract_df_supermarkets(wheelchair):
    """ Extracts all valuable data from original .json file of supermarkets
    information. If wheelchair parameter is given this function can filter
    the input data by wheelchair accessibility.

    @param: wheelchair. A boolean variable to determine if the dataframe
    returned will be filtered by wheelchair accessibility.

    @return: supermarkets_df.
    """
    supermarkets_df = pd.read_json('datasets/berlin_supermarkets.json',
                                   orient='records')
    tags = supermarkets_df['tags']

    tags_dict = create_dict(['wheelchair'])

    bool_wheelchair_list = []

    for row in tags:
        if 'wheelchair' in row.keys():
            tags_dict['wheelchair'].append(row['wheelchair'])
            if row['wheelchair'] == 'yes':
                bool_wheelchair_list.append(True)
            elif row['wheelchair'] == 'limited':
                bool_wheelchair_list.append(True)
            elif row['wheelchair'] == 'no':
                bool_wheelchair_list.append(False)
        else:
            tags_dict['wheelchair'].append(None)
            bool_wheelchair_list.append(False)

    # Create Series
    wheelchair_series = pd.Series(tags_dict['wheelchair'], name='wheelchair')
    bool_wheelchair_list = pd.Series(bool_wheelchair_list,
                                     name='wheelchair_bool')

    supermarkets_df = pd.concat([supermarkets_df['id'],
                                 supermarkets_df['lat'],
                                 supermarkets_df['lon'],
                                 wheelchair_series,
                                 bool_wheelchair_list], axis=1)

    # Filter by wheelchair
    if wheelchair:
        supermarkets_df = supermarkets_df[supermarkets_df['wheelchair_bool']]

    return supermarkets_df
