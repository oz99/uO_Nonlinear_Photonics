from functools import partial
# from pydantic import validate_call
import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
from shapely.geometry.polygon import Polygon
import shapely as sp
import argparse

PDK = get_generic_pdk()
PDK.activate()



def main(args):
    # Activating the generic PDK
    PDK = get_generic_pdk()
    PDK.activate()

    width = args.width
    length1 = args.length1
    layer = args.layer
    overdose = args.overdose
    underdose = args.underdose
    iteration_width = args.iteration_width
    MinWidth = args.MinWidth
    MaxWidth = args.MaxWidth

    c = gf.Component("L_shape_proximity_correction")
    #center = c << gf.components.rectangle(size=(length1, width), layer=layer)
    widths = []

    #number of waveguide steps will be determined

    steps = int((MaxWidth-MinWidth)/iteration_width)

    for i in range(0, steps):
        width = width + iteration_width


        rect = c << gf.components.rectangle(size=(length1, width), layer=layer)

        widths.append(width-(iteration_width/2)) 
        total_y = sum(widths)      
        rect.center = ([length1/2,total_y+(1000*i)])


        ## Add rectangles to all corners of the L shape
    rect1 = c << gf.components.rectangle(size=(overdose, overdose), layer=layer)
    rect2 = c << gf.components.rectangle(size=(overdose, overdose), layer=layer)
    rect3 = c << gf.components.rectangle(size=(overdose, overdose), layer=layer)
    rect4 = c << gf.components.rectangle(size=(overdose, overdose), layer=layer)
 

    rect1.center = ([0,0])
    rect2.center = ([0,width])
    rect3.center = ([length1,0])
    rect4.center = ([length1,width])
    
    # Save the component to a GDSII file with high precision
    #d.write_gds("L_meta_prox.gds",with_metadata=True)
    
    gdspath = c.write_gds("L_meta_prox.gds", precision=1e-9, unit=1e-9,with_metadata=True)

    # Display the GDSII file using gdsfactory's viewer
    gf.show(gdspath)

    # gf.write_gds("L_w_proximity.gds", with_metadata=True)

    ## Extract and Save Netlist [Connections, Instances, Placements, Ports, Name]
    #elems_yaml = c.get_netlist_yaml()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=500, help='Width of the waveguide')
    parser.add_argument('--length1', type=int, default=1000000, help='Length of the waveguide')
    parser.add_argument('--layer', type=int, default=1, help='Layer number for the L shape')
    parser.add_argument('--overdose', type=int, default=50, help='Overdose on 270 deg edges')
    parser.add_argument('--underdose', type=int, default=50, help='Underdose on 90 deg edges')
    parser.add_argument('--iteration_width', type=int, default=10, help='spacing between waveguides')
    parser.add_argument('--MinWidth', type=int, default=500, help='Minimum Width of the waveguide')
    parser.add_argument('--MaxWidth', type=int, default=800, help='Maximum Width of the waveguide')

    parser.add_argument('-NetlistNew', action='store_true', default=True, help='Set True to Activate (default: False)')
    args = parser.parse_args()
    main(args)

