# 2019 cbg map to use for comparison: https://databasin.org/datasets/b6359a64b2fa4d19a8b38ff0c348f2d1/ 

from pathlib import Path
import pandas as pd
import geopandas as gpd
from gerrychain import Graph
import networkx as nx
import matplotlib.pyplot as plt

## Read in new data file without water CBGs
# gdf = gpd.read_file("Downloads/ersp data/shapefiles/synced_cbg_pop_voting_withoutwater_2020/synced_cbg_pop_voting_withoutwater_2020.shp")
gdf = gpd.read_file("./data/final_shapefile_without_water/final_shapefile_without_water.shp") # synced shapefile generated using script from sync-cbg-shape-with-voting repo

# graph = Graph.from_geodataframe(gdf, adjacency="queen")
graph = Graph.from_geodataframe(gdf, ignore_errors=False)

print(len(graph.nodes)) # 25584 CBGs that are non-water (of the 25607 CBGs total in California)

"""
Add the following edges:
060750604002 (port) - 060759804011 (farallon island) --- DONE
060750101011 (pier 39) - 060750179032 (alcatraz island) --- DONE
060750615072 - 060750179031 --- DONE
060839801001 (channel island 0) - 061110025003 (ventura harbor) --- DONE
061110036181 (channel island 1) - 061110036172 --- DONE
061119800001 (channel island 2) - 061110036172 --- DONE
060375991001 (channel island 3) - 060375991002 (channel island 4) --- DONE
060375990001 (channel island 5main) - 060375760011 --- DONE
060375990001 (channel island 5main) - 060379800311 --- DONE
060375990001 (channel island 5main) - 060375990002 (channel island 5main_2) --- DONE
060375990001 (channel island 5main) - 060375990003 (channel island 5main_3) --- DONE
060375990001 (channel island 5main) - 060375990004 (channel island 5main_4) --- DONE
060730050001 - 060730110001 --- DONE
"""

# Add edge  between farallon islands and port (geoid: 060759804011)
farallon_island_geoid = "060759804011"
farallon_island_index = gdf.index[gdf["GEOID20"] == farallon_island_geoid].tolist()[0]
port_geoid = "060750604002"
port_index = gdf.index[gdf["GEOID20"] == port_geoid].tolist()[0]
graph.add_edges_from([(farallon_island_index, port_index)])

# Add edge between alcatraz and  pier 39
alcatraz_island_geoid = "060750179032"
alcatraz_island_index = gdf.index[gdf["GEOID20"] == alcatraz_island_geoid].tolist()[0]
pier_39_geoid = "060750101011"
pier_39_index = gdf.index[gdf["GEOID20"] == pier_39_geoid].tolist()[0]
graph.add_edges_from([(alcatraz_island_index, pier_39_index)])

# Add edge between 060750615072 and 060750179031
connection1_geoid = "060750615072"
connection2_geoid = "060750179031"
connection1_index = gdf.index[gdf["GEOID20"] == connection1_geoid].tolist()[0]
connection2_index = gdf.index[gdf["GEOID20"] == connection2_geoid].tolist()[0]
graph.add_edges_from([(connection1_index, connection2_index)])

## Add edge between channel islands and their respective ports
channel_islands_geoids = ["060839801001", "061110036181", "061119800001", "060375991002", "060375991001", "060375990001", "060375990002", "060375990003", "060375990004"] # retrieved using mapshaper.org, last digit is the block group number
channel_islands_indices = gdf.index[gdf["GEOID20"].isin(channel_islands_geoids)].tolist()
# Add edge between channel island 0 and ventura harbor (geoid: 061110025003)
ventura_harbor_geoid = "061110025003"
ventura_harbor_index = gdf.index[gdf["GEOID20"] == ventura_harbor_geoid].tolist()[0]
graph.add_edges_from([(channel_islands_indices[0], ventura_harbor_index)])
# Add edges between channel island 1 and 2 and their shared port (geoid: 061110036172)
channel_island_1and2_port_geoid = "061110036172"
channel_island_1and2_port_index = gdf.index[gdf["GEOID20"] == channel_island_1and2_port_geoid].tolist()[0]
graph.add_edges_from([(channel_islands_indices[1], channel_island_1and2_port_index)])
graph.add_edges_from([(channel_islands_indices[2], channel_island_1and2_port_index)])
# Add edge between channel island 3 and channel island 4
graph.add_edges_from([(channel_islands_indices[3], channel_islands_indices[4])])
# Add edges between channel island 5main and its two ports (geoids: 060375760011 and 060379800311)
channel_island_5main_port1_geoid = "060375760011"
channel_island_5main_port1_index = gdf.index[gdf["GEOID20"] == channel_island_5main_port1_geoid].tolist()[0]
channel_island_5main_port2_geoid = "060379800311"
channel_island_5main_port2_index = gdf.index[gdf["GEOID20"] == channel_island_5main_port2_geoid].tolist()[0]
graph.add_edges_from([(channel_islands_indices[5], channel_island_5main_port1_index)])
graph.add_edges_from([(channel_islands_indices[5], channel_island_5main_port2_index)])
# Add edges between channel island 5main and the three 5main subparts
graph.add_edges_from([(channel_islands_indices[5], channel_islands_indices[6])])
graph.add_edges_from([(channel_islands_indices[5], channel_islands_indices[7])])
graph.add_edges_from([(channel_islands_indices[5], channel_islands_indices[8])])

# Add edge between 060730050001 and 060730110001
connection3_geoid = "060730050001"
connection4_geoid = "060730110001"
connection3_index = gdf.index[gdf["GEOID20"] == connection3_geoid].tolist()[0]
connection4_index = gdf.index[gdf["GEOID20"] == connection4_geoid].tolist()[0]
graph.add_edges_from([(connection3_index, connection4_index)])

graph.to_json("./dual-graph.json")

positions = {node: (row.geometry.centroid.x, row.geometry.centroid.y) 
             for node, row in gdf.iterrows()}
nx.draw(graph, pos=positions, node_size=10, edge_color="blue")
plt.show()
