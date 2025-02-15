
# import gdsfactory as gf
# from gdsfactory.generic_tech import get_generic_pdk
# import math

# PDK = get_generic_pdk()
# PDK.activate()



# # c = gf.Component()
# c = gf.components.L(width=80, size=(170, 160), layer=(1, 0))
# gdspath = c.write_gds(precision=1e-9, unit=1e-9)

# gf.show(gdspath)

import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
import argparse


def main(args):
    # Activating the generic PDK
    PDK = get_generic_pdk()
    PDK.activate()

    width = args.width
    length1 = args.length1
    length2 = args.length2
    layer = args.layer
    overdose = args.overdose
    underdose = args.underdose
    
    c = gf.Component("L_shape_proximity_correction")
    center = c << gf.components.L(width=width, size=(length1-width/2, length2-width/2), layer=layer)

    #removes 90 edges for underexposure
    rect6 = c << gf.components.rectangle(size=(underdose, underdose), layer=layer)
    rect6.dcenter = ([width/2, width/2])


    ## create a boolean between the current shape and rect 6
    # new = c.flatten()


    d = gf.Component("L_shape_proximity_correction1")
    final =  d << gf.boolean(c, rect6, operation="xor",layer=layer)

        ## Add rectangles to all corners of the L shape
    rect1 = d << gf.components.rectangle(size=(overdose, overdose), layer=layer)
    rect2 = d << gf.components.rectangle(size=(overdose, overdose), layer=layer)
    rect3 = d << gf.components.rectangle(size=(overdose, overdose), layer=layer)
    rect4 = d << gf.components.rectangle(size=(overdose, overdose), layer=layer)
    rect5 = d << gf.components.rectangle(size=(overdose, overdose), layer=layer)

    rect1.dcenter = ([-width/2,-width/2])
    rect2.dcenter = ([-width/2,length2-width/2])
    rect3.dcenter = ([length1-width/2,-width/2])
    rect4.dcenter = ([width/2,length2-width/2])
    rect5.dcenter = ([length1-width/2,width/2])

    final.drotate(45)
    rect1.drotate(45) 
    rect2.drotate(45)
    rect3.drotate(45)
    rect4.drotate(45)
    rect5.drotate(45)


    #     # Create an array of the copied cell
    # array = gf.components.array(
    #     component="L_shape_proximity_correction1",  # The component to array
    #     spacing=(0.5, 0.5),       # Spacing between cells (x, y)
    #     rows=500,                 # Number of rows
    #     columns=300               # Number of columns
    # )



    # Save the component to a GDSII file with high precision
    #d.write_gds("L_meta_prox.gds",with_metadata=True)
    gdspath = d.write_gds(f"L_meta_prox_corr_{overdose}um.gds",with_metadata=True)

    # Display the GDSII file using gdsfactory's viewer
    gf.show(gdspath)

    return

    # gf.write_gds("L_w_proximity.gds", with_metadata=True)

    ## Extract and Save Netlist [Connections, Instances, Placements, Ports, Name]
    #elems_yaml = c.get_netlist_yaml()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=80/1000, help='Width of the L shape\'s arms')
    parser.add_argument('--length1', type=int, default=170/1000, help='Length of the first arm of the L shape')
    parser.add_argument('--length2', type=int, default=160/1000, help='Length of the second arm of the L shape')
    parser.add_argument('--layer', type=int, default=(1,0), help='Layer number for the L shape')
    parser.add_argument('--overdose', type=int, default=15/1000, help='Overdose on 270 deg edges')
    parser.add_argument('--underdose', type=int, default=15/1000, help='Underdose on 90 deg edges')

    parser.add_argument('-NetlistNew', action='store_true', default=True, help='Set True to Activate (default: False)')
    args = parser.parse_args()
    main(args)
