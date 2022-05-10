#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 16:03:12 2022

@author: camillewathne
"""

import pandas as pd
import numpy as np

#%% Creating unduplicated count between vacants in "VAC PROG" and coded as vacant in real_property

parcels = pd.read_csv("Aggregated Files/compiled_parcels.csv")

## Adding additional real property vacants - vacant program or real vacant column
parcels["VACorREALVAC"] = parcels[["VAC:PROG", "REAL:Vacant"]].sum(axis=1)
parcels["VACorREALVAC"] = parcels["VACorREALVAC"].replace(2, 1)
print("\nTotal vacants in either program vacant or real property vacant", round(parcels["VACorREALVAC"].sum()))

parcels = parcels.drop(columns="VAC:PROG")
parcels = parcels.rename(columns = {"VACorREALVAC": "VAC:PROG"})
print("\nNew number of vacants from newly created inclusive column:", round(parcels["VAC:PROG"].sum()))

#%% Creating columns for co-occurance of vacancy classifications and program interventions

any_vacant_list = ["VAC:PROG", "ADOPT:PROG", "REC:PROG", "BID:PROG", "DEMO:PROG"]
any_program_list = ["ADOPT:PROG", "REC:PROG", "BID:PROG", "DEMO:PROG"]

## Identifying number of unduplicated parcels that appear in any of the vacancy classifications 
parcels[any_vacant_list] = parcels[any_vacant_list].fillna(0)
parcels["Classification#"] = parcels[any_vacant_list].sum(axis=1)

## Describing co-occurence between classifications at city level
overlap = parcels.groupby("Classification#")
overlap_summary = pd.DataFrame()
overlap_summary["Programs"] = overlap.size()
print("\nNumber of parcels in 3 classifications:\n", overlap_summary.loc[3])
print("\nNumber of parcels in 2 classifications:\n", overlap_summary.loc[2])
print("\nNumber of parcels in 1 classification:\n", overlap_summary.loc[1])
print("\nNumber of parcels in no classifications:\n", overlap_summary.loc[0])

## Parcels that appear in ANY classification
parcels["AnyVacant"] = np.where(parcels["Classification#"] > 0, 1, 0)
print("Parcels in any program:", parcels["AnyVacant"].sum())
print("\nTotal number of parcels:", len(parcels), "\n")

## Identifying number of unduplicated parcels that appear in any of the program interventions
parcels[any_program_list] = parcels[any_program_list].fillna(0)
parcels["Program#"] = parcels[any_program_list].sum(axis=1)
parcels["AnyProgram"] = np.where(parcels["Program#"] > 0, 1, 0)
print("Parcels in any program:", parcels["AnyProgram"].sum())
print("\n-------------------------")

#%% Identifying which parcels belong to the city

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

#%% Describing co-occurence between individual programs at the city level to determine next steps: program agg dataframe
classifications = parcels.groupby(["VAC:PROG", "ADOPT:PROG", "REC:PROG", "BID:PROG", "DEMO:PROG", "CityOwned"])
classification_agg = pd.DataFrame()
classification_agg["total_instances"] = classifications.size()
print("\nCheck: does total number match total number of parcels above?", classification_agg["total_instances"].sum(), "\n")
print("\nDescription of program co-occurance:\n", classification_agg)
##print("(Determined trivial (<5) co-occurence between Receivership & OpenBid, and Receivership & Adopt)")

## Examining co-occurance of largest overlapping programs
## Co-occurence between city and Any Vacant
parcels["CITYandANY"] = parcels[["CityOwned", "AnyVacant"]].sum(axis=1)
parcels["CITYandANY"] = parcels["CITYandANY"].replace(1, 0)
parcels["CITYandANY"] = parcels["CITYandANY"].replace(2, 1)
print("\nTotal co-occurence between City and AnyVacant:", round(parcels["CITYandANY"].sum()))

## Co-occurence between City and Adopt
parcels["CITYandADOPT"] = parcels[["CityOwned", "ADOPT:PROG"]].sum(axis=1)
parcels["CITYandADOPT"] = parcels["CITYandADOPT"].replace(1, 0)
parcels["CITYandADOPT"] = parcels["CITYandADOPT"].replace(2, 1)
print("\nTotal co-occurence between City and Adopt:", round(parcels["CITYandADOPT"].sum()))

## Co-occurence between city and demo
parcels["CITYandDEMO"] = parcels[["CityOwned", "DEMO:PROG"]].sum(axis=1)
parcels["CITYandDEMO"] = parcels["CITYandDEMO"].replace(1, 0)
parcels["CITYandDEMO"] = parcels["CITYandDEMO"].replace(2, 1)
print("\nTotal co-occurence between City and Demo:", round(parcels["CITYandDEMO"].sum()))

## Co-occurence between city and vacants
parcels["CITYandVAC"] = parcels[["CityOwned", "VAC:PROG"]].sum(axis=1)
parcels["CITYandVAC"] = parcels["CITYandVAC"].replace(1, 0)
parcels["CITYandVAC"] = parcels["CITYandVAC"].replace(2, 1)
print("\nTotal co-occurence between City and Vacants:", round(parcels["CITYandVAC"].sum()))

## Co-occurence between vacants and receivership
parcels["VACandREC"] = parcels[["VAC:PROG", "REC:PROG"]].sum(axis=1)
parcels["VACandREC"] = parcels["VACandREC"].replace(1, 0)
parcels["VACandREC"] = parcels["VACandREC"].replace(2, 1)
print("\nTotal co-occurence between Vacants and Receivership:", round(parcels["VACandREC"].sum()))


#%% Creating neighborhood-level dataframe; Aggregating program and ownership data for parcels by neighborhood

## Grouping by neighborhood and program type
neighborhood_agg = parcels.groupby(["REAL:Neighborhood"]).agg({"VAC:PROG":np.sum, "REC:PROG":np.sum,
                                                              "ADOPT:PROG":np.sum,"BID:PROG":np.sum,
                                                              "DEMO:PROG":np.sum, "CityOwned":np.sum, "CITYandANY":np.sum,
                                                              "CITYandADOPT":np.sum, "CITYandDEMO":np.sum, "CITYandVAC":np.sum, 
                                                              "VACandREC":np.sum, "AnyVacant":np.sum, "AnyProgram":np.sum})

parcels_by_neighborhood = parcels.groupby("REAL:Neighborhood")
neighborhood_agg["TotalParcels"] = parcels_by_neighborhood.size()
neighborhood_agg.to_csv("Aggregated Files/neighborhood_parcel_agg.csv")


