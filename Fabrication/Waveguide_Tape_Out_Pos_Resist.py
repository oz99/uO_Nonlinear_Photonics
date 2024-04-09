from functools import partial
# from pydantic import validate_call
import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
from shapely.geometry.polygon import Polygon
import shapely as sp

PDK = get_generic_pdk()
PDK.activate()

@gf.cell
def align_mark_unit():
    c = gf.Component()
    center = c << gf.components.cross(length=15, width=1, layer=(2, 0)) # central cross
    # create references for the rectangles at the tips of the cross:
    rect1 = c << gf.components.rectangle(size=(20, 5), layer=(2, 0))
    rect2 = c << gf.components.rectangle(size=(20, 5), layer=(2, 0))
    rect3 = c << gf.components.rectangle(size=(20, 5), layer=(2, 0))
    rect4 = c << gf.components.rectangle(size=(20, 5), layer=(2, 0))
    # position rectangles:
    rect1.center = center.center
    rect2.center = center.center
    rect3.center = center.center
    rect4.center = center.center
    rect1.xmin = center.xmax
    rect2.rotate(90).ymax = center.ymin
    rect3.xmax = center.xmin
    rect4.rotate(90).ymin = center.ymax

    ##Add smaller alignment marks at the edge of the reference cross. Up to 100nm size. Expose these at 10kV.add
    # Burn dot in center and conduct WFA in there.

    #Create Write-Field-Alignment Marks at the edge of the reference cross
    rect5 = c << gf.components.rectangle(size=(30, 2.5), layer=(61, 0))
    rect6 = c << gf.components.rectangle(size=(30, 2.5), layer=(61, 0))
    # position write field alignment marks

    ## Align the following two marks so they are in the top right of each alignment mark
    rect6.rotate(90).ymax = center.ymax
    rect6.move([27,17])
    rect5.center = (rect6.xmin, rect6.ymax)
    rect5.move((rect6.xmin - rect5.xmax, rect6.ymax - rect5.ymin))




    #rect5.center = center.center
    #rect5.xmax = center.xmax
    #rect6.center = center.center
    # rect6.rotate(90).ymax = center.ymax


    # L shape structure at the edge
    L_shape = c << gf.components.L(width=40, size=(220, 220), layer=(2, 0))
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

    am5 = c << align_mark_unit()
    am6 = c << align_mark_unit()

    # am5.move([side, 0])
    # am6.move([0, side])
    return c


am = align_mark(500)

meta = gf.read.import_gds('c:\\UO\\Git_dump\\uO_Nonlinear_Photonics\\Fabrication\\Metasurfaces\\metasurface.gds')

parent_component = gf.Component("parent_layout")

am_ref = parent_component.add_ref(am)
my_gds_ref = parent_component.add_ref(meta)

# Optionally, position the components
am_ref.move((0, 0))  # Position of am component, change as needed
my_gds_ref.move((50, 50)) #my_gds_ref.move((50, 50))  # Position of my_gds component, change as needed

parent_component.show()

