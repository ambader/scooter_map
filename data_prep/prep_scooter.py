import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx
from tqdm import tqdm_notebook as tqdm

ds=pd.read_excel("data.xlsx")

dat=pd.DataFrame(columns=ds.columns.values[0].replace('"','').split(","))
for i in range(len(ds)):
    dat.loc[i]=ds.loc[i].values[0].replace('"','').split(",")
    
dat.batteryLevel=dat.batteryLevel.astype(float)
dat.lat=dat.lat.astype(float)
dat.lng=dat.lng.astype(float)
dat["max"]=dat["max"].astype(float)

dat.columns=['id_num', 'id', 'state', 'lastLocationUpdate', 'lastStateChange',
       'batteryLevel', 'lat', 'lng', 'zoneId', 'code', 'licencePlate',
       'isRentable', 'max_lev']

geometry = [Point(xy) for xy in zip(dat.lng, dat.lat)]

crs = {'init': 'epsg:4326'}
gdf = gpd.GeoDataFrame(dat, crs=crs, geometry=geometry)

gdf.lastLocationUpdate=pd.to_datetime(gdf.lastLocationUpdate)
gdf.lastStateChange=pd.to_datetime(gdf.lastStateChange)

gdf.to_csv("scooter.csv",index=False)
gdf.geometry.to_file(driver='ESRI Shapefile', filename='scooter.shp')

lp=ds.licencePlate.unique()
llp={}
for i in lp:
    zw=len(ds[ds.licencePlate==i])
    llp.update({ i : zw })
    
ds['count_']=ds.licencePlate
ds.count_=ds.count_.replace(llp)

ds.to_csv("scooter.csv",index=False)
