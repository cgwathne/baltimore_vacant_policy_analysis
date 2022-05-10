#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 22:24:37 2022

@author: camillewathne
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#%% Creating compiled neighborhood file that merges parcel data to demographic info

## Opening neighborhood file
neighborhoods = pd.read_csv("Source Files/neighborhoods.csv")


## Prepping neighborhood data from city (and 2020 census)
neighborhoods = neighborhoods.drop(columns=["fid", "housing", "occupied", "occ_own", "occ_rent", 
                                            "vacant", "vac_rent", "vac_sale", "vac_other", 
                                            "color_2", "geodata_eg", "created_da", 
                                            "last_edite", "last_edi_1", "shape_star","shape_stle", 
                                            "SHAPE__Length", "SHAPE__Area", "created_us", "age0_4",
                                            "age5_11", "age12_14", "age15_17", "age18_24", "age25_34",
                                            "age35_44", "age45_64", "age65ovr", "married", "married18",
                                            "malehh", "femalehh", "femalehh18", "malehh18"])
neighborhoods = neighborhoods.rename(columns={"name":"Neighborhood"})
neighborhoods["Neighborhood"] = neighborhoods["Neighborhood"].str.upper()
neighborhoods["Neighborhood"] = neighborhoods["Neighborhood"].str.strip()
neighborhoods["Neighborhood"] = neighborhoods["Neighborhood"].str.replace(r"\s+", " ", regex=True)

## Read in economic data from manually coded pdf documents
city_data_pdf = pd.read_csv("Aggregated Files/city_data_pdf.csv")
city_data_pdf["Neighborhood"] = city_data_pdf["Neighborhood"].str.upper()
city_data_pdf["Neighborhood"] = city_data_pdf["Neighborhood"].str.strip()
city_data_pdf["Neighborhood"] = city_data_pdf["Neighborhood"].str.replace(r"\s+", " ", regex=True)
neighborhoods = pd.merge(neighborhoods, city_data_pdf, on="Neighborhood", how='outer', indicator=True)
print("\nMerge counts:\n\n", neighborhoods["_merge"].value_counts() )
neighborhoods = neighborhoods.drop(columns="_merge")

## Read in parcel and program information from neighborhood_agg file
neighborhood_agg = pd.read_csv("Aggregated Files/neighborhood_parcel_agg.csv")
neighborhood_agg = neighborhood_agg.rename(columns={"REAL:Neighborhood":"Neighborhood"})
neighborhood_agg["Neighborhood"] = neighborhood_agg["Neighborhood"].str.upper()
neighborhood_agg["Neighborhood"] = neighborhood_agg["Neighborhood"].str.strip()
neighborhood_agg["Neighborhood"] = neighborhood_agg["Neighborhood"].str.replace(r"\s+", " ", regex=True)

## Merging neighborhood agg and neighborhoods to create neighborhood_data
neighborhood_data = pd.merge(neighborhood_agg, neighborhoods, on="Neighborhood", how='outer', indicator=True)
print("\nMerge counts:\n\n", neighborhood_data["_merge"].value_counts() )
neighborhood_data = neighborhood_data[neighborhood_data["_merge"].str.contains("left_only")==False]
neighborhood_data = neighborhood_data.drop(columns="_merge")

neighborhood_data.to_csv("Aggregated Files/neighborhood_full_data.csv")



