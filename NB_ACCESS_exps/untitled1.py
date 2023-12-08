import xarray as xr
import numpy as np

import dask
import cftime
import random
import glob

import os

def open_u_winds(file_dir):
    DS = xr.open_mfdataset(file_dir+"ocean_month.nc-*"), parallel=True)
    tauu = DS.tau_x
    #try to save files
    ds1 = tauu.to_dataset(name = "tauu")
    return ds1

def open_v_winds(file_dir):
    DS = xr.open_mfdataset(glob.glob(file_dir+"ocean_month.nc-*"), parallel=True)
    tauv = DS.tau_y
    #try to save files
    ds1 = tauv.to_dataset(name = "tauv")
    return ds1

u = open_u_winds("/scratch/w97/zg0866/cs947_raw/history/ocn/")
u.to_netcdf("/g/data/e14/sm2435/Pacemaker/mod_uwnd.nc")
v = open_v_winds("/scratch/w97/zg0866/cs947_raw/history/ocn/")
v.to_netcdf("/g/data/e14/sm2435/Pacemaker/mod_vwnd.nc")
u = open_u_winds("/scratch/e14/sm2435/archive/cy286/history/ocn/")
u.to_netcdf("/g/data/e14/sm2435/Pacemaker/var_uwnd.nc")
v = open_v_winds("/scratch/e14/sm2435/archive/cy286/history/ocn/")
v.to_netcdf("/g/data/e14/sm2435/Pacemaker/var_vwnd.nc")
u = open_u_winds("/scratch/e14/sm2435/archive/cw323/history/ocn/")
u.to_netcdf("/g/data/e14/sm2435/Pacemaker/ob_uwnd.nc")
v = open_v_winds("/scratch/e14/sm2435/archive/cw323/history/ocn/")
v.to_netcdf("/g/data/e14/sm2435/Pacemaker/ob_vwnd.nc")
u = open_u_winds("/g/data/hh5/tmp/zg0866/ACCESS-CM2_archive/cm000/history/ocn/")
u.to_netcdf("/g/data/e14/sm2435/Pacemaker/ctrl_uwnd.nc")
v = open_v_winds("/g/data/hh5/tmp/zg0866/ACCESS-CM2_archive/cm000/history/ocn/")
v.to_netcdf("/g/data/e14/sm2435/Pacemaker/ctrl_vwnd.nc")