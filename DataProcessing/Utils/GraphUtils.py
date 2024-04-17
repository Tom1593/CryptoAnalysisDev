import networkx as nx
from pyvis.network import Network

class GraphUtils:
  def create_graph(graph) -> None:
    """
  Creates a Graph Chart based on a graph input

  Args:
      graph =  A NetworkX graph object representing the transaction network.

  Returns:
      null, saves and show the graph
  """
    vis_network = Network(directed=True)
    net = Network(height="500px", width="100%", directed=True)

    # Add nodes and edges to the PyVis network
    for node in graph.nodes:
        net.add_node(node)

    for start, end, data in graph.edges(data=True):
        net.add_edge(start, end, label=data['weight'], arrows={'to': {'enabled': True, 'scaleFactor': 0.5}})


    # Customize the network
    net.set_edge_smooth('dynamic')
    # net.set_edge_length(200)

    vis_network.barnes_hut()
    vis_network.set_options("""
        var options = {
          "edges": {
            "color": {
              "inherit": true
            },
            "smooth": {
              "enabled": true,
              "type": "dynamic"
            }
          },
          "interaction": {
            "dragNodes": true,
            "hideEdgesOnDrag": false,
            "hideNodesOnDrag": false
          },
          "physics": {
            "barnesHut": {
              "gravitationalConstant": -2000,
              "springLength": 250,
              "springConstant": 0.001
            },
            "enabled": true,
            "stabilization": {
              "enabled": true,
              "fit": true,
              "iterations": 1000,
              "onlyDynamicEdges": false,
              "updateInterval": 50
            }
          }
        }
    """)
    vis_network.from_nx(graph)
    
    vis_network.show("Transaction Graph.html",notebook=False)
    net.show("Transaction Graph2.html",notebook=False)  