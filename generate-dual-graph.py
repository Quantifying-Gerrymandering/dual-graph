# 2019 cbg map to use for comparison: https://databasin.org/datasets/b6359a64b2fa4d19a8b38ff0c348f2d1/ 

import os
from pathlib import Path
import pandas as pd
import geopandas as gpd
from gerrychain import Graph
import networkx as nx
import matplotlib.pyplot as plt

# Read in new data file without water CBGs
gdf = gpd.read_file("synced_cbg_pop_voting_withoutwater_2020/synced_cbg_pop_voting_withoutwater_2020.shp") # synced shapefile generated using script from sync-cbg-shape-with-voting repo

gdf = gdf.to_crs(3310) # Reproject to projected coordinate system (3310 = California Albers)

dual_graph = Graph.from_geodataframe(gdf, adjacency="queen")
dual_graph.to_json("dual_graph.json")

print(len(dual_graph.nodes)) # 25584 CBGs that are non-water (of the 25607 CBGs total in California)

positions = {node: (row.geometry.centroid.x, row.geometry.centroid.y) 
             for node, row in gdf.iterrows()}
nx.draw(dual_graph, pos=positions, node_size=10, edge_color="blue")
plt.show()

# if not os.path.exists("./dual_graph_withoutwater"):
#     os.makedirs("./dual_graph_withoutwater")
# gdf.to_file("./dual_graph_withoutwater.shp", driver="ESRI Shapefile")