
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

    columns = args.columns
    rows = args.rows
    spacing = args.spacing
    
    c = gf.Component("L_shape_proximity_correction")
    center = c << gf.components.L(width=width, size=(length1-width/2, length2-width/2), layer=layer)

    #removes 90 edges for underexposure
    rect6 = c << gf.components.rectangle(size=(underdose, underdose), layer=layer)
    rect6.dcenter = ([width/2, width/2])


    ## create a boolean between the current shape and rect 6
    # new = c.flatten()


    d = gf.Component("L_shape_proximity_correction_")
    final =  d << gf.boolean(c, rect6, operation="xor")

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

    final.drotate(90)
    rect1.drotate(90) 
    rect2.drotate(90)
    rect3.drotate(90)
    rect4.drotate(90)
    rect5.drotate(90)


    ## Create a few lines of code that copies the d component and rotates it 90 degrees as a specified location
    # e

    array_unit_cell = gf.Component("L_shape_proximity_correction_array_unit_cell")

    d1 = array_unit_cell << gf.Component.copy(d)

    

    d2 = array_unit_cell << gf.Component.copy(d)
    d2.drotate(-45)
    d2.move([0, 1])

    d3 = array_unit_cell << gf.Component.copy(d)
    d3.drotate(135)
    d3.move([1, 1+width])
 

    d4 = array_unit_cell << gf.Component.copy(d)
    d4.mirror()
    d4.move([1, 0])

    e = gf.Component("L_shape_proximity_correction_array")

    r1 = e.add_ref(component=array_unit_cell,
        name="L_shape_proximity_correction_array_unit_cell",
        spacing=spacing,
        columns=columns,
        rows=rows)

        
  
    # Save the component to a GDSII file with high precision
    #d.write_gds("L_meta_prox.gds",with_metadata=True)
    gdspath = e.write_gds(f"L_meta_prox_corr_{overdose}um.gds",with_metadata=True)

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
    parser.add_argument('--overdose', type=int, default=16/1000, help='Overdose on 270 deg edges')
    parser.add_argument('--underdose', type=int, default=16/1000, help='Underdose on 90 deg edges')
    
    # The following parameters determine the size of the array. Note that changes need to be made to pass information regarding the unit cell.
    parser.add_argument('--columns', type=int, default=400, help='Number of rows')
    parser.add_argument('--rows', type=int, default=400, help='Number of columns')
    parser.add_argument('--spacing', type=int, default=(2,2), help='spacing between the unit cells in um. (x, y)')
    
    parser.add_argument('-NetlistNew', action='store_true', default=True, help='Set True to Activate (default: False)')
    args = parser.parse_args()
    main(args)
