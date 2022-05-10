# Analysis of Vacant Lots in Baltimore City
### Camille Wathne, March 2022
### Maxwell School at Syracuse University

____
## Motivation

As the population of Baltimore continues to decline, from a peak of approximately 1 million residents in 1950 to 600,000 today, the city is grappling with thousands of vacant buildings and empty parcels of land (hereafter referred to as “vacants”). Evidence shows that vacants have adverse impacts on health, neighborhood cohesion, and safety. Baltimore City has thus implemented a range of programs intended to mitigate the negative effects of vacants, encourage building stewardship, and promote economic vitality. 

**This project aims to:**
- characterize the neighborhoods that have a high portion of vacants and program activites
- analyze the intersection and overlap of four Baltimore City policies that address vacants
- visually depict these relationships through mapping software


**Adopt-A-Lot:** Enables citizens to adopt/steward designated empty plots of land for private use. 
**Open-Bid:** Enables citizens to purchase certain vacant parcels.  
**Receivership:** Encompasses a suite of targeted city activities intended to preserve and sustain “middle market neighborhoods.” Consists of targeted housing code enforcement; issuance of citations for negligence; seizure of properties; and legal transfer of deed to new receiving entity. 
**Demolition:** Includes city sponsored, targeted demolition of abandoned or neglected properties.
___
## Instructions

Python Files 
**1.DataClean.py:** Pulls in original, parcel-level data files from "Source Files" folder. See below for details on the origin and type of datasets. Cleans data, describes and characterises duplicates, produces program counts, codes binary value for each program participation, and prepares cleaned csv files which save to "Cleaned Files" folder and are used in subsequent scripts.  
**1b.InitialAnalysis.py:** Optional script that conducts intial program-specific analysis from cleaned csv files (eg housing typology, neighborhood prevalence, primary property owners). Output graphs are saved in folder titled "Initial Analysis_Chart Outputs."  
**2.AggregateData.py:** Aggregates cleaned, parcel-level csv files and merges on unique Block Lot identifer to create compiled sheet. Produces compiled_parcels csv file which saves to folder "Aggregated Files."  
**3.AggDataAnalysis.py:** Conducts analysis on combined parcel file; examines parcel overlap and program co-occurance. Produces neighborhood_parcel_agg file, organized by neighborhood, to prepare for merge with neighborhood-level data.  
**.NeighborhoodData.py:** Merges neighborhood-level census information, csv files titled "city_data_pdf" which includes manually coded median income data, and grouped program information from previous scripts. Produces final csv file, "neighborhood_full_data," which is saved in the main repository.  
**5.QGISprep.py:** Uses neighborhood_full_data.csv to produce neighborhood-level percentages in preparation for QGIS. Produces baltimore_shp.gpkg file, saved to "QGIS Files" folder. 

## Data Sets  
real_property.csv:
adopt_a_lot.csv:
receivership.csv:
receivership_expand:
vacants.csv:
open_bid.csv:
demo.csv:
neighborhoods.csv:

![alt_text_here](image.png)
