import os
import sys
import numpy as np
from elcc_rk_impl import get_powGen # change to elcc_impl on greatlakes

LAUNCH_FILE = 'elcc_job_0.txt'

def init():

    # Save time and money 
    print("Job Checklist: Have you...")
    user_check("Activated conda environment? (y/n): ",'y')
    user_check("Checked batch resources? (y/n): ",'y')
    user_check("Completed 10 iteration test job? (y/n): ",'y')

    # New launcher file
    new_job()

def user_check(message, test_response):

    status = input(message) == test_response
    if not status:
        sys.exit(1)

def new_job():
    global LAUNCH_FILE

    i = 0
    while os.path.exists('elcc_job_'+str(i)+'.txt'):
        i += 1
    
    LAUNCH_FILE = 'elcc_job_'+str(i)+'.txt'

def add_job(parameters):

    global root_directory
    global LAUNCH_FILE

    # start string with
    parameter_string = ''

    parameters = fix_region_string(parameters)

    for key in parameters:
        parameter_string = parameter_string + ' ' + str(key.replace(' ','_')) + ' ' + str(parameters[key])
    
    with open(LAUNCH_FILE,'a') as f:
        f.write('python -u elcc_driver.py ' + parameter_string + '\n')

def run_job():
# call batch script on current job

    global LAUNCH_FILE

    # only launch non-empty jobs
    if os.path.exists(LAUNCH_FILE):
        # launch job
        os.system('sbatch elcc_batch_job.sbat '+LAUNCH_FILE)

        # start new file for running
        new_job()

def run_map(lats,lons,parameters):

    i = 0 # keep track of job num
    for lat in lats[:]: # half resolution
        parameters['latitude'] = lat

        for lon in lons[:]: # half resolution
            parameters['longitude'] = lon
            add_job(parameters)
            
            i += 1
            # eighteen jobs/node?
            if i % 18 == 0: run_job()
    
    # run last set if necessary
    run_job()

def fix_region_string(parameters):
#list to formatted string

    if 'region' in parameters:
        
        regions = parameters['region']

        if isinstance(regions,str):
            return parameters

        #otherwise fix string
        region_str = '\"' + ' '.join(np.sort(regions)) + '\"'

        region_str = region_str[:-1] + '\"'

        parameters['region'] = region_str
    
    return parameters
    

def main(region,year,tech,tdf):

    global root_directory

    parameters = dict()
    

    ########### DO NOT WRITE ABOVE THIS LINE (please?) #############

    # universal parameters
    if tdf == 'False':
        add_on = '_fixed_for'
    else:
        add_on = ''
    parameters['root directory'] = '/home/ijbd/output/'+region+'/'+str(year)+'/500_MW_'+tech+add_on+'/'
    parameters['year'] = year
    parameters['region'] = region.capitalize()
    parameters['iterations'] = 5000
    parameters['nameplate']=500
    parameters['generator type']=tech
    parameters['temperature dependent FOR'] = tdf

    # variable parameters
    solar_cf_file = "/scratch/mtcraig_root/mtcraig1/shared_data/merraData/cfs/wecc/2018_solar_generation_cf.nc" # only used for getting lat/lons
    wind_cf_file = "/scratch/mtcraig_root/mtcraig1/shared_data/merraData/cfs/wecc/2018_wind_generation_cf.nc" 

    lats, lons, cf = get_powGen(solar_cf_file, wind_cf_file)
    
    run_map(lats,lons,parameters)
    

if __name__ == "__main__":
    init()
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
