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

    length1 = args.length1
    layer = args.layer

    wg_width = args.wg_width
    wall_width = args.wall_width
    num_wgs = args.num_wgs

    c = gf.Component("Waveguide_tapeout_positive_resist")
    #d = gf.Component("test")
    #center = c << gf.components.rectangle(size=(length1, width), layer=layer)
    widths = []

    #number of waveguide steps will be determined
    steps = num_wgs



    for i in range(0, steps+1):
        width = wg_width


        c1 = gf.components.rectangle(size=(length1, width), layer=layer).ref()
        
        c2 = gf.components.rectangle(size=(length1, width+wall_width), layer=layer).ref()
        #xor of the two above rectangles
        

        widths.append(width) 
        total_y = sum(widths)      
        c1.center = ([length1/2,total_y+(1000*i)]) ## This ensure all the waveguide are 1000nm apart
        c2.center = ([length1/2,total_y+(1000*i)])

        c3 = gf.geometry.boolean(c1, c2, operation="xor")
        c3.name = f"waveguide_{width}_nm"
       
        waveguide = c << c3

        start_letter = 65  # ASCII code for 'A'
            # Add the label
        label = c << gf.components.text(
            text=chr(start_letter + i),  # Convert ASCII code to character
            size=500,  # Set the size of the text
            #layer=gf.LAYER.TEXT
        )
        # Position the label to the left of the row
        label.x =  -500  # Adjust x position based on your layout needs
        label.y =  total_y+(1000*i)  # Adjust y position based on your layout needs



        ## Add rectangles to all corners of the L shape

    # Save the component to a GDSII file with high precision
    #d.write_gds("L_meta_prox.gds",with_metadata=True)
    
    gdspath = c.write_gds("waveguide_tapeout_pos_resist.gds", precision=1e-9, unit=1e-9,with_metadata=True)

    # Display the GDSII file using gdsfactory's viewer
    gf.show(gdspath)

    # gf.write_gds("L_w_proximity.gds", with_metadata=True)

    ## Extract and Save Netlist [Connections, Instances, Placements, Ports, Name]
    #elems_yaml = c.get_netlist_yaml()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--wg_width', type=int, default=2000, help='Width of the waveguide')
    parser.add_argument('--wall-width', type=int, default=1000, help='Maximum Width of the waveguide')
    parser.add_argument('--num_wgs', type=int, default=15, help='number of waveguides to be made')
    parser.add_argument('--length1', type=int, default=600000, help='Length of the waveguide')
    parser.add_argument('--layer', type=int, default=(1,0), help='Layer number for the L shape')

    parser.add_argument('-NetlistNew', action='store_true', default=True, help='Set True to Activate (default: False)')
    args = parser.parse_args()
    main(args)

