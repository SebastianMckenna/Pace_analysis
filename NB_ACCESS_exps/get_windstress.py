import xarray as xr
import numpy as np

import dask
import cftime
import random
import glob

import os

def open_qnet_winds(file_dir):
    DS = xr.open_mfdataset(file_dir+"ocean_month.nc-*"), parallel=True)
    tauu = DS.tau_x
    #try to save files
    ds1 = tauu.to_dataset(name = "tauu")
    return ds1

u = open_u_winds("/scratch/w97/zg0866/cs947_raw/history/ocn/")
u.to_netcdf("/g/data/e14/sm2435/Exps_ACCESS_initial/mod_uwnd.nc")
v = open_v_winds("/scratch/w97/zg0866/cs947_raw/history/ocn/")
v.to_netcdf("/g/data/e14/sm2435/Exps_ACCESS_initial/mod_vwnd.nc")
u = open_u_winds("/scratch/e14/sm2435/archive/cy286/history/ocn/")
u.to_netcdf("/g/data/e14/sm2435/Exps_ACCESS_initial/var_uwnd.nc")
v = open_v_winds("/scratch/e14/sm2435/archive/cy286/history/ocn/")
v.to_netcdf("/g/data/e14/sm2435/Exps_ACCESS_initial/var_vwnd.nc")
u = open_u_winds("/scratch/e14/sm2435/archive/cw323/history/ocn/")
u.to_netcdf("/g/data/e14/sm2435/Exps_ACCESS_initial/ob_uwnd.nc")
v = open_v_winds("/scratch/e14/sm2435/archive/cw323/history/ocn/")
v.to_netcdf("/g/data/e14/sm2435/Exps_ACCESS_initial/ob_vwnd.nc")
u = open_u_winds("/g/data/hh5/tmp/zg0866/ACCESS-CM2_archive/cm000/history/ocn/")
u.to_netcdf("/g/data/e14/sm2435/Exps_ACCESS_initial/ctrl_uwnd.nc")
v = open_v_winds("/g/data/hh5/tmp/zg0866/ACCESS-CM2_archive/cm000/history/ocn/")
v.to_netcdf("/g/data/e14/sm2435/Exps_ACCESS_initial/ctrl_vwnd.nc")