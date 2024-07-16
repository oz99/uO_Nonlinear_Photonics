# Author: Ozan W. Oner
# email : ooner083@uottawa.ca
# 
# Title: Photonic Y-branch splitter 
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
    c = gf.Component("YSplitter")


    L = args.length
    s = args.s

    sp_len = L
    str_len = args.straightlength
    len = str_len
    rad = args.radius
    a = 0.75056
    rad2 = rad * a
    device_name = 'Ysplitter_Ozan'


    ## Please note we divide by 2 since the cubic spline function used to define the countour goes from origin to w and not from -w to w.
    w0 = args.w0/2
    w1 = args.w1/2
    w2 = args.w2/2
    w3 = args.w3/2
    w4 = args.w4/2
    w5 = args.w5/2
 
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

    ## Cross-Sections of Waveguides
    layer= (1,0)
    xs = gf.cross_section.cross_section(width=w0*2, offset=0, layer=layer)

    ## Define In/Out Waveguides for S-bend Waveguide
    portsName=['o1','o2','o3']

    a = gf.Component(portsName[0])
    a.add_polygon([(0, str_len, str_len, 0), (-w0, -w0, w0, w0)], layer=layer) ## Something here changed in the most current GDSfactory update making this line of code invalid
    a.add_port(name="o1", center=[str_len-str_len, w0-w0], width = w0, orientation=0, layer=layer, port_type='optical')
    a.add_port(name="o2", center=[str_len, w0-w0], width = w0, orientation=180, layer=layer, port_type='optical')
    a.info['width'] = float(w0)
    a.info['length'] = float(str_len)
    wg_in = c << a 

    b = gf.Component(portsName[1])
    b.add_polygon([(str_len+len+sp_len+rad+rad, str_len+len+sp_len+rad+rad+str_len, str_len+len+sp_len+rad+rad+str_len, str_len+len+sp_len+rad+rad), (-w0, -w0, w0, w0)], layer=layer)
    b.add_port(name="o1", center=[str_len+len+sp_len+rad+rad, 0], width = w0/2, orientation=180, layer=layer, port_type='optical')
    b.add_port(name="o2", center=[str_len+len+sp_len+rad+rad+str_len, 0], width = w0/2, orientation=0, layer=layer, port_type='optical')
    b.info['width'] = float(w0)
    b.info['length'] = float(str_len)
    wg_out1 = c << b

    d = gf.Component(portsName[2])
    d.add_polygon([(str_len+len+sp_len+rad+rad, str_len+len+sp_len+rad+rad+str_len, str_len+len+sp_len+rad+rad+str_len, str_len+len+sp_len+rad+rad), (-w0, -w0, w0, w0)], layer=layer)
    d.add_port(name="o1", center=[str_len+len+sp_len+rad+rad, 0], width = w0/2, orientation=180, layer=layer, port_type='optical')
    d.add_port(name="o2", center=[str_len+len+sp_len+rad+rad+str_len, 0], width = w0/2, orientation=0, layer=layer, port_type='optical')
    d.info['width'] = float(w0)
    d.info['length'] = float(str_len)
    wg_out2 = c << d

    ## Define the Y-Splitter Componenent
    splitter = gf.Component("splitter")

    # Straight Input Waveguide
    f = gf.Component("StraightWG")
    f.add_polygon([(str_len, str_len+len, str_len+len, str_len), (-(w0), -(w0), (w0), (w0))], layer=layer)
    f.add_port(name="o1", center=[str_len, 0], width = w5, orientation=0, layer=layer, port_type='optical')
    f.add_port(name="o2", center=[str_len+len, 0], width = w5, orientation=180, layer=layer, port_type='optical')
    f.info['width'] = float(w5)
    f.info['length'] = float(str_len)
    wg_str = splitter << f
    wg_str.connect("o1", wg_in.ports["o2"])

    ## Curved Y-Splitter
    e = gf.Component("polygon")
    e.add_polygon([*upper_contour, *reversed(lower_contour)], layer=layer)
    e.add_port(name="o1", center=[0, w0-w0], width = w0, orientation=0, layer=layer, port_type='optical')
    e.add_port(name="o2", center=[L, (s/2+w0)], width = w0, orientation=0, layer=layer, port_type='optical')
    e.add_port(name="o3", center=[L, -(s/2+w0)], width = w0, orientation=0, layer=layer, port_type='optical')
    sp = splitter << e
    sp.connect("o1", wg_str.ports["o2"])

    ## Define Bend Eulers to form S-Bend
    p1 = gf.path.euler(radius=rad, angle=45, p=0.5, use_eff=False)
    p2 = gf.path.euler(radius=rad, angle=-45, p=0.5, use_eff=False)
    p_top = p1 + p2
    total_p_top = p_top.extrude(xs)
    sbend_top = splitter << total_p_top
    sbend_top.info['width'] = float(w5)
    sbend_top.info['radius'] = float(rad)
    sbend_top.connect("o1", sp.ports["o2"])

    p3 = gf.path.euler(radius=rad, angle=-45, p=0.5, use_eff=False)
    p4 = gf.path.euler(radius=rad, angle=45, p=0.5, use_eff=False)
    p_bot = p3 + p4
    total_p_bot = p_bot.extrude(xs)
    sbend_bot = splitter << total_p_bot
    sbend_bot.info['width'] = float(w0)
    sbend_bot.info['radius'] = float(rad)
    sbend_bot.connect("o1", sp.ports["o3"])

    wg_out1.connect("o1", sbend_top.ports["o2"])
    wg_out2.connect("o1", sbend_bot.ports["o2"])

    splitter.add_port(name="o1", center=[str_len, 0], width = w0, orientation=0, layer=layer, port_type='optical')
    splitter.add_port(name="o2", center=[str_len+len+sp_len+rad+rad, s/2+2*rad+w0/2], width = w0, orientation=0, layer=layer, port_type='optical')
    splitter.add_port(name="o3", center=[str_len+len+sp_len+rad+rad, -(s/2+2*rad+w0/2)], width = w0, orientation=0, layer=layer, port_type='optical')
    x = c << splitter

    x.connect("o1", wg_in.ports["o2"])
    
    #x.connect("o2", wg_out1.ports["o1"])
    #x.connect("o3", wg_out2.ports["o1"])

    x.info['width'] = float(w0)
    x.info['radius'] = float(rad)

    c.add_port(portsName[0], port=wg_in.ports["o1"])
    c.add_port(portsName[1], port=wg_out1.ports["o2"])
    c.add_port(portsName[2], port=wg_out2.ports["o2"])

    # Write Final GDS
    c.write_gds("Ysplitter_test.gds", with_metadata=True)

    c.show()

    ## Extract and Save Netlist [Connections, Instances, Placements, Ports, Name]
    elems_yaml = c.get_netlist_yaml()

    #not enough elements included in output netlist
    #f = open("Netlist_Y-Splitter_test.yml", "w0")
    # f.write(elems_yaml)
    #f.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--length', type=float, default=2, help='Length of the y-spliter')
    parser.add_argument('--w0', type=float, default=0.59, help='Width at point 0, and for the In/Out Waveguides')
    parser.add_argument('--w1', type=float, default=1.2, help='Width at point 1')
    parser.add_argument('--w2', type=float, default=1.8, help='Width at point 2')
    parser.add_argument('--w3', type=float, default=1.7, help='Width at point 3')
    parser.add_argument('--w4', type=float, default=1.5, help='Width at point 4')
    parser.add_argument('--w5', type=float, default=1.4, help='Width at point 5')
    parser.add_argument('--s', type=float, default=0.2, help='Width of the split between the output splitter arms')
    ### Important - Ensure to confirm that w5 and s are optimized to minimize material outside of the s-bend (i.e. there is only a material gap in the middle)

    parser.add_argument('-straightlength', type=float, default=2, help='Length of the Straight In/Out Waveguides (default: 5 um)')
    parser.add_argument('-radius', type=float, default=2, help='Radius of the Bend Section (default: 2 um)')

    parser.add_argument('-NetlistNew', action='store_true', default=True, help='Set True to Activate (default: False)')
    args = parser.parse_args()
    main(args)