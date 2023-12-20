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
    rect1 = c << gf.components.rectangle(size=(20, 5), layer=(1, 0))
    rect2 = c << gf.components.rectangle(size=(20, 5), layer=(1, 0))
    rect3 = c << gf.components.rectangle(size=(20, 5), layer=(1, 0))
    rect4 = c << gf.components.rectangle(size=(20, 5), layer=(1, 0))
    # position rectangles:
    rect1.center = center.center
    rect2.center = center.center
    rect3.center = center.center
    rect4.center = center.center
    rect1.xmin = center.xmax
    rect2.rotate(90).ymax = center.ymin
    rect3.xmax = center.xmin
    rect4.rotate(90).ymin = center.ymax
    # L shape structure at the edge
    L_shape = c << gf.components.L(width=40, size=(220, 220), layer=(1, 0))
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
    return c

am = align_mark(500)

am.show()

#am.write_gds("alignment_marks.gds")
