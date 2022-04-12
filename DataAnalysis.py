#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 16:03:12 2022

@author: camillewathne
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#%% Creating columns for program enrollment and co-occurence of programs at parcel level

##Reading compiled data; reclassifying program type and summing programs
parcels = pd.read_csv("Compiled_Sheet.csv")
program_list = ["VAC:PROG", "ADOPT:PROG", "REC:PROG", "BID:PROG"]
parcels[program_list] = parcels[program_list].fillna(0)
parcels["Program#"] = parcels[program_list].sum(axis=1)

## Describing co-occurence between programs at city level
overlap = parcels.groupby("Program#")
overlap_summary = pd.DataFrame()
overlap_summary["Programs"] = overlap.size()
print("\nNumber of parcels in 3 programs:\n", overlap_summary.loc[3])
print("\nNumber of parcels in 2 programs:\n", overlap_summary.loc[2])
print("\nNumber of parcels in 1 program:\n\n", overlap_summary.loc[1])
print("\nNumber of parcels in no programs:\n\n", overlap_summary.loc[0])
print("\nTotal number of parcels:", len(parcels), "\n")

print("\n-------------------------")

## Describing co-occurence between individual programs at the city level 
programs = parcels.groupby(["VAC:PROG", "ADOPT:PROG", "REC:PROG", "BID:PROG"])
program_agg = pd.DataFrame()
program_agg["total_instances"] = programs.size()
print("\nCheck: does total match number of parcels above?", program_agg["total_instances"].sum(), "\n")
print("Determined no co-occurence between Receivership&OpenBid, and Receivership&Adopt")

## Co-occurence between Vacants and Adopt
parcels["VACandADOPT"] = parcels[["VAC:PROG", "ADOPT:PROG"]].sum(axis=1)
parcels["VACandADOPT"] = parcels["VACandADOPT"].replace(1, 0)
parcels["VACandADOPT"] = parcels["VACandADOPT"].replace(2, 1)
print("\nTotal co-occurence between Vacants and Adopt:", parcels["VACandADOPT"].sum())

## Co-occurence between vacants and receivership
parcels["VACandREC"] = parcels[["VAC:PROG", "REC:PROG"]].sum(axis=1)
parcels["VACandREC"] = parcels["VACandREC"].replace(1, 0)
parcels["VACandREC"] = parcels["VACandREC"].replace(2, 1)
print("\nTotal co-occurence between Vacants and Receivership:", parcels["VACandREC"].sum())

## Co-occurence between vacants and open bid
parcels["VACandBID"] = parcels[["BID:PROG", "VAC:PROG"]].sum(axis=1)
parcels["VACandBID"] = parcels["VACandBID"].replace(1, 0)
parcels["VACandBID"] = parcels["VACandBID"].replace(2, 1)
print("\nTotal co-occurence between Vacants and Open bid:", parcels["VACandBID"].sum())

## Co-occurence between adopt and open bid
parcels["ADOPTandBID"] = parcels[["BID:PROG", "ADOPT:PROG"]].sum(axis=1)
parcels["ADOPTandBID"] = parcels["ADOPTandBID"].replace( 1, 0)
parcels["ADOPTandBID"] = parcels["ADOPTandBID"].replace(2, 1)
print("\nTotal co-occurence between Adopt and Open bid:", parcels["ADOPTandBID"].sum())

## Creating neighborhood-level dataframe; Aggregating program and ownership data for parcels by neighborhood

## Grouping by neighborhood and program type - ISSUE - should only be counting if value=2
neighborhood_agg = parcels.groupby(["REAL:Neighborhood"]).agg({"VAC:PROG":np.sum, "REC:PROG":np.sum,
                                                              "ADOPT:PROG":np.sum,"BID:PROG":np.sum,
                                                              "VACandADOPT":np.sum, "VACandREC":np.sum, 
                                                              "VACandBID":np.sum, "ADOPTandBID":np.sum,
                                                              "REAL:Vacant":np.sum})

#%% Describing city ownership at parcel level, then adding to neighborhood aggregate

## Calculating total parcels by neighborhood
parcels_by_neighborhood = parcels.groupby("REAL:Neighborhood")
neighborhood_agg["TotalParcels"] = parcels_by_neighborhood.size()

## Creating criteria for city ownership; colum in parcels to flag city ownership
city_list = ["MAYOR ", "CITY COUNCIL"]
parcels['CityOwned'] = False
for phrase in city_list:
    parcels['CityOwned'] = parcels["CityOwned"] | parcels['REAL:Owner'].str.contains(phrase)
print("\nNumber of parcels owned by the city:", parcels["CityOwned"].sum())

## Determining city ownership
cityowned_parcels = parcels.groupby(["REAL:Neighborhood", "CityOwned"])
cityowned_neighborhood = cityowned_parcels.size().unstack()

## Adding city ownership data to neighborhood agg - ISSUE WITH RENAMING TRUE FALSE columns
neighborhood_agg = neighborhood_agg.merge(cityowned_neighborhood, on="REAL:Neighborhood", how='outer', indicator=True)
print("\nMerge counts:\n\n", neighborhood_agg["_merge"].value_counts() )
neighborhood_agg = neighborhood_agg.drop(columns=["_merge"])

##neighborhood_agg = neighborhood_agg.rename(columns={"True":"CityOwned", "False":"NotCityOwned"})

#%%

## Understanding real property vacants vs prog vacants vs city ownership
vacant_test = parcels.groupby(["VAC:PROG", "REAL:Vacant", "CityOwned"])
vacanttest = pd.DataFrame()
vacanttest["total_instances"] = vacant_test.size()

neighborhood_agg.to_csv("neighborhood_agg.csv")






