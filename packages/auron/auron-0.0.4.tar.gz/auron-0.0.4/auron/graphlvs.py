from collections import defaultdict
from auron import tools
from itertools import count

import numpy as np
import networkx as nx
import pyclipper
import matplotlib.pyplot as plt


def update_adjacent_matrix(g, n1, adj_mat, v1, v2):
    if (adj_mat[v1][v2] != 0):
        n2 = adj_mat[v1][v2] - 1
        g.add_edge(n1, n2, key='none')
    else:
        adj_mat[v1][v2] = n1 + 1
        adj_mat[v2][v1] = n1 + 1


def create_edges(g, points, triangles):
    """
    Parameters
    ----------
    adjacent_matrix : nparray
        See which edges are connected through
        triangles. Save triangle id to which the
        edge exists.

    triangles : nparray
        Array containing the node ids of the 3
        vertices of the triangle.

    Notes
    -----
    * From triangles:
        tri --> [v1, v2, v3]
        edge --> 1-2, 2-3, 1-3

    Algorithm
    ---------
    * Loop through every triangle and its edges.
    * Save the triangle id in the adjacent_matrix
      with index of (v1, v2).
    """

    adjacent_matrix = np.zeros((len(points), len(points)), dtype=np.int8)

    for i, tri in enumerate(triangles):
        v1, v2, v3 = tri[0], tri[1], tri[2]
        
        update_adjacent_matrix(g, i, adjacent_matrix, v1, v2)
        update_adjacent_matrix(g, i, adjacent_matrix, v1, v3)
        update_adjacent_matrix(g, i, adjacent_matrix, v2, v3)
        
        
def center_nodes(g, points, triangles):
    """ Gets the center nodes of each triangle. """

    um = 10e6

    for n, tri in enumerate(triangles):
        n1, n2, n3 = points[tri[0]], points[tri[1]], points[tri[2]]

        sum_x = um*(n1[0] + n2[0] + n3[0]) / 3.0
        sum_y = um*(n1[1] + n2[1] + n3[1]) / 3.0
        sum_z = um*(n1[2] + n2[2] + n3[2]) / 3.0
        
        g.nodes[n]['vertex'] = tri
        g.nodes[n]['pos'] = [sum_x, sum_y]

        
def color_tuple(layer):
    colortuple = tuple(map(float, layer['color'].split(' ')))
    return tuple(x/255.0 for x in colortuple)


def check_branch(g, source, target):
    """ Check if the current edge is a branch, which 
    means it should not be filtered or if it is 
    a normal edge that should be filtered. """
    
    if source in g.neighbors(target):
        if g.edge[source[0]][target]['key'] == 'induct':
            source[0] = target


def is_inductance(g, path):
    masternodes = [1, 2, 3, 4, 5]
    for n in path:
        if g.node[n]['type'] in masternodes:
            return False
    return True
            
            
def does_path_exist(path, branches):
    be = [path[0], path[-1]]
    for bp in branches:
        if set(be).issubset(bp):
            return True
    return False

    
def update_branches(g, branches, path):
    if len(path) == 2:
        branches.append(path)
    else:
        if is_inductance(g, path[1:-1]):
            if not does_path_exist(path, branches):
                branches.append(path)
    

def get_branches(g, source, master):
    branches = list()
    targets = filter(lambda x: x not in [source], master)
    for target in targets:
        for path in nx.all_simple_paths(g, source=source, target=target):
            if (path[0] in master) or (path[-1] in master):
                update_branches(g, branches, path)
    return branches
    
    
def clean_subgraph(g, branches):
    """
    Variables
    ---------
        ix : bool
            Is the current path a true inductance/resistance path
    """
    remove = list()
    for n in g.nodes():
        ix_path = True 
        for key, branch in branches.items(): 
            if any(n in path for path in branch):
                ix_path = False
        if ix_path:
            remove.append(n)
    g.remove_nodes_from(remove)
    
        
