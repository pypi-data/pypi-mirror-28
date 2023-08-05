"""
    Hacker: 1h3d*n
    For: Volundr
    Docs: Algorithm 1
    Date: 31 April 2017

    Description: Write the gmsh file for meshing.

    --> Layer 80 is the wire layer difference from
        the moat layer.
    --> Layer 71 is the via layer union with the
        wire layer.
    --> Layer 70 is the moat layer union with the
        wire layer.
"""


from auron import tools
from collections import defaultdict

import meshio
import numpy as np
import pygmsh as pg


def check_terminal_duplicates(edgelabels):
    duplicates = defaultdict(list)
    
    for i, item in enumerate(edgelabels):
        duplicates[item].append(i)
    
    duplicates = {k:v for k, v in duplicates.items() if len(v) > 1}
                    
    for key, value in duplicates.items():
        if key is not None:
            if len(value) > 1:
                raise('Terminal duplicates!')


class Mesh:
    """  """
    
    def __init__(self):
        self.points = None
        self.cells = None
        self.point_data = None
        self.cell_data = None
        self.field_data = None

    def create_wireset_mesh(self, Layers, gds, wire):
        """  """

        geom = pg.built_in.Geometry()

        name = str(Layers[str(gds)]['name'])
        polygon = np.array(wire).tolist()
        layerpoly = tools.convert_node_to_3d(polygon)
        
        for i, poly in enumerate(layerpoly):
            polyname = name + '_' + str(i)
            
            layer = geom.add_polygon(poly, lcar=100, make_surface=True)
            # geom.extrude(layer, translation_axis=[0, 0, 350e-5])
            # for i in range(len(wires.edgelabels)):
            #     edge = wires.edgelabels[i]
            #     geom.add_physical_line(layer.line_loop.lines[i], label=edge)
            geom.add_physical_surface(layer.surface, label=polyname)

        geom.add_raw_code('Mesh.Algorithm = 100;')
        geom.add_raw_code('Coherence Mesh;')
        # geom.add_raw_code('Mesh 3;')
        
        meshdata = pg.generate_mesh(geom, verbose=False, num_lloyd_steps=0, prune_vertices=False)
        
        self.points = meshdata[0]
        self.cells = meshdata[1]
        self.point_data = meshdata[2]
        self.cell_data = meshdata[3]
        self.field_data = meshdata[4]
        
        meshio.write(name + '.msh', self.points, self.cells)

    #         print('\ncells')
    #         print(self.cells)
    #         print('\ncell_data')
    #         print(self.cell_data)
    #         print('\npoint_data')
    #         print(self.point_data)
    #         print('\nfield_data')
    #         print(self.field_data)

        
        
        
        
        
        
        
        
        
        
        
