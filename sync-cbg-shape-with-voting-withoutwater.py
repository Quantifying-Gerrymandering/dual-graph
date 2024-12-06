import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from gerrychain import Graph, Partition

shapefile_path = "tl_2020_06_bg20/tl_2020_06_bg20.shp"
cbg_path = "2020-pres-ca-cbg.csv"

gdf = gpd.read_file(shapefile_path)[["GEOID20", "geometry", "STATEFP20", "COUNTYFP20"]]
cbgdf = pd.read_csv(cbg_path, 
                    usecols=["GEOID20", "Name", "T_20_CENS_ADJ_Total", "E_20_PRES_Total", "E_20_PRES_Dem", "E_20_PRES_Rep"], 
                    dtype={"GEOID20": str})

gdf["FIPS"] = gdf["STATEFP20"] + gdf["COUNTYFP20"]
gdf.drop(["STATEFP20", "COUNTYFP20"], axis=1, inplace=True)

cbgdf = cbgdf.rename(columns={"T_20_CENS_ADJ_Total": "CENS_Total",
                              "E_20_PRES_Total": "PRES_Total",
                              "E_20_PRES_Dem": "PRES_Dem",
                              "E_20_PRES_Rep": "PRES_Rep"})

gdf["geometry"] = gdf["geometry"].buffer(0)

gdf = pd.merge(gdf, cbgdf, on="GEOID20", how="inner")
gdf = gdf[gdf["Name"] != "Block Group 0"] # Remove water CBGs
# gdf.info()

# Save the merged dataframe to a shapefile
if not os.path.exists("./synced_cbg_pop_voting_withoutwater_2020"):
    os.makedirs("./synced_cbg_pop_voting_withoutwater_2020")
gdf.to_file("./synced_cbg_pop_voting_withoutwater_2020.shp", driver="ESRI Shapefile")

# Convert gdf to dual graph 
graph = Graph.from_geodataframe(gdf, ignore_errors=False)
print(len(graph.nodes))

# Plot the gdf colored by FIPS code
gdf.plot("FIPS", edgecolor="black", linewidth=0.1)  
plt.show()
