from pathlib import Path
import pandas as pd
import geopandas as gpd
from gerrychain import Graph
import networkx as nx
import matplotlib.pyplot as plt

# gdf = gpd.read_file("Downloads/ersp data/shapefiles/synced_cbg_pop_and_voting_2020_shapefile/cbg_pop_and_voting_2020.shp")
gdf = gpd.read_file("cbg_pop_and_voting_2020.shp") # synced shapefile generated using script from sync-cbg-shape-with-voting repo

## attempting to combine all shapefiles (water and pop&voting) into one
# folder = Path("/Users/22ysabelc/Downloads/ersp data/shapefiles")
# shapefile_paths = list(folder.glob("*/*.shp"))
# shapefiles = []
# for shp in shapefile_paths: 
#     shp_file = gpd.read_file(shp)
#     shp_file = shp_file.to_crs(3310)
#     shapefiles.append(shp_file)
#     print(shp_file.crs)
# gdf = pd.concat(shapefiles, ignore_index=True).pipe(gpd.GeoDataFrame)
# gdf.to_file(folder / 'compiled.shp')

print("read files")
gdf = gdf.to_crs(3310) # reproject to projected coordinate system (3310 = California Albers)

dual_graph = Graph.from_geodataframe(gdf, adjacency="queen")
dual_graph.to_json("dual_graph.json")

print(len(dual_graph.nodes)) # 25607 CBGs

positions = {node: (row.geometry.centroid.x, row.geometry.centroid.y) 
             for node, row in gdf.iterrows()}
nx.draw(dual_graph, pos=positions, node_size=10, edge_color="blue")
plt.show()
