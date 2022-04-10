#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 15:45:30 2022

@author: camillewathne
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#%% Merging - how to do this between 4 files when checking merge?

## Opening real property data
RealProperty = pd.read_csv("real_property_clean.csv")
RealProperty.columns = RealProperty.columns.str.replace(' ', '')
RealProperty = RealProperty.drop(columns=["Unnamed:0"])

## Opening adopt a lot data
AdoptALot = pd.read_csv("adopt_a_lot_clean.csv")
AdoptALot.columns = AdoptALot.columns.str.replace(' ', '')
AdoptALot = AdoptALot.drop(columns=["Unnamed:0"])

## Opening vacants
Vacants = pd.read_csv("vacants_clean.csv")
Vacants.columns = Vacants.columns.str.replace(' ', '')
Vacants = Vacants.drop(columns=["Unnamed:0"])

## Opening receivership data
Receivership = pd.read_csv("receiver_clean.csv")
Receivership.columns = Receivership.columns.str.replace(' ', '')
Receivership = Receivership.drop(columns=["Unnamed:0"])

## Opening open bid data
OpenBid = pd.read_csv("open_bid_clean.csv")
OpenBid.columns = OpenBid.columns.str.replace(' ', '')
OpenBid = OpenBid.drop(columns=["Unnamed:0"])

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

##Computing total length of compiled sheet
print("\nTotal records in combined sheet:\n", len(combined4))
combined4.columns = combined4.columns.str.replace(' ', '')

combined4.to_csv("Compiled_Sheet.csv")



