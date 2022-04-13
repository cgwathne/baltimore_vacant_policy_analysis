#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 22:24:37 2022

@author: camillewathne
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#%% Neighborhoods

## Opening real property data
neighborhoods = pd.read_csv("neighborhoods.csv")


## Prepping neighborhood data
neighborhoods = neighborhoods.drop(columns=["fid", "color_2", "geodata_eg", "created_da", 
                                            "last_edite", "last_edi_1", "shape_star","shape_stle", 
                                            "SHAPE__Length", "SHAPE__Area", "created_us"])
neighborhoods = neighborhoods.rename(columns={"name":"Neighborhood"})
neighborhoods["Neighborhood"] = neighborhoods["Neighborhood"].str.upper()
neighborhoods["Neighborhood"] = neighborhoods["Neighborhood"].str.replace(' ', '')

## Read in economic data from city compiled pdf documents
city_data_pdf = pd.read_csv("city_data_pdf.csv")
city_data_pdf["Neighborhood"] = city_data_pdf["Neighborhood"].str.upper()
city_data_pdf["Neighborhood"] = city_data_pdf["Neighborhood"].str.replace(' ', '')

## Merging city data from pdfs onto neighborhoods
neighborhoods = pd.merge(neighborhoods, city_data_pdf, on="Neighborhood", how='outer', indicator=True)
print("\nMerge counts:\n\n", neighborhoods["_merge"].value_counts() )
neighborhoods = neighborhoods.drop(columns="_merge")

## Read in neighborhood_agg
neighborhood_agg = pd.read_csv("neighborhood_agg.csv")
neighborhood_agg = neighborhood_agg.rename(columns={"REAL:Neighborhood":"Neighborhood"})
neighborhood_agg["Neighborhood"] = neighborhood_agg["Neighborhood"].str.upper()
neighborhood_agg["Neighborhood"] = neighborhood_agg["Neighborhood"].str.replace(' ', '')

## Merging neighborhood agg and neighborhoods to create neighborhood_data
neighborhood_data = pd.merge(neighborhood_agg, neighborhoods, on="Neighborhood", how='outer', indicator=True)
print("\nMerge counts:\n\n", neighborhood_data["_merge"].value_counts() )
neighborhood_data = neighborhood_data[neighborhood_data["_merge"].str.contains("left_only")==False]
neighborhood_data = neighborhood_data.drop(columns="_merge")

neighborhood_data = neighborhood_data.to_csv("neighborhood_data.csv")



