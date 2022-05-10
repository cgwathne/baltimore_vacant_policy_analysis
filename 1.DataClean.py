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

#%% CLEANING AND PREPARING REAL PROPERTY FILE 

print("\nREAL PROPERTY INFO\n")
real_property = pd.read_csv("Source Files/real_property.csv", dtype=str)

## Checking for and  describing nature of duplicates in "real property" records
real_dup = real_property.duplicated( subset="BLOCKLOT", keep=False)
print('Duplicated BLOCKLOT labels:', real_dup.sum() ) 
print("which represents", round(real_dup.sum()*100/len(real_property), 2), "% of city properties")
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

## Organizing columns and cleaning spaces in data set 
real_property = real_property[["BLOCKLOT", "NEIGHBOR", "TAXBASE", "FULLADDR", "SALEPRIC", "VACIND", "OWNER_1"]]
real_property["BLOCKLOT"] = real_property["BLOCKLOT"].str.replace(' ', '')
print("\nThe number of unique parcel records for entire city is:", len(real_property))
real_property = real_property.rename(columns={"TAXBASE":"REAL:TaxBase", "FULLADDR":"REAL:FullAdd", 
                                              "SALEPRIC":"REAL:SalePrice","VACIND":"REAL:Vacant", 
                                              "OWNER_1":"REAL:Owner", "NEIGHBOR": "REAL:Neighborhood"})
real_property = real_property[["BLOCKLOT", "REAL:FullAdd", "REAL:Neighborhood", "REAL:TaxBase", 
                               "REAL:SalePrice", "REAL:Vacant", "REAL:Owner"]]
real_property["REAL:Vacant"] = real_property["REAL:Vacant"].replace(r'^\s*$', np.NaN, regex=True)
real_property["REAL:Vacant"] = real_property["REAL:Vacant"].replace(r'Y', 1)
real_property["REAL:Vacant"] = real_property["REAL:Vacant"].replace(r'N', 0)
real_property["REAL:FullAdd"] = real_property["REAL:FullAdd"].replace(r'^\s*$', np.NaN, regex=True)
real_property["REAL:Owner"] = real_property["REAL:Owner"].str.strip()

## Determining missing data
print("\nNumber of missing values in each column of Real Property Data out of", len(real_property), 
     "total entries:\n", real_property.isna().sum()) 

##Saving cleaned data to csv file
real_property.to_csv("Cleaned Files/real_property_clean.csv")
print("\n-------------------\n")

#%% CLEANING AND PREPARING ADOPT A LOT FILE

print("\nADOPT-A-LOT INFO\n")
adopt_a_lot = pd.read_csv("Source Files/adopt_a_lot.csv", dtype=str)

## Dropping unecesary columns, removing spaces and duplicates, renaming columns
adopt_a_lot = adopt_a_lot.drop(columns=["Licensee", "Shape", "QCMOS", "AssetMgmtProject", 
              "ID_AcqGreenSpaceWeb", "ContactName", "ExpDate", "ValidDate", "x", "y", 
              "Council_District", "NotAdoptable"])
print("After dropping columns, number of missing values in each column of adopt-a-lot out of", len(adopt_a_lot), 
      "total entries:\n", adopt_a_lot.isnull().sum())
adopt_a_lot["BlockLot"] = adopt_a_lot["BlockLot"].str.replace(' ', '')
adopt_a_lot.columns = adopt_a_lot.columns.str.replace(' ', '')
adopt_a_lot = adopt_a_lot.rename(columns={"BlockLot":"BLOCKLOT"})
adopt_a_lot["Neighborhood"] = adopt_a_lot["Neighborhood"].str.strip()

## Identifying duplicated parcels and dropping duplicates
adopt_dup = adopt_a_lot.duplicated( subset="BLOCKLOT", keep=False )
adopt_a_lot = adopt_a_lot.drop_duplicates(subset="BLOCKLOT")
adopt_dup2 = adopt_a_lot.duplicated( subset="BLOCKLOT", keep=False)
print('\nDuplicated parcels in Adopt-a-Lot:', adopt_dup.sum() ) 
print('\nAfter dropping, New # of duplicated BLOCKLOT labels in adopt_a_lot:', adopt_dup2.sum() ) 
print("\nTotal records in Adopt-a-Lot:", len(adopt_a_lot))

