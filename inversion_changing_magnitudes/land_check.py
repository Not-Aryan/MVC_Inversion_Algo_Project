import pandas as pd
import numpy as np
import geopandas as gpd

df = pd.read_table("Traction.gmt", sep="\s+", usecols=[0, 1, 2, 3, 4, 5, 6], names=['lon','lat', 'Fx', 'Fy', 'stdFx', 'stdFy', 'corr_xy'])

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['lon'], df['lat']))
gdf.crs = {'init' :'epsg:4326'}
result = gpd.sjoin(gdf, world, how='left')

df1 = pd.DataFrame(result)
rslt_df = df1[df1["iso_a3"]=="GRL"]

df_subset = rslt_df[['lon','lat', 'Fx', 'Fy', 'stdFx', 'stdFy', 'corr_xy']]
df_subset.to_csv("traction_parsed.gmt", index=False, header=None, sep=" ")