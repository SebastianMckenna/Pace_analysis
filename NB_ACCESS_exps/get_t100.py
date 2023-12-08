import xarray as xr
import xesmf as xe
import numpy as np
import dask
import cftime
#write regridder
def regrid_deep(ds):
    #drop unnecessary coords from input
    ds = ds.drop(["geolon_c", "geolat_c", 'xu_ocean', 'nv', 'yu_ocean', 'sw_ocean','st_edges_ocean','sw_edges_ocean', 'grid_xu_ocean', 'grid_yt_ocean', 'potrho', 'potrho_edges', 'grid_xt_ocean', 'grid_yu_ocean'])
    #create output grid
    ds_out = xe.util.grid_global(1, 1)
    ds_out = ds_out.drop({'lon_b', 'lat_b'})
    #rename grid coords
    ds_out = ds_out.rename({'lon': 'longitude', 'lat': 'latitude'})
    #drop and rename part of input
    ds_in = ds.drop({'xt_ocean', 'yt_ocean'}).rename({"geolon_t": "longitude", "geolat_t": "latitude", "st_ocean":"depth"})
    #creatre regridder
    regridder = xe.Regridder(ds_in, ds_out, 'bilinear', periodic=True)
    regridded = regridder(ds_in['temp'].chunk({'xt_ocean': -1, 'yt_ocean': -1}))
    regridded = regridded.assign_coords({'x': ds_out.longitude[0, :], 'y': ds_out.latitude[:, 0]})
    regridded = regridded.rename({'x': 'longitude', 'y': 'latitude'})
    return regridded
#open dataset
ctrl = xr.open_mfdataset("/g/data/hh5/tmp/zg0866/cm000_APP4_archive/cm000/history/ocn/ocean_month.nc-*",parallel = True, chunks = {"time":12})
#regrid
ctrl_re = regrid_deep(ctrl)
ctrl_re = ctrl_re.sel(depth = 105) - 273.15
#convert to netcdf
ctrl_re.to_netcdf("/g/data/e14/sm2435/Pacemaker/ctrl_100_t.nc")

#open dataset
OC = xr.open_mfdataset("/scratch/e14/sm2435/archive/cw323/history/ocn/ocean_month.nc-*",parallel = True, chunks = {"time":12})
#regrid
OC = regrid_deep(OC)
OC = OC.sel(depth = 105) - 273.15
#convert to netcdf
OC.to_netcdf("/g/data/e14/sm2435/Pacemaker/OC_100_t.nc")

#open dataset
VC = xr.open_mfdataset("/scratch/e14/sm2435/archive/cy286/history/ocn/ocean_month.nc-*",parallel = True, chunks = {"time":12})
#regrid
VC = regrid_deep(VC)
VC = VC.sel(depth = 105) - 273.15
#convert to netcdf
VC.to_netcdf("/g/data/e14/sm2435/Pacemaker/VC_100_t.nc")