## Preparing for merge
adopt_a_lot["ADOPT:PROG"] = 1
adopt_a_lot = adopt_a_lot.rename(columns={"ResponsibleAgency":"ADOPT:RespAgency", "Type":"ADOPT:Type", 
                                          "Address":"ADOPT:Address", "Neighborhood":"ADOPT:Neighborhood",
                                          "HousingTypology2017":"ADOPT:Typology"})
adopt_a_lot = adopt_a_lot[["BLOCKLOT", "ADOPT:PROG", "ADOPT:Address", "ADOPT:Neighborhood",
                           "ADOPT:Typology", "ADOPT:RespAgency", "ADOPT:Type"]]

##Saving cleaned data to csv file
adopt_a_lot.to_csv("Cleaned Files/adopt_a_lot_clean.csv")
print("\n-------------------\n")

#%% CLEANING AND PREPARING VACANTS FILE

print("\nVACANTS INFO\n")
vacants = pd.read_csv("Source Files/vacants.csv", dtype=str)

## Dropping unecesary columns, removing spaces and duplicates, renaming columns
vacants = vacants.drop(columns=["NoticeNum", "Shape", "Council_District", 
              "OBJECTID", "ESRI_OID", "x", "y"])
print("Number of missing values in each column of vacants out of", len(vacants), 
      "total entries:\n", vacants.isnull().sum())
vacants["BLOCKLOT"] = vacants["BLOCKLOT"].str.replace(' ', '')
vacants.columns = vacants.columns.str.replace(' ', '')
vacants["NEIGHBOR"] = vacants["NEIGHBOR"].str.strip()

## Identifying duplicated parcels and dropping duplicates
vacants_dup = vacants.duplicated( subset="BLOCKLOT", keep=False )
vacants = vacants.drop_duplicates(subset="BLOCKLOT")
vacants_dup2 = vacants.duplicated(subset="BLOCKLOT", keep=False)
print('\nDuplicated parcels in Vacants:', vacants_dup.sum() ) 
print('\nAfter dropping, New # of duplicated BLOCKLOT labels in Vacants:', vacants_dup2.sum() ) 
print("\nTotal records in Vacants:", len(vacants))

## Preparing for merge
vacants["VAC:PROG"] = 1
vacants = vacants.rename(columns={"NEIGHBOR":"VAC:Neighborhood", "DateNotice":"VAC:DateNotice",
                                  "Typology2017":"VAC:Typology"})
vacants = vacants[["BLOCKLOT", "VAC:PROG", "VAC:Neighborhood", "VAC:Typology"]]

##Saving cleaned data to csv file
vacants.to_csv("Cleaned Files/vacants_clean.csv")
print("\n-------------------\n")

#%% CLEANING AND PREPARING RECEIVERSHIP FILE (2 DATA SOURCES)

print("RECEIVERSHIP INFO\n")
receiver = pd.read_csv("Source Files/receiverships.csv", dtype=str)

## Dropping unecesary columns, removing spaces and duplicates, renaming columns
receiver.columns = receiver.columns.str.replace(' ', '')
receiver = receiver.drop(columns=["Lawyer", "ProjectName", "ReceiverAppointed", 
              "AuctionDate", "x", "y"])
print("Number of missing values in each column of receiver out of", len(receiver), 
      "total entries:\n", receiver.isnull().sum())

## Combining address fields
receiver = receiver.replace(np.nan, "")
receiver["HouseNum"] = receiver["HouseNum"].str.replace(r"\D", "", regex=True)
receiver["Dir"] = receiver["Dir"].str.strip()
receiver["StreetName"] = receiver["StreetName"].str.strip()
receiver["StreetType"] = receiver["StreetType"].str.strip()
receiver["FullAddress"] = receiver["HouseNum"] + " " + receiver["Dir"] + " " + receiver["StreetName"]  + " " + receiver["StreetType"]
receiver["FullAddress"] = receiver["FullAddress"].str.replace(r"\s+", " ", regex=True)
receiver = receiver.drop(columns=["StreetName", "HouseNum", "Dir", "StreetType", "Zip"])

