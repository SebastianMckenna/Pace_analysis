import xarray as xr
import xesmf as xe
import numpy as np
import dask
import cftime
import glob
import os
def isosurface(field, target, dim):
    """
    Linearly interpolate a coordinate isosurface where a field
    equals a target

    Parameters
    ----------
    field : xarray DataArray
        The field in which to interpolate the target isosurface
    target : float
        The target isosurface value
    dim : str
        The field dimension to interpolate
        
    Examples
    --------
    Calculate the depth of an isotherm with a value of 5.5:
    
    >>> temp = xr.DataArray(
    ...     range(10,0,-1),
    ...     coords={"depth": range(10)}
    ... )
    >>> isosurface(temp, 5.5, dim="depth")
    <xarray.DataArray ()>
    array(4.5)
    """
    slice0 = {dim: slice(None, -1)}
    slice1 = {dim: slice(1, None)}

    field0 = field.isel(slice0).drop(dim)
    field1 = field.isel(slice1).drop(dim)

    crossing_mask_decr = (field0 > target) & (field1 <= target)
    crossing_mask_incr = (field0 < target) & (field1 >= target)
    crossing_mask = xr.where(
        crossing_mask_decr | crossing_mask_incr, 1, np.nan
    )

    coords0 = crossing_mask * field[dim].isel(slice0).drop(dim)
    coords1 = crossing_mask * field[dim].isel(slice1).drop(dim)
    field0 = crossing_mask * field0
    field1 = crossing_mask * field1

    iso = (
        coords0 + (target - field0) * 
        (coords1 - coords0) / (field1 - field0)
    )

    return iso.max(dim, skipna=True)
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

def get_regrid_z20_ncfile(file_dir, outfile):
    z20s=[]
    for file in glob.glob(file_dir+"ocean_month.nc-*"):
        ds = xr.open_dataset(file chunks = {"time":12})
        #regrid
        ds_re = regrid_deep(ds)
        #get 20 eg isotherm
        ds_z20 = isosurface(ds_re, 293.15, dim = "depth")
        z20s.append(ds_z20)
    z20 = xr.concat(z20s, dim = 'time')
    #convert to netcdf
    z20.to_netcdf("/g/data/e14/sm2435/Pacemaker/"+outfile)
    return

get_regrid_z20_ncfile("/g/data/hh5/tmp/zg0866/cm000_APP4_archive/cm000/history/ocn/", "ctrl_z20.nc")
get_regrid_z20_ncfile("/scratch/e14/sm2435/archive/cw323/history/ocn/", "OC_z20.nc")
get_regrid_z20_ncfile("/scratch/e14/sm2435/archive/cy286/history/ocn/", "VC_z20.nc")
get_regrid_z20_ncfile("/scratch/w97/zg0866/cs947_raw/history/ocn/", "MC_z20.nc")


