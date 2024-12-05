import geopandas as gpd
from gerrychain import Graph
import networkx as nx
import matplotlib.pyplot as plt

# geodata = gpd.read_file("Downloads/ersp data/synced_cbg_pop_and_voting_2020_shapefile/cbg_pop_and_voting_2020.shp")
geodata = gpd.read_file("cbg_pop_and_voting_2020.shp")
print("read file")

dual_graph = Graph.from_geodataframe(geodata, adjacency="queen")
dual_graph.to_json("dual_graph.json")

print(len(dual_graph.nodes)) # 25607 CBGs

positions = {node: (row.geometry.centroid.x, row.geometry.centroid.y) 
             for node, row in geodata.iterrows()}
nx.draw(dual_graph, pos=positions, node_size=10, edge_color="blue")
plt.show()