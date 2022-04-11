#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 16:03:12 2022

@author: camillewathne
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#%%

##Reading compiled data; reclassifying program type and summing
parcels = pd.read_csv("Compiled_Sheet.csv")
program_list = ["VAC:PROG", "ADOPT:PROG", "REC:PROG", "BID:PROG"]
parcels[program_list] = parcels[program_list].fillna(0)
parcels["Program#"] = parcels[program_list].sum(axis=1)

parcels["VACandADOPT"] = parcels[["VAC:PROG", "ADOPT:PROG"]].sum(axis=1)
parcels["VACandREC"] = parcels[["VAC:PROG", "REC:PROG"]].sum(axis=1)
parcels["ADOPTandREC"] = parcels[["ADOPT:PROG", "REC:PROG"]].sum(axis=1)
parcels["BIDandVAC"] = parcels[["BID:PROG", "VAC:PROG"]].sum(axis=1)
parcels["BIDandADOPT"] = parcels[["BID:PROG", "ADOPT:PROG"]].sum(axis=1)
parcels["BIDandREC"] = parcels[["BID:PROG", "REC:PROG"]].sum(axis=1)

## How many parcels appear in 2 or more programs
overlap = parcels.groupby("Program#")
overlap_summary = pd.DataFrame()
overlap_summary["Programs"] = overlap.size()
print("\nNumber of parcels in 3 programs:\n", overlap_summary.loc[3])
print("\nNumber of parcels in 2 programs:\n", overlap_summary.loc[2])
print("\nNumber of parcels in 1 program:\n\n", overlap_summary.loc[1])
print("\nNumber of parcels in no programs:\n\n", overlap_summary.loc[0])
print("\nTotal number of parcels:", len(parcels), "\n")

print("\n-------------------------")

## How many parcels appear in Vacants and Adopt
overlap1 = parcels.groupby("VACandADOPT")
overlap1_summary = pd.DataFrame()
overlap1_summary["VACandADOPT"] = overlap1.size()
print("\nNumber of parcels in Vacants and Adopt-a-Lot:\n", overlap1_summary.loc[2.0])

## How many parcels appear in Vacants and Receivership
overlap2 = parcels.groupby("VACandREC")
overlap2_summary = pd.DataFrame()
overlap2_summary["VACandREC"] = overlap2.size()
print("\nNumber of parcels in Vacants and Receivership:\n", overlap2_summary.loc[2.0])

## How many parcels appear in Adopt-a_lot and Receivership - NOT APPLICABLE
##overlap3 = parcels.groupby("ADOPTandREC")
###overlap3_summary = pd.DataFrame()
##overlap3_summary["ADOPTandREC"] = overlap3.size()
##print("\nNumber of parcels in Adopt-a-Lot and Receivership:\n", overlap3_summary.loc[2.0])

## How many parcels appear in Open Bid and Vacants
overlap4 = parcels.groupby("BIDandVAC")
overlap4_summary = pd.DataFrame()
overlap4_summary["BIDandVAC"] = overlap4.size()
print("\nNumber of parcels in Open Bid and Vacants:\n", overlap4_summary.loc[2.0])

## How many parcels appear in Open Bid and Adopt
overlap5 = parcels.groupby("BIDandADOPT")
overlap5_summary = pd.DataFrame()
overlap5_summary["BIDandADOPT"] = overlap5.size()
print("\nNumber of parcels in Open Bid and Adopt:\n", overlap5_summary.loc[2.0])

## How many parcels appear in Open Bid and Receivership - NOT APPLICABLE
##overlap6 = parcels.groupby("BIDandREC")
##overlap6_summary = pd.DataFrame()
##overlap6_summary["BIDandREC"] = overlap6.size()
##print("\nNumber of parcels in Open Bid and Receivership:\n", overlap6_summary.loc[2.0])

#%%
#Describing ownership in parcels

## Grouping by neighborhood and program type
neighborhood_agg = parcels.groupby(["REAL:Neighborhood"]).agg({"VAC:PROG":np.sum, "REC:PROG":np.sum,
                                                               "ADOPT:PROG":np.sum,"BID:PROG":np.sum,
                                                               "VACandADOPT":np.sum, "VACandREC":np.sum, 
                                                               "BIDandVAC":np.sum, "BIDandADOPT":np.sum})

parcels_by_neighborhood = parcels.groupby("REAL:Neighborhood")
neighborhood_agg["TotalParcels"] = parcels_by_neighborhood.size()