##Stripping blank spaces in key columns
receiver["Neighborhood"] = receiver["Neighborhood"].str.replace(r"\s+", " ", regex=True)
receiver["FullAddress"] = receiver["FullAddress"].str.replace(r"\s+", " ", regex=True)
receiver["BlockLot"] = receiver["BlockLot"].str.replace(r"\s+", " ", regex=True)
receiver["Neighborhood"] = receiver["Neighborhood"].str.strip()
receiver["FullAddress"] = receiver["FullAddress"].str.strip()
receiver["BlockLot"] = receiver["BlockLot"].str.strip()

## Identifying duplicated parcels and dropping duplicates
receiver_dup = receiver.duplicated( subset="BlockLot", keep=False )
receiver = receiver.drop_duplicates(subset="BlockLot")
receiver_dup2 = receiver.duplicated(subset="BlockLot", keep=False)
print('\nDuplicated parcels in Receiver:', receiver_dup.sum() ) 
print('\nAfter dropping, New # of duplicated BLOCKLOT labels in Receiver:', receiver_dup2.sum() ) 

print("\nTotal records in Receiver:", len(receiver))

## FOLDING IN ADDITIONAL RECEIVERSHIP INFO FROM CITY

receiverEx = pd.read_csv("Source Files/receivership_expand.csv", dtype=str)

## Cleaning headings and removing unecessary columns

receiverEx.columns = receiverEx.columns.str.replace(' ', '')
receiverEx = receiverEx.drop(columns=["X", "Y", "OBJECTID", "OBJECTID_1", "ID_RS_Web", "Council_District"])

## Identifying duplicated parcels and dropping duplicates
receiverEx_dup = receiverEx.duplicated( subset="BLOCKLOT", keep=False )
receiverEx = receiverEx.drop_duplicates(subset="BLOCKLOT")
receiverEx_dup2 = receiverEx.duplicated(subset="BLOCKLOT", keep=False)
print('\nDuplicated parcels in Receiver Expanded (2nd file):', receiverEx_dup.sum() ) 
print('\nAfter dropping, New # of duplicated BLOCKLOT labels in Receiver Expanded:', receiverEx_dup2.sum() ) 

print("\nTotal records in Receiver Expanded:", len(receiverEx))

## Removing records more than a decade old
receiverEx = receiverEx[~receiverEx.DateFiled.str.contains("2001|2005|2006|2007|2008|2009|2010|2011",
                                                           regex=True)]

## Dropping unecessary columns, stripping, renaming, and preparing for merge
receiverEx = receiverEx.drop(columns=["DateFiled", "ReceiverAppointed", "DateAuction",
                                      "SoldAtAuction", "HousingMarketTypology2017"])
columnlist = ["Address", "Neighborhood", "BLOCKLOT"]
receiverEx["Address"] = receiverEx["Address"].str.replace(r"\s+", " ", regex=True)
receiverEx["Neighborhood"] = receiverEx["Neighborhood"].str.replace(r"\s+", " ", regex=True)
receiverEx["BLOCKLOT"] = receiverEx["BLOCKLOT"].str.replace(' ', '')
receiverEx["Address"] = receiverEx["Address"].str.strip()
receiverEx["Neighborhood"] = receiverEx["Neighborhood"].str.strip()
receiverEx["BLOCKLOT"] = receiverEx["BLOCKLOT"].str.strip()
receiverEx = receiverEx.rename(columns={"Address":"FullAddress", "BLOCKLOT":"BlockLot"})

## Merging receiver with receiver expanded
receivership = receiver.merge(receiverEx, on=["BlockLot", "FullAddress", "Neighborhood"], how='outer', indicator=True)
print("\nMerge counts for receivership and receiver expanded:\n\n", receivership["_merge"].value_counts() )
print('\nTotal parcels in receivership over past 10 years is:', len(receivership))
## Preparing for merge
receivership["REC:PROG"] = 1
receivership = receivership.rename(columns={"BlockLot": "BLOCKLOT", "Neighborhood":"REC:Neighborhood", 
                                    "FullAddress":"REC:Address"})
receivership = receivership[["BLOCKLOT", "REC:PROG", "REC:Neighborhood", "REC:Address"]]

