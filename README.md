
# About

This repository documents  data acquisition and processing for **Washington-Allen et al. 2019 (in prep)**. Processed in **Python (3.6) environment** using common scientific data processing libraries.      

**Analysis:** [**Jupyter Notebook**](analysis.ipynb)
**Questions:** [jjmcnelis@outlook.com](mailto:jjmcnelis@outlook.com)

## Environment

**Windows 10 running Ubuntu 16.04 via Windows Subsystem for Linux** 
All consumer-grade hardware: i7 8700K 6-cores (12t), 32g memory, 500G SSD (PCIe NVM-e form factor).
**Python 3.6 --- required packages**
* `xarray` pandas-like toolkit for analytics on n-dimensional arrays http://xarray.pydata.org/en/stable/index.html 
* `dask` flexible library for parallel computing https://docs.dask.org/en/latest/ 
* `gdal,ogr,osr` only used to make a grid from the drylands mask. Use GDAL command-line tools if gdal for python isnt available. 
* 
## Tools

***Panoply***        https://www.giss.nasa.gov/tools/panoply/       

Panoply is a popular viewer for NetCDF (and HDF, GRIB, etc) that takes advantage of the format's rich internal metadata. Plots 1- and 2-dimensional arrays with a lot of customization options.

***GDAL/OGR***       https://gdal.org/          

[gdal_rasterize](https://www.gdal.org/gdal_rasterize.html) `gdal_rasterize` to make the mask
```
gdal_rasterize \
-burn 1 \
-of "GTiff" \
-a_srs "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs" \
-a_nodata 0 \
-te <xmin> <ymin> <xmax> <ymax> \
-tr <xres> <yres> \
-ot Byte \
in.shp out.<ext>
```

[ogr2ogr](https://www.gdal.org/ogr2ogr.html) use `ogr2ogr` to do the transformation:
```
# proj4 string for MODIS Sinusoidal:        
# +proj=sinu +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs

ogr2ogr -a_srs "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs " data/ai/ai-drylands-sinu.shp data/ai/ai-drylands.shp
```

## Datasets

### Data acquisition        
Used [APPEEARS (LPDAAC)](https://lpdaac.usgs.gov/tools/data_access/appeears) to get the time series for the full history of MODIS Terra and Aqua for 8-day Leaf Area Index ([MOD15A2H](https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/mod15a2h_v006) and [MYD15A2H](https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/myd15a2h_v006)) and daily Land Surface Temperature ([MOD11A1](https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/mod11a1_v006) and [MYD11A1](https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/myd11a1_v006)) for daytime and nighttime. 

You can submit identical orders to APPEEARS using the JSON included in each products data folder, e.g for Terra and Aqua LAI ([`data/lai/US-LAI-TerraAqua-June-August-request.json`](data/lai/US-LAI-TerraAqua-June-August-request.json)):
```
{
   "error":null,
   "params":{
      "geo":{
         "type":"FeatureCollection",
         "features":[{"type":"Feature",
                      "geometry":{"type":"Polygon","coordinates":[ <very long list of vertices for CONUS boundary> ]},
                      "properties":{"NAME":"United States","GEOID":"US","AFFGEOID":"0100000US"}}],
                      "fileName":"CONUS"},
      "dates":[{"endDate":"08-31","recurring":true,"startDate":"06-01","yearRange":[2000,2022]}],
      "layers":[
         {"layer":"Lai_500m","product":"MOD15A2H.006"},
         {"layer":"LaiStdDev_500m","product":"MOD15A2H.006"},
         {"layer":"FparLai_QC","product":"MOD15A2H.006"},
         {"layer":"FparLai_QC","product":"MYD15A2H.006"},
         {"layer":"LaiStdDev_500m","product":"MYD15A2H.006"},
         {"layer":"Lai_500m","product":"MYD15A2H.006"}],
      "output":{"format":{"type":"netcdf4"},"projection":"sinu_modis"},
      "coordinates":[]
   },
   "status":"processing",
   "created":"2018-12-01T02:08:33.690625",
   "task_id":"8838208d-4c94-41d0-a67c-de35b8b08097",
   "updated":"2018-12-01T02:08:33.750654",
   "user_id":"jjmcnelis@outlook.com",
   "retry_at":null,
   "task_name":"US_LAI-TerraAqua_June-August",
   "task_type":"area",
   "api_version":null,
   "svc_version":"2.13.1",
   "web_version":"2.13.1",
   "expires_on":"2018-12-31T02:08:33.750654",
   "attempts":1
}
```
### Data metadata    
Used a JSON file [`datasets.json`](datasets.json) to store some metadata about each of the datasets. This file is consumed by the code at the bottom of the notebook to write python scripts that do the analysis for each dataset.
   
    {'datavar': 'Lai_500m',
     'discard_vars': ['FparExtra_QC', 'LaiStdDev_500m'],
     'file': 'data/MOD15A2H.006_500m_aid0001.nc',
     'fillvalue': 255,
     'long_name': 'MOD15A2H MODIS/Terra Gridded 500M Leaf Area Index LAI (8-day '
                  'composite)',
     'lookup': 'data/lai/MOD15A2H-006-FparLai-QC-lookup.csv',
     'output': 'outputs/mod15a2h_processed.nc',
     'qcvar': 'FparLai_QC',
     'valid_max': 100,
     'valid_min': 0,
     'var': 'lai'}
    
### Format

***NetCDF*** https://www.unidata.ucar.edu/software/netcdf/       

NetCDF is a self-describing, machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data. Prefered format is [CF-1.6 Convention](http://cfconventions.org/), but these files aren't fully compliant. I recommend [Panoply](/link/to/panoply) to quickly browse grids and time series. 

* *Dimensions*

Variable data are organized along *fixed* dimensions and *record*, or *unlimited*, dimensions (usually `time`). For example, in our MOD15A2H dataset:

`time` is `226` records long; 8-day MODIS products (LAI) have 46 composite periods per year; June, July, August alone ~ `46 / 4 = ~ 11` timesteps per year, and roughly `226 / 11 = ~ 19` years of data.    

`ydim` and `xdim` dimensions are of length `5932` and `12761`, respectively. MODIS pixels for LAI are roughly 463 meters tall, so `5932 * 463 = 2,746,516` meters, or 2,700 kilometers vertical coverage in the datasets. Very close to ~2500 km distance between southern tip of Texas and Canadian border. Can't check `xdim` because sinusoidal projection distorts horizontal drastically.

* *Variables*

Variables in the netCDF retain the names of their parent subdatasets in the MODIS HDF files stored at LP DAAC:
https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/mod15a2h_v006
<!--stackedit_data:
eyJoaXN0b3J5IjpbMjA3MjE1NDI3Nl19
-->