#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 15:45:30 2022

@author: camillewathne
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#%% Merging individual, cleaned data files to created aggregated, parcel-level sheet

## Opening real property data
RealProperty = pd.read_csv("Cleaned Files/real_property_clean.csv")
RealProperty.columns = RealProperty.columns.str.replace(' ', '')
RealProperty = RealProperty.drop(columns=["Unnamed:0"])
## Opening adopt a lot data
AdoptALot = pd.read_csv("Cleaned Files/adopt_a_lot_clean.csv")
AdoptALot.columns = AdoptALot.columns.str.replace(' ', '')
AdoptALot = AdoptALot.drop(columns=["Unnamed:0"])
## Opening vacants
Vacants = pd.read_csv("Cleaned Files/vacants_clean.csv")
Vacants.columns = Vacants.columns.str.replace(' ', '')
Vacants = Vacants.drop(columns=["Unnamed:0"])
## Opening receivership data
Receivership = pd.read_csv("Cleaned Files/receiver_clean.csv")
Receivership.columns = Receivership.columns.str.replace(' ', '')
Receivership = Receivership.drop(columns=["Unnamed:0"])
## Opening open bid data
OpenBid = pd.read_csv("Cleaned Files/open_bid_clean.csv")
OpenBid.columns = OpenBid.columns.str.replace(' ', '')
OpenBid = OpenBid.drop(columns=["Unnamed:0"])
## Opening demo data
Demo = pd.read_csv("Cleaned Files/demo_clean.csv")
Demo.columns = Demo.columns.str.replace(' ', '')
Demo = Demo.drop(columns=["Unnamed:0"])

## Merging adopt and real property - IDing unique block lots; dropping merge and reseting index
combined = RealProperty.merge(AdoptALot, on='BLOCKLOT', how='outer', indicator=True)
print("\nMerge counts for real property and adopt a lot:\n\n", combined["_merge"].value_counts() )
combined = combined.set_index("_merge")
adopt_only_onreal = combined.loc["right_only"]
combined = combined.set_index("BLOCKLOT")
print("\nParcels in adopt_a_lot and not in Real Property:\n\n:", adopt_only_onreal[["BLOCKLOT", "ADOPT:Address"]])

## Merging vacants onto combined  - IDing unique block lots; dropping merge and reseting index
combined2 = combined.merge(Vacants, on="BLOCKLOT", how="outer", indicator=True)
print("\nMerge counts for combined and vacants:\n\n", combined2["_merge"].value_counts() )
combined2 = combined2.set_index("_merge")
vacants_only_oncombined = combined2.loc["right_only"]
combined2 = combined2.set_index("BLOCKLOT")
print("\nParcels in vacants and not in combined:\n\n:", vacants_only_oncombined[["BLOCKLOT", "VAC:Neighborhood"]])

## Merging receivership onto combined2  - IDing unique block lots; dropping merge and reseting index
combined3 = combined2.merge(Receivership, on='BLOCKLOT', how='outer', indicator=True)
print("\nMerge counts for combined2 and receiver:\n\n", combined3["_merge"].value_counts() )
combined3 = combined3.set_index("_merge")
recevier_only_combined2 = combined3.loc["right_only"]
combined3 = combined3.set_index("BLOCKLOT")
print("\nParcels in receivership and not in combined2:\n\n:", recevier_only_combined2[["BLOCKLOT", "REC:Address"]])

## Merging open bid onto combined3  - IDing unique block lots; dropping merge and reseting index
combined4 = combined3.merge(OpenBid, on='BLOCKLOT', how='outer', indicator=True)
print("\nMerge counts for combined3 and open bid:\n\n", combined4["_merge"].value_counts() )
combined4 = combined4.set_index("_merge")
open_bid_only_combined3 = combined4.loc["right_only"]
combined4 = combined4.set_index("BLOCKLOT")
print("\nParcels in open bid and not in combined3:\n\n:", open_bid_only_combined3[["BLOCKLOT", "BID:Address"]])

## Merging demo onto combined4  - IDing unique block lots; dropping merge and reseting index
combined5 = combined4.merge(Demo, on='BLOCKLOT', how='outer', indicator=True)
print("\nMerge counts for combined4 and demo:\n\n", combined5["_merge"].value_counts() )
combined5 = combined5.set_index("_merge")
demo_only_combined4 = combined5.loc["right_only"]
combined5 = combined5.set_index("BLOCKLOT")
print("\nParcels in demo and not in combined4:\n\n:", demo_only_combined4[["BLOCKLOT", "BID:Address"]])

##Computing total length of compiled sheet
print("\nTotal records in combined sheet:\n", len(combined5))
combined5.columns = combined5.columns.str.replace(' ', '')

combined5.to_csv("Aggregated Files/compiled_parcels.csv")

print("\n-------------------\n")


