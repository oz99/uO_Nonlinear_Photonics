
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

def create_L_shape(width, length1, length2, layer):
    """
    Creates an L-shaped component using gdsfactory with specified parameters.

    Parameters:
    - width: Width of the L shape's arms.
    - length1: Length of the first arm of the L shape.
    - length2: Length of the second arm of the L shape.
    - layer: The layer on which to draw the L shape.

    Returns:
    - A gdsfactory component with the specified L shape.
    """
    # Create an L-shaped component
    c = gf.components.L(width=width, size=(length1, length2), layer=layer)
    return c

def main(args):
    # Activating the generic PDK
    PDK = get_generic_pdk()
    PDK.activate()

    # Create the L shape with parameters from args
    l_shape_component = create_L_shape(width=args.width, length1=args.length1, length2=args.length2, layer=(args.layer, 0))
    
    # Save the component to a GDSII file with high precision
    gdspath = l_shape_component.write_gds(precision=1e-9, unit=1e-9)
    
    # Display the GDSII file using gdsfactory's viewer
    gf.show(gdspath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=80, help='Width of the L shape\'s arms')
    parser.add_argument('--length1', type=int, default=170, help='Length of the first arm of the L shape')
    parser.add_argument('--length2', type=int, default=160, help='Length of the second arm of the L shape')
    parser.add_argument('--layer', type=int, default=1, help='Layer number for the L shape')
    
    args = parser.parse_args()
    main(args)
