#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 11:00:12 2022

@author: camillewathne
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import zipfile

#%% Real Property Info - TO DO: change to zip file. check determination of 
## missing data (60). Counting in a series
## optional - how to sum totals of "top 10" count? to see what remains (76)

print("\nREAL PROPERTY INFO\n")

## Open file
real_property = pd.read_csv("real_property.csv", dtype=str)

## Checking for duplicates in real property records
real_dup = real_property.duplicated( subset="BLOCKLOT", keep=False)
print('Duplicated BLOCKLOT labels:', real_dup.sum() ) 
print("which represents", round(real_dup.sum()*100/len(real_property), 2), "% of city properties")

## Describing duplicates in real_property
real_dup_rec = real_property[real_dup]
        ## Duplicates - looking at addresses
real_dup_byaddress = real_dup_rec.groupby("FULLADDR")
print("Belonging to a total of", len(real_dup_byaddress), "individual properties by address")
real_dup = real_property.duplicated( subset="BLOCKLOT", keep=False )
        ## Duplicates - looking at Pin Numbers
real_dup_bypin = real_dup_rec.groupby("PIN")
print("And a total of", len(real_dup_bypin), "individual properties by pin")
real_dup = real_property.duplicated( subset="PIN", keep=False )

## Dropping duplicates from real_property
real_property = real_property.drop_duplicates(subset="BLOCKLOT")
real_dup2 = real_property.duplicated( subset="BLOCKLOT", keep=False)
print('\nAfter dropping, New # of duplicated BLOCKLOT labels in real_property:', real_dup2.sum() ) 

## Keep 6 columns, remove spaces in block lot
real_property = real_property[["BLOCKLOT", "NEIGHBOR", "TAXBASE", "FULLADDR", "SALEPRIC", "VACIND", "OWNER_1"]]
real_property["BLOCKLOT"] = real_property["BLOCKLOT"].str.replace(' ', '')
print("\nThe number of unique parcel records for entire city is:", len(real_property))

## Renaming and classifying column headings
real_property = real_property.rename(columns={"TAXBASE":"REAL:TaxBase", "FULLADDR":"REAL:FullAdd", 
                                              "SALEPRIC":"REAL:SalePrice","VACIND":"REAL:Vacant", 
                                              "OWNER_1":"REAL:Owner", "NEIGHBOR": "REAL:Neighborhood"})
real_property = real_property[["BLOCKLOT", "REAL:FullAdd", "REAL:Neighborhood", "REAL:TaxBase", 
                               "REAL:SalePrice", "REAL:Vacant", "REAL:Owner"]]

## Convert missing data to null strings, changing notation on real vacants
real_property["REAL:Vacant"] = real_property["REAL:Vacant"].replace(r'^\s*$', np.NaN, regex=True)
real_property["REAL:Vacant"] = real_property["REAL:Vacant"].replace(r'Y', 1)
real_property["REAL:Vacant"] = real_property["REAL:Vacant"].replace(r'N', 0)
real_property["REAL:FullAdd"] = real_property["REAL:FullAdd"].replace(r'^\s*$', np.NaN, regex=True)

## Determining missing data
print("\nNumber of missing values in each column of Real Property Data out of", len(real_property), 
     "total entries:\n", real_property.isna().sum()) 

##How many vacants in real_property dataset
print("\nNumber of identified vacants in real_property:\n\n", real_property["REAL:Vacant"].value_counts())

#Describing ownership in real_property dataset
real_owners = real_property.groupby("REAL:Owner")
real_owner_summary = pd.DataFrame()
real_owner_summary["Owner"] = real_owners.size()
real_top25_owners = real_owner_summary["Owner"].sort_values()[-25:]
real_top10_owners = real_owner_summary["Owner"].sort_values()[-10:]
print("\nTop 25 owners and parcel amounts from real_property data:\n\n", real_top25_owners)

## Graphing top owners
fig1, ax1 = plt.subplots()
real_top10_owners.plot.barh(ax=ax1, color=("#84169A"))
ax1.set_xlabel("# of parcels owned")
ax1.set_title('Number of lots by top 10 owners')
fig1.savefig('real_top10owners.png')

##Saving cleaned data to csv file
real_property.to_csv("real_property_clean.csv")

print("\n-------------------\n")

#%% Adopt A Lot - TO DO: how to justify labels on bar graphs? change color?

print("ADOPT-A-LOT INFO\n")

