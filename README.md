# Washington-Allen et al. (2019)

**About:** Calculate mean, standard deviation, maximum, minimum for various time intervals MODIS time series of 4-day composite LAI (MCD15A3H) and daily daytime and nighttime LST from both Terra (MOD11A2) and Aqua (MYD11A2)

**Cite our manuscript**: In prep

## Requirements

**Python environment**
I recommend setting up a dedicated environment when using GDAL because the python bindings can be a real PITA if you have multiple Python installs or other dependent GIS software.
* netCDF4 : 	```conda install -c conda-forge netcdf4``` | [Unidata](http://unidata.github.io/netcdf4-python/)
* gdal : ```conda install -c conda-forge gdal``` | [OSGeo](https://gdal.org/python/)

*--- I'll upload an env config at some point  so you can duplicate mine*

**NetCDF operators (NCO)**
Unidata provides a powerful set of tools for manipulating n-dimensional arrays stored in netCDF format...


## Run
**1.** Crop datasets to dryland extent as defined by 
# 
# 
# 

# BELOW IS SCRATCH



































## Inputs
Inputs are netCDF4 format outputs from APPEEARS (https://lpdaacsvc.cr.usgs.gov/appeears/). Request the input data for this analysis using the following JSON strings:
### MODIS 
We use netCDF version 4  files from ...

* 4-day Leaf Area Index and QC datasets from MCD15A3H (Terra+Aqua):
```
<json goes here>
```
* Daily Daytime and Nightime Land Surface Temperature and QC datasets from MOD11A2 (Terra) and MYD11A2 (Aqua):
```
<json goes here>
```
### Aridity Index
ai.shp | WGS84 - ESRI Shapefile
Transform to sinusoidal: [https://www.gdal.org/ogr2ogr.html]
```
$ ogr2ogr -t_srs "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs " ai-drylands-sinu.shp  ai-drylands.shp
```



## Outputs
### CSV
### NetCDF
### GeoTIFF
**LST Terra:**
Day Monthly (12/year)
Day Yearly (1/year)
Night Monthly (12/year)
Night Yearly (1/year)
**LST Aqua:**
Day Monthly (12/year)
Day Yearly (1/year)
Night Monthly (12/year)
Night Yearly (1/year)
**LAI Combined:**
Monthly (12/year)
Yearly (1/year)

# Aridity index


# Testing
```
/<path_to_nco>/nco/ncks -d time,1,8 MCD15A3H.006_500m_aid0001.nc -O MCD15A3H.006_500m_aid0001_short.nc
/<path_to_nco>/nco/ncks -d time,1,29 MOD11A1.006_1km_aid0001.nc -O MOD11A1.006_1km_aid0001_short.nc
/<path_to_nco>/nco/ncks -d time,1,29 MYD11A1.006_1km_aid0001.nc -O MYD11A1.006_1km_aid0001_short.nc
```


<!--stackedit_data:
eyJoaXN0b3J5IjpbLTkzMTE3MDI4NSwxMzE3NDk3ODM4LC0xND
A5MTU2MjI4LC04ODIwOTY3ODgsLTE2MjE4NzE0MjcsLTkwNDQz
Njc1Nl19
-->