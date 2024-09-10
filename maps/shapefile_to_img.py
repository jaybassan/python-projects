# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jay Bassan

Take processed shapefiles of lakes and rivers and save those of
a particular country, in a particular projection.
"""
import geopandas as gpd
import pyproj
import numpy as np
import matplotlib.pyplot as plt

### parameters to change ###
country = 'Canada'

lake_size = '10sqkm'
river_size = '100cms'

crs_str = """PROJCS["The_World_From_Space",
    GEOGCS["GCS_Sphere_ARC_INFO",
        DATUM["D_Sphere_ARC_INFO",
            SPHEROID["Sphere_ARC_INFO",6370997.0,0.0]],
        PRIMEM["Greenwich",0.0],
        UNIT["Degree",0.0174532925199433]],
    PROJECTION["Orthographic"],
    PARAMETER["False_Easting",0.0],
    PARAMETER["False_Northing",0.0],
    PARAMETER["Longitude_Of_Center",-96.46666],
    PARAMETER["Latitude_Of_Center",62.4],
    UNIT["Meter",1.0]]"""

dpi = 1800

lw_clip = 15_000
lw_exponent = 0.7


# read the rivers, lakes, and country shape files
rivers = gpd.read_file(f'./data/processed/rivers_{river_size}.shp')
print('Rivers loaded.')
lakes = gpd.read_file(f'./data/processed/lakes_{lake_size}.shp')
print('Lakes loaded.')
world = gpd.read_file('./data/processed/WB_countries_Admin0_10m/WB_countries_Admin0_10m.shp')
print('World loaded.')

# get canada from the world shape file, and define rest of world
canada = world.loc[world['FORMAL_EN'] == country]
row = world.loc[world['FORMAL_EN'] != country]

# set and change the projection
crs = pyproj.CRS(crs_str)

rivers = rivers.to_crs(crs)
lakes = lakes.to_crs(crs)
canada = canada.to_crs(crs)
row = row.to_crs(crs)
print('Projection changed.')

# scale the river linewidths
lws = rivers['DIS_AV_CMS'].to_numpy()
lws = np.clip(lws, 0.0, lw_clip)
lws = lws / lws.max()
lws = lws ** lw_exponent

# make the figures and save
# country of interest
fig, ax = plt.subplots(figsize=(12, 12), dpi=dpi)
canada.plot(
    ax=ax,
    color='k',
)
plt.xlim(-5e6, 5e6)
plt.ylim(-5e6, 5e6)
plt.tight_layout()
ax.axis('off')
plt.savefig(f'./images/{country}_{dpi}dpi.png', bbox_inches='tight')
plt.close()

# rest of the world
fig, ax = plt.subplots(figsize=(12, 12), dpi=dpi)
row.plot(
    ax=ax,
    color='k',
)
plt.xlim(-5e6, 5e6)
plt.ylim(-5e6, 5e6)
plt.tight_layout()
ax.axis('off')
plt.savefig(f'./images/non{country}_{dpi}dpi.png', bbox_inches='tight')
plt.close()

# lakes
fig, ax = plt.subplots(figsize=(12, 12), dpi=dpi)
lakes.plot(
    ax=ax,
    color='k',
)
plt.xlim(-5e6, 5e6)
plt.ylim(-5e6, 5e6)
plt.tight_layout()
ax.axis('off')
plt.savefig(f'./images/lakes{lake_size}_{dpi}dpi.png', bbox_inches='tight')
plt.close()





# rivers
fig, ax = plt.subplots(figsize=(12, 12), dpi=dpi)
rivers.plot(
    ax=ax,
    color='k',
    lw=lws
)
plt.xlim(-5e6, 5e6)
plt.ylim(-5e6, 5e6)
plt.tight_layout()
ax.axis('off')
plt.savefig(f'./images/rivers{river_size}_{dpi}dpi.png', bbox_inches='tight')
plt.close()