## Open Adopt-A-Lot
adopt_a_lot = pd.read_csv("adopt_a_lot.csv", dtype=str)

##Dropping columns with very limited info/are irrelevant
adopt_a_lot = adopt_a_lot.drop(columns=["Licensee", "Shape", "QCMOS", "AssetMgmtProject", 
              "ID_AcqGreenSpaceWeb", "ContactName", "ExpDate", "ValidDate", "x", "y", 
              "Council_District", "NotAdoptable"])

## Determining extent of missing data after removing columns
print("After dropping columns, number of missing values in each column of adopt-a-lot out of", len(adopt_a_lot), 
      "total entries:\n", adopt_a_lot.isnull().sum())

## Removing spaces in block lot and column names, renaming BlockLot to BLOCKLOT
adopt_a_lot["BlockLot"] = adopt_a_lot["BlockLot"].str.replace(' ', '')
adopt_a_lot.columns = adopt_a_lot.columns.str.replace(' ', '')
adopt_a_lot = adopt_a_lot.rename(columns={"BlockLot":"BLOCKLOT"})

## Identifying duplicated parcels and dropping duplicates
adopt_dup = adopt_a_lot.duplicated( subset="BLOCKLOT", keep=False )
adopt_a_lot = adopt_a_lot.drop_duplicates(subset="BLOCKLOT")
adopt_dup2 = adopt_a_lot.duplicated( subset="BLOCKLOT", keep=False)
print('\nDuplicated parcels in Adopt-a-Lot:', adopt_dup.sum() ) 
print('\nAfter dropping, New # of duplicated BLOCKLOT labels in adopt_a_lot:', adopt_dup2.sum() ) 

## Describing data
print("\nTotal records in Adopt-a-Lot:", len(adopt_a_lot))
print("\nBreakdown of Adopt-a-Lot property types:\n\n", adopt_a_lot["Type"].value_counts())
print("\nBreakdown of Responsible Agencies:\n\n", adopt_a_lot["ResponsibleAgency"].value_counts())
print("\nBreakdown of Housing Typologies:\n\n", adopt_a_lot["HousingTypology2017"].value_counts())

## Graph of housing neighborhoods for adoptable lots
adopt_by_neighborhood = adopt_a_lot.groupby("Neighborhood")
adopt_neighborhood_summary = pd.DataFrame()
adopt_neighborhood_summary["neighborhood"] = adopt_by_neighborhood.size()
adopt_top_neighborhood = adopt_neighborhood_summary["neighborhood"].sort_values()[-10:]

fig1, ax1 = plt.subplots()
adopt_top_neighborhood.plot.barh(ax=ax1, color=("#21A6D7"))
ax1.set_xlabel("Neighborhood")
ax1.set_title("Top 10 neighborhoods for adopt-a-lot properties")
fig1.savefig('adopt_neighborhoods.png')

## Preparing for merge
adopt_a_lot["ADOPT:PROG"] = 1
adopt_a_lot = adopt_a_lot.rename(columns={"ResponsibleAgency":"ADOPT:RespAgency", "Type":"ADOPT:Type", 
                                          "Address":"ADOPT:Address", "Neighborhood":"ADOPT:Neighborhood",
                                          "HousingTypology2017":"ADOPT:Typology"})
adopt_a_lot = adopt_a_lot[["BLOCKLOT", "ADOPT:PROG", "ADOPT:Address", "ADOPT:Neighborhood",
                           "ADOPT:Typology", "ADOPT:RespAgency", "ADOPT:Type"]]

##Saving cleaned data to csv file
adopt_a_lot.to_csv("adopt_a_lot_clean.csv")

print("\n-------------------\n")

#%% Vacants

print("VACANTS INFO\n")

## Open Vacants
vacants = pd.read_csv("vacants.csv", dtype=str)

##Dropping columns with very limited info/are irrelevant
vacants = vacants.drop(columns=["NoticeNum", "Shape", "Council_District", 
              "OBJECTID", "ESRI_OID", "x", "y"])

## Determining extent of missing data
print("Number of missing values in each column of vacants out of", len(vacants), 
      "total entries:\n", vacants.isnull().sum())

## Removing spaces in block lot and column names
vacants["BLOCKLOT"] = vacants["BLOCKLOT"].str.replace(' ', '')
vacants.columns = vacants.columns.str.replace(' ', '')

