import sys
import os
import numpy as np
import pandas as pd

from elcc_rk_impl import main # change to elcc_impl later


# Parameters

simulation = dict()
files = dict()
system = dict()
generator = dict()

####################################### DEFAULT #############################################

########## Generic ##########

simulation["year"] = 2019 #reshmi edit changed from 2013 to 2018 to 2019
simulation["region"] = ["NYIS"] # identify the nerc region or balancing authority (e.g. "PACE", "WECC", etc.) # reshmi edit: changed from PACE to nyiso 
simulation["iterations"] = 100 # number of iterations for monte carlo simulation # change number of iterations here
simulation["target reliability"] = 2.4 # loss-of-load-hours per year (2.4 is standard)
simulation["shift load"] = 0 # +/- hours
simulation["debug"] = False # print all information flagged for debug

######## files ########

files["root directory"] = None # change to valid directory to create output directory
files["output directory"] = './'
files["eia folder"] = "../eia8602019/" # changed eia folder here
files["benchmark FORs file"] =  "../efor/Temperature_dependent_for_realtionships.xlsx"
files["total interchange folder"] = "../total_interchange/"
files["saved systems folder"] = "/scratch/mtcraig_root/mtcraig1/shared_data/elccJobs/savedSystems/"

########## System ########### 

# Adjust parameters of existing fleet
system["system setting"] = "save" # none or save (save will load existing fleet capacity or save new folder)
system["oldest year"] = 0 #remove conventional generators older than this year
system["renewable multiplier"] = 1 #multiplier for existing renewables

######### Outages ###########

system["conventional efor"] = .05 #ignored if temperature-dependent FOR is true
system["renewable efor"] = .05 #set to 1 to ignore all W&S generators from current fleet
system["temperature dependent FOR"] = True #implemnts temeprature dependent forced outage rates for 6 known technologies
system["temperature dependent FOR indpendent of size"] = True #implemnts temperature dependent forced outage rates for all generators, 
                                                            #if false only applies to generators greater then 15 MW, ignore if not using temp dependent FORs
system["enable total interchange"] = True #gathers combined imports/exports data for balancing authority N/A for WECC

######### Storage ###########

system["dispatch strategy"] = "reliability"
system["storage efficiency"] = .8 #roundtrip 
system["storage efor"] = 0
system["supplemental storage"] = False # add supplemental storage to simulate higher storage penetration
system["supplemental storage power capacity"] = 1000 # MW
system["supplemental storage energy capacity"] = 1000 # MWh

 