# scooter_map
Map scooter use with contextily

## Prepare csv and shapefile from .xlsx

```python
cd ..\data_prep #contains .xlsx file
python prep_scooter.py
```
## Load modules
```python
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx
from tqdm import tqdm_notebook as tqdm
```
## Read geo data
```python
ds=pd.read_csv("scooter.csv")
geometry=gpd.read_file('scooter.shp')
ds=gpd.GeoDataFrame(ds,geometry=geometry.geometry)
ds = ds.to_crs(epsg=3857)

ds.lastLocationUpdate=pd.to_datetime(ds.lastLocationUpdate)
```
## Plot spots
```python
ax = ds.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
ctx.add_basemap(ax, zoom=12, source = ctx.providers.OpenStreetMap.Mapnik)
plt.savefig("scooter_all.png",dpi=500)
```
![](https://raw.githubusercontent.com/ambader/scooter_map/main/img/scooter_all.png)
## Plot spot desity
```python
ax = ds.plot(figsize=(10, 10), alpha=0.1, column='count_', cmap='RdPu', legend=True, legend_kwds={'shrink': 0.81})
ctx.add_basemap(ax, zoom=12)
plt.savefig("scooter_dens.png",dpi=500)
```
![](https://raw.githubusercontent.com/ambader/scooter_map/main/img/scooter_dens.png)
