# 2019 cbg map to use for comparison: https://databasin.org/datasets/b6359a64b2fa4d19a8b38ff0c348f2d1/ 

from pathlib import Path
import pandas as pd
import geopandas as gpd
from gerrychain import Graph
import networkx as nx
import matplotlib.pyplot as plt

## Read in new data file without water CBGs
# gdf = gpd.read_file("Downloads/ersp data/shapefiles/synced_cbg_pop_voting_withoutwater_2020/synced_cbg_pop_voting_withoutwater_2020.shp")
gdf = gpd.read_file("/Users/22ysabelc/Downloads/quantifying-gerrymandering/quantifying-gerrymandering-local/data/shapefile_with_islands/shapefile_with_islands.shp") # synced shapefile generated using script from sync-cbg-shape-with-voting repo

# graph = Graph.from_geodataframe(gdf, adjacency="queen")
graph = Graph.from_geodataframe(gdf, ignore_errors=False)

print(len(graph.nodes)) # 25584 CBGs that are non-water (of the 25607 CBGs total in California)

island_geoids = ["060759804011", "060839801001", "061110036181", "061119800001", "060375991002", "060375991001", "060375990001", "060375990002", "060375990003", "060375990004"] # retrieved using mapshaper.org, last digit is the block group number
island_indices = gdf.index[gdf["GEOID20"].isin(island_geoids)].tolist()
print("Island indices: ", island_indices)

# Add edges (ferry paths) between farallon islands and pier 39 (geoid: 060750101011)
pier_39_geoid = "060750101011"
pier_39_index = gdf.index[gdf["GEOID20"] == pier_39_geoid].tolist()[0]
graph.add_edges_from([(island_indices[0], pier_39_index)])
# Add edges (ferry paths) between channel islands and ventura harbor (geoid: 061110025003)
ventura_harbor_geoid = "061110025003"
ventura_harbor_index = gdf.index[gdf["GEOID20"] == ventura_harbor_geoid].tolist()[0]
for island_index in island_indices[1:]: # channel islands <-> ventura harbor
    graph.add_edges_from([(island_index, ventura_harbor_index)])

graph.to_json("/Users/22ysabelc/Downloads/quantifying-gerrymandering/quantifying-gerrymandering-local/data/dual-graph.json")

positions = {node: (row.geometry.centroid.x, row.geometry.centroid.y) 
             for node, row in gdf.iterrows()}
nx.draw(graph, pos=positions, node_size=10, edge_color="blue")
plt.show()
