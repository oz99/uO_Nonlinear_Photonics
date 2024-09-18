### This file generates a gdsfactory script of a subwavelength grating (SWG) edge coupler
### This work was inspired by the following publications 

### Authors: Ozan W. Oner and Garen Simpson
#### 

import gdsfactory as gf
import numpy as np
import argparse
import re
from scipy.interpolate import CubicSpline
import json   

def main(args):
    c = gf.Component("SWG_Edge_Coupler")

    min_feature_size = args.min_feature_size
    num_gratings = args.num_gratings
    initial_period = args.initial_period
    final_period = args.final_period
    initial_width = args.initial_width
    final_width = args.final_width
    initial_duty_cycle = args.initial_duty_cycle
    final_duty_cycle = args.final_duty_cycle
    tapering_length = args.tapering_length
    initial_y_span = args.initial_y_span
    final_y_span = args.final_y_span
    device_name = 'SWG_Edge_Coupler'

    layer= (1,0)
    counter = 0
    #portsName = [counter]
    portsName=['o1','o2']

    # Assuming num_gratings is already defined as a variable
    for i in range(int(num_gratings - (num_gratings * 0.1))):


        xpos = i * initial_period   # Positioning each grating element based on the initial period

        # Calculate the taper ratio based on the manual tapering length

        taper_ratio = xpos / tapering_length;  # Ratio within the tapering length

        # Calculate the taper ratio based on the position
        taper_ratio = i / (num_gratings-1)
        
        # Taper the period
        current_period = initial_period * (1 - taper_ratio) + final_period * taper_ratio
        
        # Taper the duty cycle
        current_duty_cycle = initial_duty_cycle * (1 - taper_ratio) + final_duty_cycle * taper_ratio
        
        # Calculate the width of the current grating element
        current_width = current_duty_cycle * current_period

        # Taper the grating width independently of the duty cycle
        actual_width = initial_width * (1 - taper_ratio) + final_width * taper_ratio
        
        # Taper the y span (height)
        current_y_span = initial_y_span * (1 - taper_ratio) + final_y_span * taper_ratio
    
        # Calculate the gap between this segment and the next
        current_gap = current_period - current_width
        
        
        print([i])        
        portsName.append(counter)

        name = counter
        
        
        # a = gf.Component(portsName[0])
        # a.add_polygon([(xpos + current_width / 2, current_y_span), (-xpos - current_width / 2, current_y_span),
        #                 (xpos + current_width / 2, -current_y_span), -(xpos + current_width / 2, current_y_span)],Layer=layer)
        
        # add references
        a = gf.Component()    
        a.add_polygon([(xpos - current_width / 2, current_y_span), (xpos - current_width / 2, -current_y_span),
                        (xpos + current_width / 2, -current_y_span), (xpos + current_width / 2, current_y_span)],layer=layer)
    #    ref = SWG_Edge_Coupler.addref(a)
        counter += 1
        
       # a.add_polygon([(xpos + current_width / 2, current_y_span), (-xpos - current_width / 2, current_y_span), (xpos + current_width / 2, -current_y_span), -(xpos + current_width / 2, current_y_span)],Layer=layer)
        grating  = c << a
    a.add_port(name="o1", center=[-initial_width / 2, 0], width = initial_width, orientation=180, layer=layer, port_type='optical')

        #####################################################################
        # Linear taper

        #####################################################################

    b = gf.Component("WG_taper")  
    # b.add_polygon([( -tapering_length + xpos  + current_width/2, -min_feature_size),
    #             (-tapering_length + xpos  + current_width/2, min_feature_size),
    #             (xpos  + current_width/2 , final_y_span),
    #             (xpos  + current_width/2, -final_y_span)], layer=layer)
    b.add_polygon([(initial_width/2, -min_feature_size),
            (initial_width/2, min_feature_size),
            (xpos  + current_width/2 , final_y_span),
            (xpos  + current_width/2, -final_y_span)], layer=layer)
    WG  = c << b

    # ##############################################################
    # # Straight output waveguide 
    # ##############################################################

    d = gf.Component("output_WG")    
    # d.add_polygon([( grating_span + current_width/2, final_y_span),(grating_span + current_width / 2, -final_y_span),
    #                 (grating_span - current_width / 2, -final_y_span),
    #                 (grating_span - current_width / 2, final_y_span)],layer=layer)
    
    d.add_polygon([( grating_span + current_width/2, final_y_span),
                (grating_span + current_width / 2, -final_y_span),
                (xpos  + current_width/2 , -final_y_span),
                (xpos  + current_width/2, final_y_span)], layer=layer)
    d.add_port(name="o2", center=[grating_span + current_width/2, 0], width = final_y_span, orientation=0, layer=layer, port_type='optical')
    WG  = c << d
    
    c.add_port(portsName[0], port=a.ports["o1"])
    c.add_port(portsName[1], port=d.ports["o2"])

    c.write_gds("Ysplitter_test.gds")
    c.show()
    return c


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--min_feature_size', type=int, default=0.04, help='Minimum feature size, generally 40nm for our e-beam')
    parser.add_argument('--num_gratings', type=int, default=110, help='Number of grating elements')

    parser.add_argument('--initial_period', type=float, default=0.4, help='Initial period of the grating (e.g., 700 nm)')
    parser.add_argument('--final_period', type=float, default=0.267, help='Final period of the grating (e.g., 300 nm)')
    parser.add_argument('--initial_width', type=float, default=0.2, help='Initial width of the grating element (e.g., 350 nm)')
    parser.add_argument('--final_width', type=float, default=0.17, help='Final width of the grating element (e.g., 150 nm)')
    parser.add_argument('--initial_duty_cycle', type=float, default=0.5, help='Initial duty cycle (50% of the period)')
    parser.add_argument('--final_duty_cycle', type=float, default=0.6, help='Final duty cycle (80% of the period)')
    parser.add_argument('--tapering_length', type=float, default=35, help='Length over which tapering occurs (e.g., 10 microns)')
    parser.add_argument('--initial_y_span', type=float, default=0.2, help='Initial height of the grating element (e.g., 450 nm)')
    parser.add_argument('--final_y_span', type=float, default=0.45, help='Final height of the grating element (e.g., 250 nm)')
    parser.add_argument('--NetlistNew', action='store_true', default=True, help='Set True to Activate (default: False)')
    args = parser.parse_args()
    main(args)