# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Jay Bassan

Process large shapefiles from (https://www.hydrosheds.org/products/hydrolakes) into smaller,
more managable shapefiles of lakes, rivers etc.
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# lakes first
lakes_in = gpd.read_file('./data/raw/HydroLAKES_polys_v10.shp')

# filter into a few dataframes containing lakes with a varying area cut off
# this allows tweaking maps using faster, smaller datasets then rerendering with all the lakes
lakes_all = lakes_in.copy()
lakes_1sqkm = lakes_in[lakes_in['Lake_area'] >= 1.].copy()
lakes_10sqkm = lakes_in[lakes_in['Lake_area'] >= 10.].copy()
lakes_100sqkm = lakes_in[lakes_in['Lake_area'] >= 100.].copy()

print(f'{lakes_all.shape[0]:,} total lakes.')
print(f'{lakes_1sqkm.shape[0]:,} lakes >= 1 sq km')
print(f'{lakes_10sqkm.shape[0]:,} lakes >= 10 sq km')
print(f'{lakes_100sqkm.shape[0]:,} lakes >= 100 sq km')

lakes_all.to_file('./data/processed/lakes_all.shp')
lakes_1sqkm.to_file('./data/processed/lakes_1sqkm.shp')
lakes_10sqkm.to_file('./data/processed/lakes_10sqkm.shp')
lakes_100sqkm.to_file('./data/processed/lakes_100sqkm.shp')

print('Lakes done.')

# free up memory
del lakes_in, lakes_all, lakes_1sqkm, lakes_10sqkm, lakes_100sqkm


# now do rivers, same idea
rivers_in = gpd.read_file('./data/raw/HydroRIVERS_v10.shp')

rivers_all = rivers_in.copy()
rivers_1cms = rivers_in[rivers_in['DIS_AV_CMS'] >= 1.].copy()
rivers_10cms = rivers_in[rivers_in['DIS_AV_CMS'] >= 10.].copy()
rivers_100cms = rivers_in[rivers_in['DIS_AV_CMS'] >= 100.].copy()
rivers_1000cms = rivers_in[rivers_in['DIS_AV_CMS'] >= 1000.].copy()

print(f'{rivers_in.shape[0]:,} total rivers')
print(f'{rivers_1cms.shape[0]:,} >= 1 CMS')
print(f'{rivers_10cms.shape[0]:,} >= 10 CMS')
print(f'{rivers_100cms.shape[0]:,} >= 100 CMS')
print(f'{rivers_1000cms.shape[0]:,} >= 1000 CMS')

rivers_all.to_file('./data/processed/rivers_all.shp')
rivers_1cms.to_file('./data/processed/rivers_1cms.shp')
rivers_10cms.to_file('./data/processed/rivers_10cms.shp')
rivers_100cms.to_file('./data/processed/rivers_100cms.shp')
rivers_1000cms.to_file('./data/processed/rivers_1000cms.shp')

print('Rivers done.')








