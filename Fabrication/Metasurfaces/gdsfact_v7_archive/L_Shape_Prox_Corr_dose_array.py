from functools import partial
# from pydantic import validate_call
import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
from shapely.geometry.polygon import Polygon
import shapely as sp

PDK = get_generic_pdk()
PDK.activate()

# Create a new component to hold the grid of rows and labels
array_component = gf.Component()

# Define the number of rows, the vertical spacing, and the starting letter
num_rows = 12
vertical_spacing = 500
start_letter = 65  # ASCII code for 'A'

prox_corr_row = {}

# Add rows of the component and labels, spaced apart vertically
for i in range(num_rows):

    ###The following will ensure that all rows imported will have a different cell name.
    ### This is needed as we want to assign varying dose factors to each row
    ### This is what makes a varying dose test!

    prox_corr_row_file = gf.read.import_gds('c:\\Users\\test\\Proximity_correction_row.gds', read_metadata=True)
    prox_corr_row_file = prox_corr_row_file.flatten()
    prox_corr_row_file.name = f"Proximity_corr_row_{i}"
    prox_corr_row[i] = gf.Component(f"Proximity_correction_row_{i}")
    prox_corr_row[i].add_ref(prox_corr_row_file)
    #prox_corr_row[i] = prox_corr_row[i].flatten()
    prox_corr_row[i] = array_component << prox_corr_row[i]
    prox_corr_row[i].movey(i * vertical_spacing)

    # Add the label
    label = array_component << gf.components.text(
        text=chr(start_letter + i),  # Convert ASCII code to character
        size=150,  # Set the size of the text
        #layer=gf.LAYER.TEXT
    )
    # Position the label to the left of the row
    label.x =  prox_corr_row[i].xmin - 200  # Adjust x position based on your layout needs
    label.y =  prox_corr_row[i].ymax - 100  # Adjust y position based on your layout needs


############################################################################


@gf.cell
def align_mark_unit():
    c = gf.Component()

    # L shape structure at the edge
    L_shape = c << gf.components.L(width=500, size=(2000, 2000), layer=(2, 0))
    L_shape.move([-130, -130])
    return c

@gf.cell
def align_mark(side):
    c = gf.Component()
    am1 = c << align_mark_unit()
    am2 = c << align_mark_unit()
    am3 = c << align_mark_unit()
    am4 = c << align_mark_unit()

    am2.mirror().movex(0, side)
    am3.rotate(180).move([side, side])
    am4.mirror_y().movey(0, side)

    # am5 = c << align_mark_unit()
    # am6 = c << align_mark_unit()

    # am5.move([side, 0])
    # am6.move([0, side])
    return c


am = align_mark(8000)


am_ref = array_component.add_ref(am)


# Optionally, position the components
am_ref.move((-2500, -1000))  # Position of am component, change as needed




##########################################
array_component.name = "L_shape_dose_test"
# Show the complete array of components
array_component.show()

gdspath = array_component.write_gds(f"Proximity_correction_array.gds", precision=1e-9, unit=1e-9,with_metadata=True)

# prox_corr_row.show()