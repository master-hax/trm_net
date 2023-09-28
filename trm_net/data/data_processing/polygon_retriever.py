# Retrieving polygons from maxar data for sentinel download capability

import pandas as pd
import geopandas as gpd
import leafmap.foliumap as leafmap

import datetime
from subprocess import call

from PIL import Image
from os.path import join, isfile, isdir
from os import listdir, remove, mkdir
import numpy as np
import urllib.request
from multiprocessing.dummy import Pool

repo = 'https://raw.githubusercontent.com/opengeos/maxar-open-data/master/'

dataset = 'Kahramanmaras-turkey-earthquake-23'

def get_image(collection_name, data_dir):
    try:
        collections = leafmap.maxar_child_collections(collection_name)
    except:
        print("The collection name is not valid.")
        return
    
    print("downloading sentinel data for" + collection_name + " collection")
    geojson = f'{repo}datasets/{dataset}.geojson'

    gdf = gpd.read_file(geojson)
    # sort by datetime
    gdf = gdf.sort_values(by='datetime')

    # get the first and last date
    start_date = gdf['datetime'].iloc[0]
    end_date = gdf['datetime'].iloc[-1]

    print(gdf['tile:data_area'].iloc[0])
    # loop through each row

    for index, row in gdf[:1].iterrows():
        # date
        date = row['datetime']
        year = date.year
        quad = int(date.month/4)+1
        # polygon
        polygon = row['geometry']
        # creating a list of coordinates from the polygon like this: [[llong1, llat1], [llong2, llat2], [llong3, llat3], [llong4, llat4]...etc]
        coords = list(polygon.exterior.coords)

        bounds = []
        for coord in coords:
            bounds.append([coord[0], coord[1]])

        # get the center of the polygon
        center = polygon.centroid

        # output name
        output_name = 'bbox'+str(int(center.x*1000))+'_'+str(int(center.y*1000))+'_'+str(year)+'_'+str(quad).zfill(2)

        # url data for downloading the image
        url_data = {'name': output_name, 'format': 'jpg', 'region': bounds, 'min': 0, 'max': 0.3, 'gamma': 1.0, 'dimensions': (1024, 1024)}

        #  save output_name, url_data to a npz file so we can use url_data as input to download the image
        out_dir = join(data_dir, 'urls')
        out_file_name = join(out_dir, 'urls_'+ collection_name)
        if not isdir(out_dir):
            mkdir(out_dir)
        
        # save the output_name and url_data to a npz file allowing pickle so we can use url_data as input to download the image
        np.savez(out_file_name, output_name=output_name, url_data=url_data)
        


        # test if it works by retrieving output_name and url_data from the npz file
        npzfile = np.load(out_file_name+'.npz')
        print(npzfile.files)
        output_name = npzfile['output_name']
        url_data = npzfile['url_data']
        print(output_name)
        print(url_data)


        
        
        # # get the image
        # try:
        #     url = image.getThumbURL({'name': output_name, 'format': 'jpg', 'region': bounds, 'min': 0, 'max': 0.3, 'gamma': 1.0, 'dimensions': (1024, 1024)})
        # except ee.ee_exception.EEException as e:
        #     print(e)
        #     # OUTER_BREAK = True
        #     continue
        # print(url)

        # if(isfile(join(data_dir, output_name+'.jpg'))):
        #     continue
        # urllib.request.urlretrieve(url, join(data_dir, output_name+'.jpg'))


get_image('tonga-volcano21', 'data')

# print(f'First date: {start_date}')
# print(f'Last date: {end_date}')

# # get the first and last polygon
# first_polygon = gdf['geometry'].iloc[0]
# last_polygon = gdf['geometry'].iloc[-1]

# # get the center of the first polygon
# center = first_polygon.centroid

# output = 'bbox'+str(int(center.x*1000))+'_'+str(int(center.y*1000))+'_'+str(year)+'_'+str(quad).zfill(2)
# print(output)
# try:
#     url = image.getThumbURL({'name': output, 'format': 'jpg', 'region': [[longi, lati+res], [longi+res, lati+res], [longi+res, lati], [longi, lati]], 'min': 0, 'max': 0.3, 'gamma': 1.0, 'dimensions': (1024, 1024)})
# 			except ee.ee_exception.EEException as e:
# 				print(e)
# 				# OUTER_BREAK = True
# 				continue
# 			print(url)