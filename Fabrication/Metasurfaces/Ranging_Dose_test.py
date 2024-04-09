import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
import math

# Function to create an L-shaped structure with proximity correction
def prox_corr_L(len1, width1, len2, width2, sqr_l, x0, y0, layer):
    # y1 = y0 + len1
    # x2 = x0 + width1
    # y3 = y0 + width2 + sqr_l / 2
    # x4 = x2 - sqr_l / 2
    # y5 = y3 - sqr_l
    # x6 = x4 + sqr_l
    # y7 = y0 + width2
    # x8 = x0 + len2

    c = gf.components.L(width=0.08, size=(0.017, 0.016), layer=(1, 0))
    
    #vertices = [(x0, y0), (x0, y1), (x2, y1), (x2, y3), (x4, y3), (x4, y5), (x6, y5), (x6, y7), (x8, y7), (x8, y0)]

    #poly = gf.components.polygon(vertices=vertices, layer=layer)
    # square1 = gf.components.rectangle(size=(sqr_l, sqr_l), layer=layer, centered=True).move((x0, y0))
    # square2 = gf.components.rectangle(size=(sqr_l, sqr_l), layer=layer, centered=True).move((x0, y1))
    # square3 = gf.components.rectangle(size=(sqr_l, sqr_l), layer=layer, centered=True).move((x2, y1))
    # square4 = gf.components.rectangle(size=(sqr_l, sqr_l), layer=layer, centered=True).move((x8, y7))
    # square5 = gf.components.rectangle(size=(sqr_l, sqr_l), layer=layer, centered=True).move((x8, y0))

    cell = gf.Component()
    # cell.add_ref(poly)
    # cell.add_ref(square1)
    # cell.add_ref(square2)
    # cell.add_ref(square3)
    # cell.add_ref(square4)
    # cell.add_ref(square5)
    
    return cell

# Function to rotate coordinates
def rotate(angle, x, y):
    rad = math.radians(angle)  # Convert angle to radians for math functions
    rot_x = x * math.cos(rad) - y * math.sin(rad)
    rot_y = x * math.sin(rad) + y * math.cos(rad)
    
    return rot_x, rot_y

# Example parameters for the prox_corr_L function
len1 = 100
width1 = 50
len2 = 150
width2 = 75
sqr_l = 20
x0 = 0
y0 = 0
layer = (1, 0)  # GDSII layer number and datatype

# Generate the L-shaped structure
l_shape = prox_corr_L(len1, width1, len2, width2, sqr_l, x0, y0, layer)

# Save the structure as a GDS file
l_shape.write_gds('L_shape_with_proximity_correction.gds')

# To visualize the structure in KLayout, open the GDS file in KLayout
# You can do this by running KLayout and opening the file manually,
# or by using a command line if available: `klayout L_shape_with_proximity_correction.gds`

l_shape.show()