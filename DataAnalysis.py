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
print("\nNumber of parcels in 1 program:\n", overlap_summary.loc[1])
print("\nNumber of parcels in no programs:\n", overlap_summary.loc[0])

## Creating column for parcels that appear in ANY program
parcels["AnyProgram"] = np.where(parcels["Program#"] > 0, 1, 0)
print("Parcels in any program:", parcels["AnyProgram"].sum())
print("\nTotal number of parcels:", len(parcels), "\n")

print("\n-------------------------")

#%% Describing co-occurence between individual programs at the city level to determine next steps: program agg dataframe
programs = parcels.groupby(["VAC:PROG", "ADOPT:PROG", "REC:PROG", "BID:PROG"])
program_agg = pd.DataFrame()
program_agg["total_instances"] = programs.size()
print("\nCheck: does total match total number of parcels above?", program_agg["total_instances"].sum(), "\n")
print("(Determined no co-occurence between Receivership & OpenBid, and Receivership & Adopt)")

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

## 



#%% Creating neighborhood-level dataframe; Aggregating program and ownership data for parcels by neighborhood

## Grouping by neighborhood and program type
neighborhood_agg = parcels.groupby(["REAL:Neighborhood"]).agg({"VAC:PROG":np.sum, "REC:PROG":np.sum,
                                                              "ADOPT:PROG":np.sum,"BID:PROG":np.sum,
                                                              "VACandADOPT":np.sum, "VACandREC":np.sum, 
                                                              "VACandBID":np.sum, "ADOPTandBID":np.sum,
                                                              "REAL:Vacant":np.sum, "AnyProgram":np.sum})
## Calculating total parcels by neighborhood
parcels_by_neighborhood = parcels.groupby("REAL:Neighborhood")
neighborhood_agg["TotalParcels"] = parcels_by_neighborhood.size()


#%% Describing city ownership at parcel level, then adding to neighborhood aggregate

## Creating criteria for city ownership; colum in parcels to flag city ownership
city_list = ["MAYOR ", "CITY COUNCIL"]
parcels['CityOwned'] = False
for phrase in city_list:
    parcels['CityOwned'] = parcels["CityOwned"] | parcels['REAL:Owner'].str.contains(phrase)
parcels["CityOwned"] = parcels["CityOwned"].astype(int)
print("\nNumber of parcels owned by the city:", parcels["CityOwned"].sum())

## Determining city ownership at neighborhood level
cityowned_parcels = parcels.groupby(["REAL:Neighborhood", "CityOwned"])
cityowned_neighborhood = cityowned_parcels.size().unstack()

## Adding city ownership data to neighborhood agg 
neighborhood_agg = neighborhood_agg.merge(cityowned_neighborhood, on="REAL:Neighborhood", how='outer', indicator=True)
print("\nMerge counts:\n\n", neighborhood_agg["_merge"].value_counts() )
neighborhood_agg = neighborhood_agg.drop(columns=["_merge"])
neighborhood_agg = neighborhood_agg.rename(columns={1:"CityOwned", 0:"NotCityOwned"})

## Identifying which city owned properties are in 1 or more program
city_owned_program = parcels.loc[ (parcels["CityOwned"] == 1) & (parcels["Program#"] != 0)]
city_owned_program_neighborhood = city_owned_program.groupby("REAL:Neighborhood")
city_lots_inprogram = pd.DataFrame()
city_lots_inprogram["CityOwnedProgramSubset"] = city_owned_program_neighborhood.size()
neighborhood_agg = neighborhood_agg.merge(city_lots_inprogram, on= "REAL:Neighborhood", how="outer", indicator=True)
print("\nMerge counts:\n\n", neighborhood_agg["_merge"].value_counts() )
neighborhood_agg = neighborhood_agg.drop(columns=["_merge"])
print("Total city owned parcels:", parcels["CityOwned"].sum())
print("\nTotal city owned parcels in one or more vacant-related programs:\n", round(neighborhood_agg["CityOwnedProgramSubset"].sum()))


#%% Describing additional city vacants at parcel level, then adding to neighborhood aggregate 

## Understanding real property vacants vs prog vacants vs city ownership
vacant_test = parcels.groupby(["VAC:PROG", "REAL:Vacant", "CityOwned"])
vacanttest = pd.DataFrame()
vacanttest["total_instances"] = vacant_test.size()

## Creating column for lots that are in real_property vacant but NOT in vacant program
realprop_vacant = parcels.loc[ (parcels["REAL:Vacant"] == 1) & (parcels["VAC:PROG"] == 0)]
realprop_vacant_neighborhood = realprop_vacant.groupby("REAL:Neighborhood")
realprop_vacant_new = pd.DataFrame()
realprop_vacant_new["AdditionalVacants"] = realprop_vacant_neighborhood.size()
neighborhood_agg = neighborhood_agg.merge(realprop_vacant_new, on= "REAL:Neighborhood", how="outer", indicator=True)
print("\nMerge counts:\n\n", neighborhood_agg["_merge"].value_counts() )
neighborhood_agg = neighborhood_agg.drop(columns=["_merge"])
print("Total additional vacants from real property data:", round(neighborhood_agg["AdditionalVacants"].sum()))


neighborhood_agg.to_csv("neighborhood_agg.csv")






