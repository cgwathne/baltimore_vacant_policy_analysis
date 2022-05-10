#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 10:02:52 2022

@author: camillewathne
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%% DESCRIBING REAL PROPERTY

real_property_analysis = pd.read_csv("Cleaned Files/real_property_clean.csv")

##How many vacants in real_property dataset
print("\nNumber of identified vacants in real_property (1=vacant):\n\n", real_property_analysis["REAL:Vacant"].value_counts())

#Describing ownership in real_property dataset
real_owners = real_property_analysis.groupby("REAL:Owner")
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
fig1.savefig("Initial Analysis_Chart Outputs/real_top10owners.png")


#%% DESCRIBING ADOPT A LOT

adopt_a_lot_analysis = pd.read_csv("Cleaned Files/adopt_a_lot_clean.csv")

## Overview
print("\nBreakdown of Adopt-a-Lot property types:\n\n", adopt_a_lot_analysis["ADOPT:Type"].value_counts())
print("\nBreakdown of Responsible Agencies:\n\n", adopt_a_lot_analysis["ADOPT:RespAgency"].value_counts())
print("\nBreakdown of Housing Typologies:\n\n", adopt_a_lot_analysis["ADOPT:Typology"].value_counts())

## Graph of housing neighborhoods for adoptable lots
adopt_by_neighborhood = adopt_a_lot_analysis.groupby("ADOPT:Neighborhood")
adopt_neighborhood_summary = pd.DataFrame()
adopt_neighborhood_summary["neighborhood"] = adopt_by_neighborhood.size()
adopt_top_neighborhood = adopt_neighborhood_summary["neighborhood"].sort_values()[-10:]

fig1, ax1 = plt.subplots()
adopt_top_neighborhood.plot.barh(ax=ax1, color=("#21A6D7"))
ax1.set_xlabel("Neighborhood")
ax1.set_title("Top 10 neighborhoods for adopt-a-lot properties")
fig1.savefig("Initial Analysis_Chart Outputs/adopt_neighborhoods.png")

#%% DESCRIBING VACANTS

vacants_analysis = pd.read_csv("Cleaned Files/vacants_clean.csv")

print("\nBreakdown of Vacant property types:\n\n", vacants_analysis["VAC:Typology"].value_counts())

## Graph of housing typology types for vacant lots
vacants_by_type = vacants_analysis.groupby("VAC:Typology")
vacants_type_summary = pd.DataFrame()
vacants_type_summary["Type"] = vacants_by_type.size()
vacants_type_summary = vacants_type_summary.sort_values("Type")

fig1, ax1 = plt.subplots()
vacants_type_summary.plot.barh(ax=ax1, color=("#619B1E"))
ax1.set_xlabel('Type')
ax1.set_title('Top 10 Neighborhoods for Vacants')
fig1.savefig("Initial Analysis_Chart Outputs/vacants_bytypology.png")

## Graph of housing neighborhoods for vacant lots
vacants_by_neighborhood = vacants_analysis.groupby("VAC:Neighborhood")
vacants_neighborhood_summary = pd.DataFrame()
vacants_neighborhood_summary["NEIGHBOR"] = vacants_by_neighborhood.size()
vacants_top_neighborhood = vacants_neighborhood_summary["NEIGHBOR"].sort_values()[-10:]

fig1, ax1 = plt.subplots()
vacants_top_neighborhood.plot.barh(ax=ax1, color=("#3D7002"))
ax1.set_xlabel("Neighborhood")
ax1.set_title('Prevalance of Neighborhood for Vacants')
fig1.savefig("Initial Analysis_Chart Outputs/vacants_byneighborhood")

#%% DESCRIBING RECEIVERSHIP

receivership_analysis = pd.read_csv("Cleaned Files/receiver_clean.csv")

## Graph of housing neighborhoods for receivership activities
receivership_by_neighborhood = receivership_analysis.groupby("REC:Neighborhood")
receivership_neighborhood_summary = pd.DataFrame()
receivership_neighborhood_summary["Neighborhood"] = receivership_by_neighborhood.size()
receivership_top_neighborhood = receivership_neighborhood_summary["Neighborhood"].sort_values()[-10:]
print("\nTop neighborhoods with receivership activities:\n\n", receivership_top_neighborhood)

fig1, ax1 = plt.subplots()
receivership_top_neighborhood.plot.barh(ax=ax1, color=("#900606"))
ax1.set_xlabel("Neighborhood")
ax1.set_title('Top 10 Neighborhoods for Receivership')
fig1.savefig('Initial Analysis_Chart Outputs/receivership_byneighborhood.png')

#%% DESCRIBING OPEN BID

open_bid_analysis = pd.read_csv("Cleaned Files/open_bid_clean.csv")
print("\nBreakdown of Open Bid property types:\n\n", open_bid_analysis["BID:Typology"].value_counts())

## Graph of housing typology types for open bid properties
open_bid_by_type = open_bid_analysis.groupby("BID:Typology")
open_bid_type_summary = pd.DataFrame()
open_bid_type_summary["HousingTypology"] = open_bid_by_type.size()
open_bid_type_summary = open_bid_type_summary.sort_values("HousingTypology")

fig1, ax1 = plt.subplots()
open_bid_type_summary.plot.barh(ax=ax1, color=("#B69527"))
ax1.set_xlabel('HousingTypology')
ax1.set_title('Prevalance of Housing Typology for Open Bid')
fig1.tight_layout()
fig1.savefig('Initial Analysis_Chart Outputs/openbid_bytypology.png')

## Graph of housing neighborhoods for open bid
open_bid_by_neighborhood = open_bid_analysis.groupby("BID:Neighborhood")
open_bid_neighborhood_summary = pd.DataFrame()
open_bid_neighborhood_summary["NEIGHBOR"] = open_bid_by_neighborhood.size()
open_bid_top_neighborhood = open_bid_neighborhood_summary["NEIGHBOR"].sort_values()[-10:]
print("\nTop neighborhoods with open bid parcels:\n\n", open_bid_top_neighborhood)

fig1, ax1 = plt.subplots()
open_bid_top_neighborhood.plot.barh(ax=ax1, color=("#866A0D"))
ax1.set_xlabel("Neighborhood")
ax1.set_title('Top 10 Neighborhoods for Open Bid')
fig1.tight_layout()
fig1.savefig('Initial Analysis_Chart Outputs/openbid_byneighborhood.png')

#%% DESCRIBING DEMOLITION

demo_analysis = pd.read_csv("Cleaned Files/demo_clean.csv")

## Graph of neighborhoods for demo
demo_by_neighborhood = demo_analysis.groupby("DEMO:Neighborhood")
demo_neighborhood_summary = pd.DataFrame()
demo_neighborhood_summary["Neighborhood"] = demo_by_neighborhood.size()
demo_top_neighborhood = demo_neighborhood_summary["Neighborhood"].sort_values()[-10:]
print("\nTop neighborhoods with demo parcels:\n\n", demo_top_neighborhood)

fig1, ax1 = plt.subplots()
demo_top_neighborhood.plot.barh(ax=ax1, color=("#93BD1D"))
ax1.set_xlabel("Neighborhood")
ax1.set_title('Top 10 Neighborhoods for Demos')
fig1.tight_layout()
fig1.savefig('Initial Analysis_Chart Outputs/demo_byneighborhood.png')

