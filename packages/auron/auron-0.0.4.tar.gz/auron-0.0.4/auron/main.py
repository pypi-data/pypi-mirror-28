"""

Usage:
    auron <process> <testname> <ldf> [--cell=<cellname>] [--union] [--layer=<layer>] [--filter]
    auron (-h | --help)
    auron (-V | --version)

Options:
    -h --help     Show this screen.
    -p --pretty   Prettify the output.
    -V --version  Show version.
    --quiet       print less text
    --verbose     print more text

"""


from docopt import docopt
from itertools import count

from yuna import machina

from auron import mesh
from auron import graphlvs
from auron import tools

import os
import gdsyuna
import meshio
import subprocess
import networkx as nx
import pygmsh as pg
import numpy as np
import matplotlib.pyplot as plt


"""
Hacker: 1h3d*n
For: Volundr
Docs: Algorithm 1
Date: 31 April 2017

Description: Morph the moat layer and the wire layers.

1) Get a list of all the polygons inside the GDS file.
2) Send this list to the Clip library with the wiring
   layer number and the moat layer number as parameters.
3) Get the union of all the wiring layer polygons that
   are connected. Update this to check for vias.
4) Get the intersection of the moat layer with the
   wiring layer and save this in a new polygon.
5) Get the difference of the moat layer with the
   wiring layer and save this in a new polygon.
6) Join the intersected and difference polygons
   to form a list of atleast 3 polygons.
7) We now know which part of the wiring layer
   goes over the moat is most probably mutually
   connected to wiring layer 2.
8) Send this polygon structure to GMSH.
"""


def draw_graph(g):
    pos = {n: g.nodes[n]['pos'] for n in g.nodes()}
    # labels = {n: n for n in g.nodes()}
    labels = {n: g.node[n]['layer'] for n in g.nodes()}
    colors = [g.node[n]['color'] for n in g.nodes()]
    
    nx.draw_networkx_edges(g, pos=pos, edgelist=g.edges(), alpha=0.5, with_labels=True)
    nx.draw_networkx_nodes(g, pos=pos, nodelist=g.nodes(), node_size=600, node_color=colors, cmap=plt.cm.jet)
    nx.draw_networkx_labels(g, pos=pos, labels=labels, font_size=8)
    
    plt.show()
    

def main():
    """  """

    arguments = docopt(__doc__, version='Yuna 0.0.1')
    tools.red_print('Summoning Yuna...')
    tools.parameter_print(arguments)

    examdir = os.getcwd() + '/tests/' + arguments['<process>'] + '/' + arguments['<testname>']
    gds_file = examdir + '/' + arguments['<testname>'] + '.gds'

    if arguments['--cell'] == 'list':
        gds_file = examdir + '/' + testname + '.gds'
        tools.list_layout_cells(gds_file)
    elif arguments['--cell']:
        auron_cell, Params, Layers = machina(arguments, '')
        
        if arguments['--layer'] is not None:
            lg = single_layer_graph(arguments['--layer'], auron_cell, gds_file, Params, Layers, arguments['--filter'])
            lg.draw_graph()
        else:
            graphs = list()
            for gds, layer in Layers.items():
                if layer['type'] == 'wire' or layer['type'] == 'shunt':
                    lg = single_layer_graph(gds, auron_cell, gds_file, Params, Layers, arguments['--filter'])
                    
                    if lg is not None:
                        graphs.append(lg)
                        lg.draw_graph()
                    
            # graphs = layer_graphs(auron_cell, gds_file, Params, Layers, arguments['--filter'])
            combine_graphs(graphs)
    else:
        cellref = ""

    tools.red_print('Auron. Done.')
    
    
def single_layer_graph(gds, auron_cell, file_name, Params, Layers, subfilter):
    """ Generating the individual layer graphs."""
    tools.magenta_print('Generating layer graphs')
    
    wires = auron_cell.get_polygons(True)
    labels = auron_cell.get_labels(0)
    
    lg = None
    for key, wire in wires.items():
        if key[0] == int(gds):
            cmesh = mesh.Mesh()
            cmesh.create_wireset_mesh(Layers, int(gds), wire) 

            lg = calculate_graph(int(gds), Layers, Params, cmesh, wires, labels, subfilter)
            lg.g = quotient_nodes(lg.g)
            
    return lg

    
