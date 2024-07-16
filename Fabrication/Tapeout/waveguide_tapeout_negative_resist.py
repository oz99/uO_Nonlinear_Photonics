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


    length1 = args.length1
    layer = args.layer

    iteration_width = args.iteration_width
    MinWidth = args.MinWidth
    MaxWidth = args.MaxWidth
    wall_width = args.wall_width

    c = gf.Component("waveguide_tapeout_negative_resist")
    #center = c << gf.components.rectangle(size=(length1, width), layer=layer)
    widths = []

    #number of waveguide steps will be determined
    width = MinWidth-iteration_width
    steps = int((MaxWidth-MinWidth)/iteration_width)

    for i in range(0, steps+1):
        width = width + iteration_width

        c1 = c << gf.components.rectangle(size=(length1, width), layer=layer)
        
        c1.name = f"waveguide_{width}_nm"

        widths.append(width-(iteration_width/2)) 
        total_y = sum(widths)      
        c1.center = ([length1/2,total_y+(1000*i)])

        

        #waveguide = c << c1


 
        ## Add rectangles to all corners of the L shape

    # Save the component to a GDSII file with high precision
    #d.write_gds("L_meta_prox.gds",with_metadata=True)
    
    gdspath = c.write_gds("waveguide_tapeout_negative_resist.gds", precision=1e-9, unit=1e-9,with_metadata=True)

    # Display the GDSII file using gdsfactory's viewer
    gf.show(gdspath)

    # gf.write_gds("L_w_proximity.gds", with_metadata=True)

    ## Extract and Save Netlist [Connections, Instances, Placements, Ports, Name]
    #elems_yaml = c.get_netlist_yaml()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--iteration_width', type=int, default=100, help='spacing between waveguides')
    parser.add_argument('--MinWidth', type=int, default=500, help='Minimum Width of the waveguide')
    parser.add_argument('--MaxWidth', type=int, default=2000, help='Maximum Width of the waveguide')
    parser.add_argument('--wall-width', type=int, default=0, help='Maximum Width of the waveguide')

    parser.add_argument('--length1', type=int, default=1000000, help='Length of the waveguide')
    parser.add_argument('--layer', type=int, default=(1,0), help='Layer number for the L shape')

    parser.add_argument('-NetlistNew', action='store_true', default=True, help='Set True to Activate (default: False)')
    args = parser.parse_args()
    main(args)
