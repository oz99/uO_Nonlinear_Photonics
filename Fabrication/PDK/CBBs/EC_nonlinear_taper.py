# Author: Ozan W. Oner
# email : ooner083@uottawa.ca
# 
# Title: Edge Coupler (EC) Nonlinear Taper
# Description: This script generates a smooth curved y-branch splitter with ports using gdsfactory and CubicSpline interpolation. Note that this device is intended for photonic applications.
#               In the field of sillicon photonics, namely sillicon-on-insulator (SOI), smooth splitter designs  
#               have prooven to have the highest efficiencies amongst splitter designs. Our goal is to generate GDSII 
#               files from this script in in which we can then simulate and optimize geometries using either meep or lumerical. 
#               You may ask why not just use lumerical's built in waveguide generator? The answer is twofold.
#               1. We want to be able to optimize the geometry using python scripts.
#               2. We want to easily Tape-Out. Tape-Out is the process of sending your design to a foundry to be fabricated.
#                   In our case, at the University of uOttawa, we will be using our in-house e-beam for lithography.
#               
#               To further understand the physics of this device. Please reference the following:
#               1. Optimized low-loss integrated photonics silicon-nitride Y-branch splitter: https://pubs.aip.org/aip/acp/article/1002090
#               2. MIT Photonic Games Y-splitter: https://s3.amazonaws.com/fip-4/Combiner/index.html
# Please note that all parameters are in microns. They are listed at the bottom of this code. Ensure that KLayout is open and that you have KLive plugin installed.

import gdsfactory as gf
import numpy as np
import argparse
import re
from scipy.interpolate import CubicSpline
import json   

def main(args):
    c = gf.Component("EC_nonlinear_taper")

    L = args.length
    sp_len = L
    device_name = 'EC_nonlinear_taper_Ozan'

    ## Please note we divide by 2 since the cubic spline function used to define the countour goes from origin to w and not from -w to w.
    w0 = args.w0/2
    w1 = args.w1/2
    w2 = args.w2/2
    w3 = args.w3/2
    w4 = args.w4/2
    w5 = args.w5/2
 
    # It is possible to add breakpoints of widths to achieve a specific structure.
    widths = [w0, w1, w2, w3, w4, w5]

    breakpoints = np.linspace(0, L, 6)
    
    # Heights for the upper and lower halves
    heights_upper = [w0, w1, w2, w3, w4, w5]
    heights_lower = [-w for w in heights_upper]

    # Cubic Spline interpolation for the upper and lower contours
    cs_upper = CubicSpline(breakpoints, heights_upper)
    cs_lower = CubicSpline(breakpoints, heights_lower)

    # Generate points along the waveguide
    x = np.linspace(0, L, 100)
    upper_contour = np.array([x, cs_upper(x)]).T
    lower_contour = np.array([x, cs_lower(x)]).T    
    lower_contour = np.flip(lower_contour, axis=0)
    entire_contour = np.concatenate((upper_contour, lower_contour), axis=0)

    ## Cross-Sections of Waveguides
    layer= (1,0)
    xs = gf.cross_section.cross_section(width=w0*2, offset=0, layer=layer)

    ## Define the Y-Splitter Componenent
    splitter = gf.Component("splitter")
    ## EC_nonlinear_taper
    e = gf.Component("polygon")
    e.add_polygon([*entire_contour], layer=layer)
    e.add_port(name="o1", center=[0, 0], width = w0, orientation=0, layer=layer, port_type='optical')
    e.add_port(name="o2", center=[L, 0], width = w5, orientation=0, layer=layer, port_type='optical')
    sp = c << e

    # Write Final GDS
    c.write_gds("EC_Nonlinear_Taper.gds")
    c.show()
    return c

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--length', type=float, default=2, help='Length of the y-spliter')
    parser.add_argument('--w0', type=float, default=0.2, help='Width at point 0, and for the In/Out Waveguides')
    parser.add_argument('--w1', type=float, default=0.3, help='Width at point 1')
    parser.add_argument('--w2', type=float, default=0.35, help='Width at point 2')
    parser.add_argument('--w3', type=float, default=0.4, help='Width at point 3')
    parser.add_argument('--w4', type=float, default=1.0, help='Width at point 4')
    parser.add_argument('--w5', type=float, default=2.1, help='Width at point 5')

    parser.add_argument('-NetlistNew', action='store_true', default=True, help='Set True to Activate (default: False)')
    args = parser.parse_args()
    main(args)