# def layer_graphs(auron_cell, file_name, Params, Layers, subfilter):
#     """ Generating the individual layer graphs."""
#     tools.magenta_print('Generating layer graphs')
# 
#     wires = auron_cell.get_polygons(True)
#     labels = auron_cell.get_labels(0)
# 
#     graphs = list()
#     for gds, layer in Layers.items():
#         if layer['type'] == 'wire' or layer['type'] == 'shunt':
#             # TODO: Apply lambda functino here
#             for key, wire in wires.items():
#                 if key[0] == int(gds):
#                     cmesh = mesh.Mesh()
#                     cmesh.create_wireset_mesh(Layers, int(gds), wire) 
# 
#                     cg = calculate_graph(int(gds), Layers, Params, cmesh, wires, labels, subfilter)
# 
#                     # cg.g = quotient_nodes(cg.g)
# 
#                     graphs.append((int(gds), cg))
#                     print(graphs)
#     return graphs


def calculate_graph(gds, Layers, Params, cmesh, wires, labels, subfilter):
    lvs = graphlvs.LayerGraph(gds, Layers, Params, cmesh, wires, labels)
    lvs.create_graph()
    
    if subfilter:
        tools.green_print('Applying graph node filter')
        
        # First filtering:
        # This filters the minor noise nodes 
        # and added the userdefined nodes. 
        lvs.filter_subgraphs()
        lvs.label_user_triangles()
        
        # Second filtering:
        # Once the usernodes are added, we
        # have to filter the network again 
        # and relabel the branch nodes.
        lvs.filter_subgraphs()
        lvs.label_branch_nodes()
    
        # Third filtering:
        # Group label the nodes for the quotient graph.
        lvs.filter_wire_nodes()
    return lvs

    
def combine_graphs(graphs):
    """ Read in Mesh and manipulate it from here on out. """
    
    layergraphs = [lg.g for lg in graphs]
    g = nx.disjoint_union_all(layergraphs)
    # print(nx.get_node_attributes(graphs[0].g, 'type'))
    qg = quotient_nodes(g)
    draw_graph(qg)
    

def quotient_nodes(g):
    """ Combine all nodes of the same type into one node. """
    
    # g = lg.g
    
    def partition_nodes(u, v):
        if g.node[u]['type'] == 1 or g.node[u]['type'] == 3:
            if g.node[u]['layer'] == g.node[v]['layer']:
                return True 
            return False

    def sub_nodes(b):
        S = g.subgraph(b)
        color = nx.get_node_attributes(S, 'color')
        layer = nx.get_node_attributes(S, 'layer')
        center = nx.get_node_attributes(S, 'pos')
        branch = nx.get_node_attributes(S, 'branch')
        mtype = nx.get_node_attributes(S, 'type')
        
        sub_color = list()
        for key, value in color.items():
            sub_color = [value[0], value[1], value[2]]
        
        sub_pos = list()
        for key, value in center.items():
            sub_pos = [value[0], value[1]]
            
        return dict(color=sub_color, layer=layer, pos=sub_pos, branch=branch, type=mtype)
    
    Q = nx.quotient_graph(g, partition_nodes, node_data=sub_nodes, edge_data=None)
    
    Pos = nx.get_node_attributes(Q, 'pos')
    Color = nx.get_node_attributes(Q, 'color')
    Layer = nx.get_node_attributes(Q, 'layer')
    Type = nx.get_node_attributes(Q, 'type')
    Branch = nx.get_node_attributes(Q, 'branch')
    Edges = nx.get_edge_attributes(Q, 'weight')
    
    g1 = nx.Graph()
    for key, value in Edges.items():
        n1, n2 = list(key[0]), list(key[1])
        g1.add_edge(n1[0], n2[0])
        
    for n in g1.nodes():
        for key, value in Pos.items():
            if n == list(key)[0]:
                g1.node[n]['pos'] = [value[0], value[1]]
        for key, value in Color.items():
            if n == list(key)[0]:
                g1.node[n]['color'] = [value[0], value[1], value[2]]
        for key, value in Layer.items():
            if n == list(key)[0]:
                g1.node[n]['layer'] = value[n]
        for key, value in Branch.items():
            if n == list(key)[0]:
                g1.node[n]['branch'] = value[n]
        for key, value in Type.items():
            if n == list(key)[0]:
                g1.node[n]['type'] = value[n]
                
    return g1
    

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