class LayerGraph:
    """  """

    def __init__(self, gds, Layers, Params, cmesh, wires, labels):
        self.g = None

        self.gds = gds
        self.wires = wires
        self.labels = labels
        self.mesh = cmesh

        self.Branches = dict()
        self.Layers = Layers
        self.Params = Params
        
    def label_default_triangles(self, triangles, field_data):
        """ Every triangle is connected to a layer type
        in the layout. Each graph vertex represent 
        a triangle, thus we have to map the triangle
        layer properties to the specific graph vertex. """
        
        for n in self.g.nodes():
            cell_list = triangles['physical'].tolist()
            layerid = cell_list[n]
            
            self.g.node[n]['color'] = color_tuple(self.Layers['6'])
            self.g.node[n]['layer'] = 'null'
            self.g.node[n]['type'] = 0
            self.g.nodes[n]['branch'] = None
            
            for key, value in field_data.items():
                if layerid in value:
                    layername = key.split('_')[0]
                    for key, layer in self.Layers.items():
                        if layer['name'] == layername:
                            self.g.node[n]['type'] = 0
                            self.g.node[n]['layer'] = layername
                            self.g.node[n]['color'] = color_tuple(layer)

    def label_terminal_triangles(self, triangles):
        for n, tri in enumerate(triangles):
            points = self.mesh.points
            n1, n2, n3 = points[tri[0]], points[tri[1]], points[tri[2]]

            n1 = tools.convert_node_to_2d(n1)
            n2 = tools.convert_node_to_2d(n2)
            n3 = tools.convert_node_to_2d(n3)

            poly = [n1, n2, n3]

            for label in self.labels:
                if label.text[0] == 'P':
                    if pyclipper.PointInPolygon(label.position, poly) != 0:
                        self.g.node[n]['type'] = 2
                        self.g.node[n]['layer'] = label.text
                        self.g.node[n]['color'] = color_tuple(self.Params['TERM'])

    def label_via_triangles(self, triangles):
        # tools.green_print('Via labeling:')

        for n, tri in enumerate(triangles):
            points = self.mesh.points
            n1, n2, n3 = points[tri[0]], points[tri[1]], points[tri[2]]

            n1 = tools.convert_node_to_2d(n1)
            n2 = tools.convert_node_to_2d(n2)
            n3 = tools.convert_node_to_2d(n3)

            poly = [n1, n2, n3]
            
            for label in self.labels:
                if label.text[:3] == 'via':
                    point = label.position
                    if pyclipper.PointInPolygon(point, poly) != 0:
                        if label.text[-3:] == 'gnd':
                            self.g.node[n]['type'] = 4
                            self.g.node[n]['layer'] = label.text + '_' + str(label.texttype)
                            self.g.node[n]['color'] = color_tuple(self.Layers['32'])
                        else:
                            self.g.node[n]['type'] = 1
                            self.g.node[n]['layer'] = label.text + '_' + str(label.texttype)
                            self.g.node[n]['color'] = color_tuple(self.Layers['15'])
                            
    def label_jj_triangles(self, triangles):
        # tools.green_print('Via labeling:')
        
        for n, tri in enumerate(triangles):
            points = self.mesh.points
            n1, n2, n3 = points[tri[0]], points[tri[1]], points[tri[2]]

            n1 = tools.convert_node_to_2d(n1)
            n2 = tools.convert_node_to_2d(n2)
            n3 = tools.convert_node_to_2d(n3)

            poly = [n1, n2, n3]
            
            for label in self.labels:
                if label.text[:2] == 'jj':
                    point = label.position
                    if pyclipper.PointInPolygon(point, poly) != 0:
                        self.g.node[n]['type'] = 3
                        self.g.node[n]['layer'] = label.text + '_' + str(label.texttype)
                        self.g.node[n]['color'] = color_tuple(self.Layers['21'])
                        
    def label_user_triangles(self):
        """
        * Autodetect the usernodes, which are represented
          as the Green vertices on the graph.

        * Get the vertex with 3 neighbours, and the current
          vertex must be a wire vertex (COU or CTL) in this case.

        * Use the 'type' variable in the layer json object to
          see if the vertex is a layer or not.

        * Lastly, update the vertex_key property map
        """
    
        for n in self.g.nodes():
            if len([i for i in self.g.neighbors(n)]) > 2:
                self.g.node[n]['type'] = 5
                self.g.node[n]['color'] = color_tuple(self.Params['USER'])
                
                for i in self.g.neighbors(n):
                    if self.g.nodes[i]['type'] == 3:
                        self.g.node[n]['type'] = 3
                        self.g.node[n]['layer'] = self.g.node[i]['layer']
                        self.g.node[n]['color'] = color_tuple(self.Layers['21'])
    
    def label_branch_nodes(self):
        """  """
        for n in self.g.nodes():
            for key, branch in self.Branches.items(): 
                for x in [x for path in branch for x in path[1:-1]]:
                    if self.g.node[x]['branch'] is None:
                        self.g.node[x]['branch'] = key
                
    def create_graph(self):
        """  """

        self.g = nx.Graph()
        
        field_data = self.mesh.field_data
        triangle_data = self.mesh.cell_data['triangle']
        triangle_cells = self.mesh.cells['triangle']
        # line_cells = self.mesh.cells['line']

        create_edges(self.g, self.mesh.points, triangle_cells)
        center_nodes(self.g, self.mesh.points, triangle_cells)

        self.label_default_triangles(triangle_data, field_data)
        self.label_terminal_triangles(triangle_cells)
        self.label_via_triangles(triangle_cells)
        self.label_jj_triangles(triangle_cells)
        
    def ix_master(self, g, master, count):
        for source in master:
            ixb = get_branches(g, source, master)
            if ixb is not None:
                self.Branches[count[0]] = ixb
            count[0] += 1
    
    def gnd_master(self, master, count):
        self.Branches[count[0]] = [master]
        count[0] += 1
        
    def filter_subgraphs(self):
        """ Branch must have atleast 2 masternodes, otherwise just save 
        the masternode, master = get_master_nodes(sg) """
        
        masternodes = [1, 2, 3, 4, 5]
        sub_graphs = nx.connected_component_subgraphs(self.g, copy=True)
        
        count = [0]
        for sg in sub_graphs:
            master = [n for n in sg.nodes() if sg.node[n]['type'] in masternodes]
            
            if len(master) == 0:
                print('No masternodes found')
            elif len(master) == 1:
                self.gnd_master(master, count)
            else:
                self.ix_master(sg, master, count)
                
        for key, value in self.Branches.items():
            print(key, value)
                
        clean_subgraph(self.g, self.Branches)
        
    def filter_wire_nodes(self):
        for key, value in self.Branches.items():
            for branch in value:
                mtype = self.g.node[branch[0]]['type']
                mcolor = self.g.node[branch[0]]['color']
                mlabel = self.g.node[branch[0]]['layer']
                
                for n in branch:
                    if self.g.node[n]['type'] == 0:
                        self.g.node[n]['type'] = mtype
                        self.g.node[n]['color'] = mcolor
                        self.g.node[n]['layer'] = mlabel + '_' + str(self.g.node[n]['branch'])

    def draw_graph(self):
        pos = {n: self.g.nodes[n]['pos'] for n in self.g.nodes()}
        # labels = {n: n for n in self.g.nodes()}
        # labels = {n: self.g.node[n]['layer'] for n in self.g.nodes()}
        labels = {n: self.g.node[n]['branch'] for n in self.g.nodes()}
        colors = [self.g.node[n]['color'] for n in self.g.nodes()]
    
        nx.draw_networkx_edges(self.g, pos, edgelist=self.g.edges(), alpha=0.5, with_labels=True)
        nx.draw_networkx_nodes(self.g, pos, nodelist=self.g.nodes(), node_color=colors, node_size=600, cmap=plt.cm.jet)
        nx.draw_networkx_labels(self.g, pos, labels=labels, font_size=8)
    
        plt.show()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
