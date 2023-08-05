from __future__ import print_function
from termcolor import colored
from collections import defaultdict


import os
import sys
import json
import gdsyuna
import pyclipper
import numpy as np


def list_layout_cells(gds):
    """ List the Cells in the GDS layout. """

    gdsii = gdsyuna.GdsLibrary()
    gdsii.read_gds(gds, unit=1.0e-12)

    print ('\n  ' + '[' + colored('*', 'green', attrs=['bold']) + '] ', end='')
    print('Cell List:')
    for key, value in gdsii.cell_dict.items():
        print('      -> ' + key)


def convert_node_to_3d(layer):
    polygons = []
    for pl in layer:
        poly = [[float(y*10e-9) for y in x] for x in pl]
        for row in poly:
            row.append(0.0)
        polygons.append(poly)
    return polygons


def convert_node_to_2d(layer):
    um = 10e7

    layer = list(layer)
    del layer[2]

    layer[0] = layer[0] * um
    layer[1] = layer[1] * um

    return layer


def parameter_print(arguments):
    print ('\n  ' + '[' + colored('*', 'green', attrs=['bold']) + '] ', end='')
    print ('Parameters:')
    for key, value in arguments.items():
        print('      ' + str(key) + ' : ' + str(value))


def red_print(header):
    """ Main program header (Red) """
    print ('\n' + '[' + colored('*', 'red', attrs=['bold']) + '] ', end='')
    print(header)


def magenta_print(header):
    """ Python package header (Purple) """
    print ('\n' + '[' + colored('*', 'magenta', attrs=['bold']) + '] ', end='')
    print ('--- ' + header + ' ----------')


def green_print(header):
    """ Function header (Green) """
    print ('\n  ' + '[' + colored('*', 'green', attrs=['bold']) + '] ', end='')
    print(header)


def cyan_print(header):
    """ Function header (Green) """
    print ('\n[' + colored('*', 'cyan', attrs=['bold']) + '] ', end='')
    print(header)