#!/usr/bin/python

import os,json,math                        # general env use and reading json configs
import xarray,pandas,numpy                 # <-- these do 99.9% of processing
from osgeo import gdal, ogr, osr           # to grid shapefile mask and transform netcdf crs for plots

from collections import OrderedDict        # text-escaped dictionarys in output scripts
from dask.diagnostics import ProgressBar   # progress bar for long saves

numpy.seterr(divide='ignore', invalid='ignore')

_dataset = 'mod11a1d'
_file = 'outputs/mod11a1d_processed.nc'
_datavar = 'LST_Day_1km'
_valid_min = '150'
_valid_max = '1310.7'

_mean = _datavar+"_mean"
_variance = _datavar+"_variance"
_stdev = _datavar+"_stdev"

nc = xarray.open_dataset(
    _file, 
    mask_and_scale = True,    
    chunks = dict( time=5, ydim= 1000, xdim= 1000 ) 
)
drylands = nc['drylands']
nc = nc.drop('drylands')

################################################## TESTING
#nc = nc.sel(time=slice("2000-01-01","2003-01-01"))
################################################## TESTING

nc[_datavar].attrs.update(dict(valid_min=_valid_min,valid_max=_valid_max))

data = dict( dates=[] , grid=dict( mean=[],variance=[],stdev=[] ) , series=dict( mean=[],stdev=[] ) )
for year,dataset in nc.groupby('time.year', squeeze=False):
    for month,subdataset in dataset.groupby('time.month', squeeze=False):

        data['dates'].append(pandas.to_datetime(str(year)+"-0"+str(month)+"-"+"01")) 

        _m = subdataset[_datavar].mean('time', keep_attrs = True, skipna=True)
        data['grid']['mean'].append( _m )
        _v = subdataset[_datavar].var('time', keep_attrs = True, skipna=True)
        data['grid']['variance'].append( _v )
        data['grid']['stdev'].append( xarray.ufuncs.sqrt(_v) )

        data['series']['mean'].append( _m.mean(['xdim','ydim'],keep_attrs = True) )
        data['series']['stdev'].append( xarray.ufuncs.sqrt(_v.mean(['ydim','xdim'],skipna = True)) )

grid = xarray.merge([
    xarray.concat(data['grid']['mean'], dim=data['dates']).rename(_mean),
    xarray.concat(data['grid']['variance'], dim=data['dates']).rename(_variance),
    xarray.concat(data['grid']['stdev'], dim=data['dates']).rename(_stdev)
])
grid = grid.rename(dict(concat_dim='time'))
grid['crs'] = nc.crs 
grid['drylands'] = drylands

series = xarray.merge([
    xarray.concat(data['series']['mean'], dim=data['dates']).rename(_mean),
    xarray.concat(data['series']['stdev'], dim=data['dates']).rename(_stdev)
])
series = series.rename(dict(concat_dim='time'))#,xdim='x',ydim='y'))

outf = "outputs/"+_dataset+"_stats.nc"
xarray.Dataset().to_netcdf(outf, unlimited_dims=("time"), compute=True)
writeg = grid.to_netcdf(outf, mode="a", group="/grid/", unlimited_dims=("time"), compute=False)
writes = series.to_netcdf(outf, mode="a", group="/series/", unlimited_dims=("time"), compute=False)

with ProgressBar(): 
    for j in [writer1,writer2,writer3]:
        j.compute()

