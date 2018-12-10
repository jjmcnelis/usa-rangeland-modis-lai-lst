#!/usr/bin/python

import os
import xarray
from osgeo import gdal, ogr, osr
from dask.diagnostics import ProgressBar
import numpy
import pandas
import json
from collections import OrderedDict

if not os.path.exists('outputs'): os.makedirs('outputs')      # make outputs dir if none exists

_dataset = 'mod11a1n'
_f = 'data/MOD11A1.006_1km_aid0001.nc'
_output = 'outputs/mod11a1n_processed.nc'
_lookup = 'data/lst/MOD11A1-006-QC-Night-lookup.csv'
_var = 'lst'
_datavar = 'LST_Night_1km'
_qcvar = 'QC_Night'
_fillvalue = 0
_discard_vars = ['LST_Day_1km', 'QC_Day']

shapefile = "data/ai/ai-drylands-sinu.shp"    # reprojected aridity index shapefile
qc = json.load( open( "qc.json" , "r" ) )

nc = xarray.open_dataset(   # open the netCDF dataset in parallel i/o mode
    _f , 
    mask_and_scale = False ,                                   # no, changes to floats
    drop_variables = _discard_vars,                            # discard these
    chunks =  dict(time=5, ydim= 1000, xdim= 1000)             # ~5m
)

print("---	Making drylands mask . . . ")

shp = ogr.Open(shapefile)                     # open shapefile
lyr = shp.GetLayer()                          # get first (and only) layer
srs = lyr.GetSpatialRef()                     # get srs

ncols,nrows = nc.xdim.size,nc.ydim.size    # get number of cols and rows
ymax,ymin = max(nc.ydim),min(nc.ydim)      # get max and min for y
xmax,xmin = max(nc.xdim),min(nc.xdim)      # get max and min for x
yres=(ymax-ymin)/float(nrows)              # get y res
xres=(xmax-xmin)/float(ncols)              # get x res
geotransform=(xmin,xres,0,ymax,0, -yres)   # define geotransformation

dst_ds = gdal.GetDriverByName('MEM').Create('', ncols, nrows, 1 ,gdal.GDT_Byte)   # open raster obj in memory
dst_rb = dst_ds.GetRasterBand(1)
dst_rb.Fill(0)                          # init with zeros
dst_rb.SetNoDataValue(0)                # set nodata value
dst_ds.SetGeoTransform(geotransform)    # set geotransform

err = gdal.RasterizeLayer(dst_ds, [1], lyr, burn_values=[1])   # rasterize shp. drylands == 1 ; not drylands == 0
dst_ds.FlushCache()

m = dst_ds.GetRasterBand(1).ReadAsArray()

nzero_ix = numpy.argwhere(m)                    # get index of every non-zero point
tl = nzero_ix.min(axis=0).tolist()              # get min of indices for both dims
br = nzero_ix.max(axis=0).tolist()              # get max of indices for both dims
ext = [v for v in [tl[0],br[0],tl[1],br[1]]]    # _ymax _ymin _xmax _xmin

print("---	Masking dataset . . . ")

# add the mask to the input dataset as a new variable called 'drylands'
nc['drylands'] = xarray.DataArray( m , coords = [ nc.ydim , nc.xdim ] , dims = [ 'ydim' , 'xdim' ] )
nc.drylands.attrs = dict(                         # add some attributes to describe the new mask variable
    grid_mapping='crs',                           # "grid_mapping" (CF standard) instruct software how to grid data
    flag_values=(0,1),                            # "flag_values" sometimes interpretable by software
    flag_meanings='non_drylands drylands',        # same is true for "flag_meanings" 
    _FillValue=0                                  # and most software hide "_FillValues" by default
)
nc = nc[ dict(ydim=slice(ext[0],ext[1]), xdim=slice(ext[2],ext[3])) ] # trim dataset to mask extent
nc[_datavar] = nc[_datavar].where( nc.drylands == 1 , _fillvalue ) # apply mask

print("---	Quality filtering . . . ")

lookup = pandas.read_csv(_lookup)
criteria = qc[_var]
qcv = lookup.loc[(
    ( lookup[ list(criteria.keys())[0] ].isin( list(criteria.values())[0] ) & 
      lookup[ list(criteria.keys())[1] ].isin( list(criteria.values())[1] ))
), "Value"].tolist()
nc[_datavar] = nc[_datavar].where( nc[_qcvar].isin(qcv) , _fillvalue ) # apply filter
nc = nc.drop(_qcvar)

print("---	Writing output time series:  . . . ")

from dask.diagnostics import ProgressBar # load dask's progress bar

# initialize output job
timeseries = nc.to_netcdf( _output , unlimited_dims="time" , compute=False )

# do queued calculations and save
with ProgressBar(): 
    timeseries.compute()

