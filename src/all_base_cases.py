rom elcc_map_base_case import main

for region in ['nyiso']:
    for year in [2015, 2016,2017,2018,2019]:
        for tech in ['solar', 'wind']:
            for tdf in ['True', 'False']:

                main(region,year,tech,tdf)s