## Identifying duplicated parcels and dropping duplicates
vacants_dup = vacants.duplicated( subset="BLOCKLOT", keep=False )
vacants = vacants.drop_duplicates(subset="BLOCKLOT")
vacants_dup2 = vacants.duplicated(subset="BLOCKLOT", keep=False)
print('\nDuplicated parcels in Vacants:', vacants_dup.sum() ) 
print('\nAfter dropping, New # of duplicated BLOCKLOT labels in Vacants:', vacants_dup2.sum() ) 

## Describing initial data
print("\nTotal records in Vacants:", len(vacants))
print("\nBreakdown of Vacant property types:\n\n", vacants["Typology2017"].value_counts())

## Graph of housing typology types for vacant lots
vacants_by_type = vacants.groupby("Typology2017")
vacants_type_summary = pd.DataFrame()
vacants_type_summary["Type"] = vacants_by_type.size()
vacants_type_summary = vacants_type_summary.sort_values("Type")

fig1, ax1 = plt.subplots()
vacants_type_summary.plot.barh(ax=ax1, color=("#619B1E"))
ax1.set_xlabel('Type')
ax1.set_title('Prevalance of Housing Typology for Vacants')
fig1.savefig("vacants_bytypology.png")

## Graph of housing neighborhoods for vacant lots
vacants_by_neighborhood = vacants.groupby("NEIGHBOR")
vacants_neighborhood_summary = pd.DataFrame()
vacants_neighborhood_summary["NEIGHBOR"] = vacants_by_neighborhood.size()
vacants_top_neighborhood = vacants_neighborhood_summary["NEIGHBOR"].sort_values()[-10:]

fig1, ax1 = plt.subplots()
vacants_top_neighborhood.plot.barh(ax=ax1, color=("#3D7002"))
ax1.set_xlabel("Neighborhood")
ax1.set_title('Prevalance of Neighborhood for Vacants')
fig1.savefig("vacants_byneighborhood")

## Preparing for merge
vacants["VAC:PROG"] = 1
vacants = vacants.rename(columns={"NEIGHBOR":"VAC:Neighborhood", "DateNotice":"VAC:DateNotice",
                                  "Typology2017":"VAC:Typology"})
vacants = vacants[["BLOCKLOT", "VAC:PROG", "VAC:Neighborhood", "VAC:Typology"]]

##Saving cleaned data to csv file
vacants.to_csv("vacants_clean.csv")

print("\n-------------------\n")

#%% Receivership TO DO: check dates?

print("RECEIVERSHIP INFO\n")

## Open Receivership
receiver = pd.read_csv("receiverships.csv", dtype=str)

## Removing spaces in block lot and column names
receiver.columns = receiver.columns.str.replace(' ', '')

##Dropping columns with very limited info/are irrelevant
receiver = receiver.drop(columns=["Lawyer", "ProjectName", "ReceiverAppointed", 
              "AuctionDate", "x", "y"])

## Determining extent of missing data
print("Number of missing values in each column of receiver out of", len(receiver), 
      "total entries:\n", receiver.isnull().sum())

## Combining address fields (and replace nan with empty string) - troubleshoot this
receiver = receiver.replace(np.nan, "")
receiver["HouseNum"] = receiver["HouseNum"].str.replace(r"\D", "", regex=True)
receiver["Dir"] = receiver["Dir"].str.strip()
receiver["StreetName"] = receiver["StreetName"].str.strip()
receiver["StreetType"] = receiver["StreetType"].str.strip()
receiver["FullAddress"] = receiver["HouseNum"] + " " + receiver["Dir"] + " " + receiver["StreetName"]  + " " + receiver["StreetType"]
receiver["FullAddress"] = receiver["FullAddress"].str.replace(r"\s+", " ", regex=True)
receiver = receiver.drop(columns=["StreetName", "HouseNum", "Dir", "StreetType", "Zip"])

## Identifying duplicated parcels and dropping duplicates
receiver_dup = receiver.duplicated( subset="BlockLot", keep=False )
receiver = receiver.drop_duplicates(subset="BlockLot")
receiver_dup2 = receiver.duplicated(subset="BlockLot", keep=False)
print('\nDuplicated parcels in Receiver:', receiver_dup.sum() ) 
print('\nAfter dropping, New # of duplicated BLOCKLOT labels in Receiver:', receiver_dup2.sum() ) 

## Describing data
print("\nTotal records in Receiver:", len(receiver))