##Saving cleaned data to csv file
receivership.to_csv("Cleaned Files/receiver_clean.csv")
print("\n-------------------\n")

#%% CLEANING AND PREPARING OPEN BID FILE

print("\nOPEN BID INFO\n")
open_bid = pd.read_csv("Source Files/open_bid.csv", dtype=str)

##Dropping columns with very limited info, determining missing data, cleaning spaces
open_bid = open_bid.drop(columns=["ID_AcqFirefly", "OBJECTID", "Status", 
              "Council_District", "Shape", "x", "y"])
print("\nNumber of missing values in each column of open bid out of", len(open_bid), 
      "total entries:\n", open_bid.isnull().sum())
open_bid["BLOCKLOT"] = open_bid["BLOCKLOT"].str.replace(' ', '')
open_bid["Neighborhood"] = open_bid["Neighborhood"].str.strip()

## Identifying duplicated parcels and dropping duplicates
open_bid_dup = open_bid.duplicated( subset="BLOCKLOT", keep=False )
open_bid = open_bid.drop_duplicates(subset="BLOCKLOT")
open_bid_dup2 = open_bid.duplicated(subset="BLOCKLOT", keep=False)
print('\nDuplicated parcels in Open Bid:', open_bid_dup.sum() ) 
print('\nAfter dropping, New # of duplicated BLOCKLOT labels in Open Bid:', open_bid_dup2.sum() ) 

## Describing initial data
print("\nTotal records in Open Bid:", len(open_bid))

## Preparing for merge
open_bid["BID:PROG"] = 1
open_bid = open_bid.rename(columns={"Address":"BID:Address", "Neighborhood":"BID:Neighborhood",
                                  "HousingMarketTypology2017":"BID:Typology"})
open_bid = open_bid[["BLOCKLOT", "BID:PROG", "BID:Neighborhood", "BID:Typology", "BID:Address"]]

##Saving cleaned data to csv file
open_bid.to_csv("Cleaned Files/open_bid_clean.csv")
print("\n-------------------\n")


#%% CLEANING AND PREPARING DEMO FILE

print("\nDEMO INFO\n")
demo = pd.read_csv("Source Files/demo.csv", dtype=str)

## Dropping unecessary columns, determining missing data, stripping blank spaces
demo.columns = demo.columns.str.replace(' ', '')
demo = demo[["BLOCKLOT", "DateDemoFinished", "Address", "HousingMarketTypology2017", "Neighborhood"]]
print("Number of missing values in each column of demo out of", len(demo), 
      "total entries:\n", demo.isnull().sum())
demo["Neighborhood"] = demo["Neighborhood"].str.replace(r"\s+", " ", regex=True)
demo["Address"] = demo["Address"].str.replace(r"\s+", " ", regex=True)
demo["BLOCKLOT"] = demo["BLOCKLOT"].str.replace(r"\s+", " ", regex=True)
demo["Neighborhood"] = demo["Neighborhood"].str.strip()
demo["Address"] = demo["Address"].str.strip()
demo["BLOCKLOT"] = demo["BLOCKLOT"].str.strip()
demo["BLOCKLOT"] = demo["BLOCKLOT"].str.replace(' ', '')

## Identifying duplicated parcels and dropping duplicates
demo_dup = demo.duplicated( subset="BLOCKLOT", keep=False )
demo = demo.drop_duplicates(subset="BLOCKLOT")
demo_dup2 = demo.duplicated(subset="BLOCKLOT", keep=False)
print('\nDuplicated parcels in Demo:', demo_dup.sum() ) 
print('\nAfter dropping, New # of duplicated BLOCKLOT labels in Demo:', demo_dup2.sum() ) 
print("\nTotal parcels in demolition over past 10 years is:", len(demo))

## Preparing for merge
demo["DEMO:PROG"] = 1
demo = demo.rename(columns={"Address":"DEMO:Address", "Neighborhood":"DEMO:Neighborhood",
                                  "HousingMarketTypology2017":"DEMO:Typology"})
demo = demo[["BLOCKLOT", "DEMO:PROG", "DEMO:Neighborhood", "DEMO:Typology", "DEMO:Address"]]

##Saving cleaned data to csv file
demo.to_csv("Cleaned Files/demo_clean.csv")
print("\n-------------------\n")

