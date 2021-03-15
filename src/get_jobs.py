import numpy as np
from elcc_rk_impl import powGen
import netCDF4 as nk

latitudes, longitudes, cfs = powGen(file1, file2)