## Graph of housing neighborhoods for receivership activities
receiver_by_neighborhood = receiver.groupby("Neighborhood")
receiver_neighborhood_summary = pd.DataFrame()
receiver_neighborhood_summary["Neighborhood"] = receiver_by_neighborhood.size()
receiver_top_neighborhood = receiver_neighborhood_summary["Neighborhood"].sort_values()[-10:]

fig1, ax1 = plt.subplots()
receiver_top_neighborhood.plot.barh(ax=ax1, color=("#900606"))
ax1.set_xlabel("Neighborhood")
ax1.set_title('Prevalance of Neighborhood for Receivership')
fig1.savefig('receivership_byneighborhood.png')

## Preparing for merge
receiver["REC:PROG"] = 1
receiver = receiver.rename(columns={"BlockLot": "BLOCKLOT", "Neighborhood":"REC:Neighborhood", 
                                    "FullAddress":"REC:Address"})
receiver = receiver[["BLOCKLOT", "REC:PROG", "REC:Neighborhood", "REC:Address"]]

##Saving cleaned data to csv file
receiver.to_csv("receiver_clean.csv")

print("\n-------------------\n")

#%% Open Bid

## Open open bid
print("OPEN BID INFO\n")

open_bid = pd.read_csv("open_bid.csv", dtype=str)

##Dropping columns with very limited info/are irrelevant
open_bid = open_bid.drop(columns=["ID_AcqFirefly", "OBJECTID", "Status", 
              "Council_District", "Shape", "x", "y"])

## Determining extent of missing data
print("\nNumber of missing values in each column of open bid out of", len(open_bid), 
      "total entries:\n", open_bid.isnull().sum())

## Removing spaces in block lot 
open_bid["BLOCKLOT"] = open_bid["BLOCKLOT"].str.replace(' ', '')

## Identifying duplicated parcels and dropping duplicates
open_bid_dup = open_bid.duplicated( subset="BLOCKLOT", keep=False )
open_bid = open_bid.drop_duplicates(subset="BLOCKLOT")
open_bid_dup2 = open_bid.duplicated(subset="BLOCKLOT", keep=False)
print('\nDuplicated parcels in Open Bid:', open_bid_dup.sum() ) 
print('\nAfter dropping, New # of duplicated BLOCKLOT labels in Open Bid:', open_bid_dup2.sum() ) 

## Describing initial data
print("\nTotal records in Open Bid:", len(open_bid))
print("\nBreakdown of Open Bid property types:\n\n", open_bid["HousingMarketTypology2017"].value_counts())

## Graph of housing typology types for open bid properties
open_bid_by_type = open_bid.groupby("HousingMarketTypology2017")
open_bid_type_summary = pd.DataFrame()
open_bid_type_summary["HousingTypology"] = open_bid_by_type.size()
open_bid_type_summary = open_bid_type_summary.sort_values("HousingTypology")

fig1, ax1 = plt.subplots()
open_bid_type_summary.plot.barh(ax=ax1, color=("#B69527"))
ax1.set_xlabel('HousingTypology')
ax1.set_title('Prevalance of Housing Typology for Open Bid')
fig1.tight_layout()
fig1.savefig('openbid_bytypology.png')

## Graph of housing neighborhoods for open bid
open_bid_by_neighborhood = open_bid.groupby("Neighborhood")
open_bid_neighborhood_summary = pd.DataFrame()
open_bid_neighborhood_summary["NEIGHBOR"] = open_bid_by_neighborhood.size()
open_bid_top_neighborhood = open_bid_neighborhood_summary["NEIGHBOR"].sort_values()[-10:]

fig1, ax1 = plt.subplots()
open_bid_top_neighborhood.plot.barh(ax=ax1, color=("#866A0D"))
ax1.set_xlabel("Neighborhood")
ax1.set_title('Prevalance of Neighborhood for Open Bid')
fig1.tight_layout()
fig1.savefig('openbid_byneighborhood.png')

## Preparing for merge
open_bid["BID:PROG"] = 1
open_bid = open_bid.rename(columns={"Address":"BID:Address", "Neighborhood":"BID:Neighborhood",
                                  "HousingMarketTypology2017":"BID:Typology"})
open_bid = open_bid[["BLOCKLOT", "BID:PROG", "BID:Neighborhood", "BID:Typology", "BID:Address"]]

##Saving cleaned data to csv file
open_bid.to_csv("open_bid_clean.csv")

print("\n-------------------\n")






