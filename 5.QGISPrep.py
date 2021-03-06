#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:13:22 2022

@author: camillewathne
"""

import geopandas as gpd
import pandas as pd

#%% Preparing for QGIS import

## Pulling in neighborhood file from Baltimore City
neighborhood_shp = gpd.read_file("QGIS Files/shapefile_neighborhoods.zip")
neighborhood_shp.columns = neighborhood_shp.columns.str.replace(' ', '')
neighborhood_shp = neighborhood_shp[["fid", "color_2", "name", "geodata_eg",
                                    "shape_stle", "SHAPE__Len", "SHAPE__Are", "geometry"]]
neighborhood_shp = neighborhood_shp.rename(columns={"name":"Neighborhood"})
neighborhood_shp["Neighborhood"] = neighborhood_shp["Neighborhood"].str.strip()
neighborhood_shp["Neighborhood"] = neighborhood_shp["Neighborhood"].str.upper()

## Pulling in full compiled data set
neighborhood_csv = pd.read_csv("Aggregated Files/neighborhood_full_data.csv")

## Creating compiled shapefile
combined_shp = neighborhood_shp.merge(neighborhood_csv, on=["Neighborhood"], how='outer', indicator=True)
print("\nMerge counts:\n\n", combined_shp["_merge"].value_counts() )
combined_shp = combined_shp.drop(columns="_merge")
combined_shp = combined_shp.set_index("Neighborhood")
combined_shp.columns = combined_shp.columns.str.replace(' ', '')
combined_shp = combined_shp.drop(columns="Unnamed:0")

## Determining percentages for each program area
combined_shp["per_anyprog"] = combined_shp["AnyProgram"] / combined_shp["TotalParcels"]
combined_shp["per_VAC"] = combined_shp["VAC:PROG"] / combined_shp["TotalParcels"]
combined_shp["per_REC"] = combined_shp["REC:PROG"] / combined_shp["TotalParcels"]
combined_shp["per_ADOPT"] = combined_shp["ADOPT:PROG"] / combined_shp["TotalParcels"]
combined_shp["per_BID"] = combined_shp["BID:PROG"] / combined_shp["TotalParcels"]
combined_shp["per_DEMO"] = combined_shp["DEMO:PROG"] / combined_shp["TotalParcels"]

## Determining how many from key programs are city owned
combined_shp["per_city_owned_any"] = combined_shp["CITYandANY"] / combined_shp["AnyVacant"]
combined_shp["per_city_owned_adopt"] = combined_shp["CITYandADOPT"] / combined_shp["ADOPT:PROG"]
combined_shp["per_city_owned_demo"] = combined_shp["CITYandDEMO"] / combined_shp["DEMO:PROG"]
combined_shp["per_city_owned_vacant"] = combined_shp["CITYandVAC"] / combined_shp["VAC:PROG"]

## Percent of vacants in receivership process
combined_shp["per_rec_of_vacants"] = combined_shp["VACandREC"] / combined_shp["VAC:PROG"]

## Demographic percentages
combined_shp["per_white"] = combined_shp["white"] / combined_shp["population"]
combined_shp["per_black"] = combined_shp["blk_afam"] / combined_shp["population"]
combined_shp["per_popchange"] = combined_shp["pop_chng"] / combined_shp["population"]

combined_shp.to_file("QGIS Files/baltimore_shp.gpkg",layer="Neighborhood")



