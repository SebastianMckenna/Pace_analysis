import xarray as xr
import numpy as np

import dask
import cftime
import random
import glob

import os

def open_HF_terms(file_dir):
    DS = xr.open_mfdataset((file_dir+"ocean_month.nc-*"), parallel=True)
    sw_pn = DS.sw_heat
    triver = DS.temp_rivermix
    tvdbc = DS.temp_vdiffuse_sbc
    sfc_hflux_pme = DS.sfc_hflux_pme
    Qnet_int = tvdbc.sum("st_ocean") + triver.sum("st_ocean") + sfc_hflux_pme + sw_pn.sum("st_ocean")
    #try to save files
    ds1 = Qnet_int.to_dataset(name = "Qnet")
    return ds1



u = open_u_winds("/g/data/hh5/tmp/zg0866/pacemaker/cs947/history/ocn/")
u.to_netcdf("/g/data/e14/sm2435/Exps_ACCESS_initial/MC_qnet.nc")

u = open_u_winds("/scratch/e14/sm2435/archive/cy286/history/ocn/")
u.to_netcdf("/g/data/e14/sm2435/Exps_ACCESS_initial/VC_qnet.nc")

u = open_u_winds("/scratch/e14/sm2435/archive/cw323/history/ocn/")
u.to_netcdf("/g/data/e14/sm2435/Exps_ACCESS_initial/OC_qnet.nc")

u = open_u_winds("/g/data/hh5/tmp/zg0866/ACCESS-CM2_archive/cm000/history/ocn/")
u.to_netcdf("/g/data/e14/sm2435/Exps_ACCESS_initial/ctrl_qnet.nc")
