#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 21:22:56 2023

@author: jayb

map of the rivers and lakes of TN
"""
import conda
import os
import geopandas as gpd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from skimage import morphology, filters
import pyproj

conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib

# read the states shapefile
states = gpd.read_file('../data/cb_2018_us_state_500k/cb_2018_us_state_500k.shp')

# get tennessee
tn = states[states['STUSPS'] == 'TN']

# get rivers and lakes
rivers = gpd.read_file('../data/processed/rivers_10cms.shp')
print('Rivers loaded.')
lakes = gpd.read_file('../data/processed/lakes_all.shp')
print('Lakes loaded.')






# read usa shapefile for land 
usa = gpd.read_file('../data/WB_countries_Admin0_10m/WB_countries_Admin0_10m.shp')
usa = usa[usa['FORMAL_EN'] == 'United States of America']

# filter
lakes = lakes[lakes['Country'] == 'United States of America']

keep_continent = []
for river_id in rivers['HYRIV_ID']:
    cont_id = str(river_id)[0]
    if cont_id == '7':
        keep_continent.append(True)
    else:
        keep_continent.append(False)
        
rivers = rivers.iloc[keep_continent, :]




# get projection right
crs_str = """PROJCS["The_World_From_Space",
    GEOGCS["GCS_Sphere_ARC_INFO",
        DATUM["D_Sphere_ARC_INFO",
            SPHEROID["Sphere_ARC_INFO",6370997.0,0.0]],
        PRIMEM["Greenwich",0.0],
        UNIT["Degree",0.0174532925199433]],
    PROJECTION["Orthographic"],
    PARAMETER["False_Easting",0.0],
    PARAMETER["False_Northing",0.0],
    PARAMETER["Longitude_Of_Center",-86.362],
    PARAMETER["Latitude_Of_Center",35.860],
    UNIT["Meter",1.0]]"""
    
crs = pyproj.CRS(crs_str)


rivers = rivers.to_crs(crs)
lakes = lakes.to_crs(crs)
tn = tn.to_crs(crs)
usa = usa.to_crs(crs)

#get river linewidths, massage them to display nicely
lws = rivers['DIS_AV_CMS'].copy().to_numpy(dtype=float)
lws = np.sqrt(lws*30)
lws = np.clip(lws, 0, 10_000)
lws = lws / lws.max()



xlim0 = -600000
xlim1 = 600000
ylim0 = -600000
ylim1 = 600000










# make the figures and save
dpi=1200


fig, ax = plt.subplots(figsize=(12,12), dpi=dpi)
tn.plot(
    ax=ax,
    color='k',
)
plt.xlim(xlim0, xlim1)
plt.ylim(ylim0, ylim1)
plt.tight_layout()
ax.axis('off')
plt.savefig('../images/layer_tn_state.png', bbox_inches='tight')
plt.close()


fig, ax = plt.subplots(figsize=(12,12), dpi=dpi)
rivers.plot(
    ax=ax,
    color='k',
    lw=lws
)
plt.xlim(xlim0, xlim1)
plt.ylim(ylim0, ylim1)
plt.tight_layout()
ax.axis('off')
plt.savefig('../images/layer_tn_rivers.png', bbox_inches='tight')
plt.close()


fig, ax = plt.subplots(figsize=(12,12), dpi=dpi)
lakes.plot(
    ax=ax,
    color='k',
)
plt.xlim(xlim0, xlim1)
plt.ylim(ylim0, ylim1)
plt.tight_layout()
ax.axis('off')
plt.savefig('../images/layer_tn_lakes.png', bbox_inches='tight')
plt.close()



fig, ax = plt.subplots(figsize=(12,12), dpi=dpi)
usa.plot(
    ax=ax,
    color='k',
)
plt.xlim(xlim0, xlim1)
plt.ylim(ylim0, ylim1)
plt.tight_layout()
ax.axis('off')
plt.savefig('../images/layer_tn_usa.png', bbox_inches='tight')
plt.close()







