from functools import partial
# from pydantic import validate_call
import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
from shapely.geometry.polygon import Polygon
import shapely as sp

PDK = get_generic_pdk()
PDK.activate()

## Note units are in nm.

@gf.cell
def align_mark_unit():
    c = gf.Component()


    # L shape structure at the edge
    L_shape = c << gf.components.L(width=1000, size=(4000, 4000), layer=(2, 0))
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



@gf.cell
def circ():
    c = gf.Component()
    # L shape structure at the edge
    circle_shape = c << gf.components.circle(radius=20, layer=(1, 0))
    return c

@gf.cell
def beam_circ(spacing, number_of_circles):
    c = gf.Component()
    
    for i in range(number_of_circles):
        circle = c << circ()
        circle.move([(i + 1) * spacing, 0])
    return c


circ = beam_circ(1000,20)



am = align_mark(130000)

#meta = gf.read.import_gds('c:\\UO\\Git_dump\\uO_Nonlinear_Photonics\\Fabrication\\Metasurfaces\\gdsii\\metasurface.gds')
dose = gf.read.import_gds('c:\\users\\test\\waveguide_tapeout_pos_resist.gds') 
father_component = gf.Component("father_component")

circ_ref = father_component.add_ref(circ)
circ_ref.move((0,65000))

circ_ref1 = father_component.add_ref(circ)
circ_ref1.move((100000,65000))

circ_ref2 = father_component.add_ref(circ)
circ_ref2.rotate(90)
circ_ref2.move((65000,0))


circ_ref3 = father_component.add_ref(circ)
circ_ref3.rotate(90)
circ_ref3.move((65000,100000))



am_ref = father_component.add_ref(am)
am_ref.move((0,0))

dose_ref = father_component.add_ref(dose)
dose_ref1 = father_component.add_ref(dose)
dose_ref2 = father_component.add_ref(dose)
dose_ref3 = father_component.add_ref(dose)


dose_ref.move((0,10000))
dose_ref1.move((0, 70000))
dose_ref2.move((0,120000))
dose_ref3.move((0,180000))

# father_component.move((1000,1000))

father_component.show()

gdspath = father_component.write_gds(f"WG_dose_test_pos_resist.gds", precision=1e-9, unit=1e-9,with_metadata=True)

