# scooter_map
Create GeoDataFrame with contextily and plot e-scooter mobility with OpenStreetMap.

The .xlsx file contains the status report of a commercial e-scooter fleet in Heidelberg and Mannheim. The [prep_scooter.py](https://github.com/ambader/scooter_map/blob/main/data_prep/prep_scooter.py) file contains the code to generate a .csv and shapefiles to use geopandas.

## Preview
![](https://raw.githubusercontent.com/ambader/scooter_map/main/img/plotly_scooter.gif)
![](https://raw.githubusercontent.com/ambader/scooter_map/main/img/scooter_sns.png)

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
plt.tight_layout()
plt.savefig("scooter_all.png",dpi=500)
```
![](https://raw.githubusercontent.com/ambader/scooter_map/main/img/scooter_all.png)
## Plot spot desity
```python
ax = ds.plot(figsize=(10, 10), alpha=0.1, column='count_', cmap='RdPu', legend=True, legend_kwds={'shrink': 0.755})
ctx.add_basemap(ax, zoom=12)
plt.tight_layout()
plt.savefig("scooter_dens.png",dpi=500)
```
![](https://raw.githubusercontent.com/ambader/scooter_map/main/img/scooter_dens.png)

## Plot both with Seaborn
```python
import seaborn as sns
sns.set_theme(style="darkgrid")

fig, axes = plt.subplots(1, 2, figsize=(21, 9))

fig.suptitle('Scooter Maps',fontsize=30)
axes[0].set_title('Observed Spots',fontsize=10)
axes[1].set_title('Scooter density at Spots',fontsize=10)

ax = ds.plot(ax=axes[0],figsize=(9, 9), alpha=0.5, edgecolor='k')
ctx.add_basemap(ax,zoom=12, source = ctx.providers.OpenStreetMap.Mapnik)

ax = ds.plot(ax=axes[1],figsize=(12, 12), alpha=0.1, column='count_', cmap='RdPu', legend=True, legend_kwds={'shrink': .99})
ctx.add_basemap(ax, zoom=12)

plt.tight_layout()

plt.savefig("scooter_sns.png",dpi=250)
```
![](https://raw.githubusercontent.com/ambader/scooter_map/main/img/scooter_sns.png)

## Plot sample with plotly

```python
ds_p = ds[ds.licencePlate.isin(ds.licencePlate.unique()[:5])]

import plotly.express as px

fig = px.line_mapbox(ds_p, lat="lat", lon="lng", hover_name="licencePlate", hover_data=["licencePlate", "lastLocationUpdate"],color="licencePlate", zoom=12, height=300)
fig.update_layout(mapbox_style="open-street-map")

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
```
![](https://raw.githubusercontent.com/ambader/scooter_map/main/img/plotly_scooter.gif)
