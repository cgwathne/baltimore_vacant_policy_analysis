clear
import delimited "C:\Users\cgwathne\OneDrive - Syracuse University\Advanced Policy Analysis\Github\baltimore_vacant_policy_analysis_dev\neighborhood_data.csv", varnames(1)
save "C:\Users\cgwathne\OneDrive - Syracuse University\Advanced Policy Analysis\Github\baltimore_vacant_policy_analysis_dev\neighborhood_dta", replace
*Cleaning data
*drop neighborhoods with less than 200 people
keep if population>200

*generate a variable for percent of parcels in any program
capture drop perc_anyprog
gen perc_anyprog=anyprog/totalparcels
summarize perc_anyprog, detail
*generage a binary variable for neighborhood with parcels in any program
capture drop binary_anyprog
gen binary_anyprog=1 if anyprog>0
replace binary_anyprog=0 if anyprog==0

*generate a variable for percent of city-owned parcels in any program
replace cityownedprogramsubset = 0 if(cityownedprogramsubset == .)
capture drop perc_cityanyprog
gen perc_cityanyprog=cityownedprogramsubset/totalparcels
summarize perc_cityanyprog, detail

***
*generate variables for percent of parcels in each program
*Vacants
capture drop perc_vac
gen perc_vac=vacprog/totalparcels
summarize perc_vac, detail
*Receivership
capture drop perc_rec
gen perc_rec=recprog/totalparcels
summarize perc_rec, detail
*Open Bid
capture drop perc_bid
gen perc_bid=bidprog/totalparcels
summarize perc_bid, detail
*Adopt-a-Lot
capture drop perc_adopt
gen perc_adopt=adoptprog/totalparcels
summarize perc_adopt, detail

*Creating demographic percentages
*Race
gen perc_white=white/population
gen perc_black=blk_afam/population
gen perc_hisp=hisp_lat/population

***
*generate a categorical variable based on the distribution of parcels but with rounded percentages ANY PROGRAM - better way to bin these?
capture drop categ_anyprog
summarize anyprog, detail
gen categ_anyprog=0 if perc_anyprog==0
replace categ_anyprog=1 if perc_anyprog>0 & perc_anyprog<=0.02
replace categ_anyprog=2 if perc_anyprog>0.02 & perc_anyprog<=0.10
replace categ_anyprog=3 if perc_anyprog>0.10 & perc_anyprog<=0.20
replace categ_anyprog=4 if perc_anyprog>0.20 & perc_anyprog!=.
*doing summary statistics by category
by categ_anyprog, sort: sum perc_white perc_black medianincome pop_dens pop_chng

*generate a categorical variable based on the distribution of parcels but with rounded percentages CITY OWNED PROGRAM - better way to bin these?
capture drop categ_cityanyprog
summarize cityownedprogramsubset, detail
gen categ_cityanyprog=0 if perc_cityanyprog==0
replace categ_cityanyprog=1 if perc_cityanyprog>0 & perc_cityanyprog<=0.001
replace categ_cityanyprog=2 if perc_cityanyprog>0.001 & perc_cityanyprog<=0.003
replace categ_cityanyprog=3 if perc_cityanyprog>0.003 & perc_cityanyprog<=0.01
replace categ_cityanyprog=4 if perc_cityanyprog>0.01 & perc_cityanyprog!=.
*doing summary statistics by category
by categ_cityanyprog, sort: sum perc_white perc_black medianincome pop_dens pop_chng

*generate neighborhood income quartiles
xtile incquart=medianincome, nq(4)

*doing regressions with one or more regressors
reg perc_anyprog perc_white 
reg perc_anyprog perc_white medianincome
regress perc_bid medianincome
regress perc_cityanyprog medianincomechangefrom2011

*Scatter plots
scatter perc_adopt perc_vac medianincomechangefrom2011, msize(1pt 1pt)
scatter perc_anyprog perc_black, msize(2pt 2pt)
scatter perc_anyprog perc_white, msize(2pt 2pt)
scatter perc_rec medianincome, msize(2pt)

reg perc_rec i.incquart
reg perc_rec i.incquart perc_vac
by incquart, sort: summarize medianincome


