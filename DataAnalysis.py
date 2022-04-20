#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 16:03:12 2022

@author: camillewathne
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

##Reading compiled data
parcels = pd.read_csv("Compiled_Sheet.csv")

## Adding additional real property vacants - vacant program or real vacant column
parcels["VACorREALVAC"] = parcels[["VAC:PROG", "REAL:Vacant"]].sum(axis=1)
parcels["VACorREALVAC"] = parcels["VACorREALVAC"].replace(2, 1)
print("\nTotal vacants in either program vacant or real property vacant", parcels["VACorREALVAC"].sum())
## Replacing Vacant Program column with Vacant or Real Property Vacant numbers
parcels = parcels.drop(columns="VAC:PROG")
parcels = parcels.rename(columns = {"VACorREALVAC": "VAC:PROG"})
print("\nNew number of vacants from newly created inclusive column:", round(parcels["VAC:PROG"].sum()))

#%% Creating columns for program enrollment and co-occurence of programs at parcel level

## Reclassifying program type and summing programs
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
print("\nCheck: does total number match total number of parcels above?", program_agg["total_instances"].sum(), "\n")
print("\nDescription of program co-occurance:\n", program_agg)
print("(Determined trivial (<5) co-occurence between Receivership & OpenBid, and Receivership & Adopt)")

## Co-occurence between Vacants and Adopt
parcels["VACandADOPT"] = parcels[["VAC:PROG", "ADOPT:PROG"]].sum(axis=1)
parcels["VACandADOPT"] = parcels["VACandADOPT"].replace(1, 0)
parcels["VACandADOPT"] = parcels["VACandADOPT"].replace(2, 1)
print("\nTotal co-occurence between Vacants and Adopt:", round(parcels["VACandADOPT"].sum()))

## Co-occurence between vacants and receivership
parcels["VACandREC"] = parcels[["VAC:PROG", "REC:PROG"]].sum(axis=1)
parcels["VACandREC"] = parcels["VACandREC"].replace(1, 0)
parcels["VACandREC"] = parcels["VACandREC"].replace(2, 1)
print("\nTotal co-occurence between Vacants and Receivership:", round(parcels["VACandREC"].sum()))

## Co-occurence between vacants and open bid
parcels["VACandBID"] = parcels[["BID:PROG", "VAC:PROG"]].sum(axis=1)
parcels["VACandBID"] = parcels["VACandBID"].replace(1, 0)
parcels["VACandBID"] = parcels["VACandBID"].replace(2, 1)
print("\nTotal co-occurence between Vacants and Open bid:", round(parcels["VACandBID"].sum()))

## Co-occurence between adopt and open bid
parcels["ADOPTandBID"] = parcels[["BID:PROG", "ADOPT:PROG"]].sum(axis=1)
parcels["ADOPTandBID"] = parcels["ADOPTandBID"].replace(1, 0)
parcels["ADOPTandBID"] = parcels["ADOPTandBID"].replace(2, 1)
print("\nTotal co-occurence between Adopt and Open bid:", round(parcels["ADOPTandBID"].sum()))


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


#%% Describing city ownership at parcel level, then adding to neighborhood aggregate - maybe check city program due to dashboard data

## Creating criteria for city ownership; column in parcels to flag city ownership
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
city_check = parcels["CityOwned"] == 1
parcels_check = parcels["Program#"] != 0
in_both = city_check & parcels_check
city_owned_program = parcels[in_both]
city_owned_program_neighborhood = city_owned_program.groupby("REAL:Neighborhood")
city_lots_inprogram = pd.DataFrame()
city_lots_inprogram["CityOwnedProgramSubset"] = city_owned_program_neighborhood.size()
neighborhood_agg = neighborhood_agg.merge(city_lots_inprogram, on= "REAL:Neighborhood", how="outer", indicator=True)
print("\nMerge counts:\n\n", neighborhood_agg["_merge"].value_counts() )
neighborhood_agg = neighborhood_agg.drop(columns=["_merge"])
print("Total city owned parcels:", parcels["CityOwned"].sum())
print("\nTotal city owned parcels in one or more vacant-related programs:\n", round(neighborhood_agg["CityOwnedProgramSubset"].sum()))

## Saving to file
neighborhood_agg.to_csv("neighborhood_agg.csv")




