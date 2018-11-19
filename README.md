# MODIS Processing for US Drylands

Calculate monthly and yearly mean, standard deviation, maximum, minimum, amplitude, and integral for MODIS time series of LAI (MCD15A2H) and Daytime and Nighttime LST from Terra (MOD11A2) and Aqua (MYD11A2)


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

# Aridity index mask
```
>>> import netCDF4 as nc4
>>> lai_input = "F:/drylands_modis_lai_lst/test/data/lai/MCD15A3H.006_500m_aid0001.nc"
>>> lai_nc = nc4.Dataset(datadir+lai_input, "r")

>>> print(lai_nc.dimensions['xdim'].size)
>>> print(lai_nc.dimensions['ydim'].size)

12761 
5932

>>> print(max(lai_nc.variables['xdim'][:]))
>>> print(min(lai_nc.variables['xdim'][:]))
>>> print(max(lai_nc.variables['ydim'][:]))
>>> print(min(lai_nc.variables['ydim'][:]))

-5134663.180919099
-11046533.443813546
5491413.972645489
2743506.2509192373
```


<!--stackedit_data:
eyJoaXN0b3J5IjpbMjkyMTg0Mjk4LC05MDQ0MzY3NTZdfQ==
-->