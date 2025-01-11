#test

import pathlib
from functools import partial

import pytest
from pytest_regressions.data_regression import DataRegressionFixture

import gdsfactory as gf
from gdsfactory.difftest import difftest
from gdsfactory.technology import (
    LayerMap,
)
from gdsfactory.typings import Layer

nm = 1e-3

class LayerMapDemo(LayerMap):
    WG: Layer = (1, 0)
    DEVREC: Layer = (68, 0)
    PORT: Layer = (1, 10)
    PORTE: Layer = (1, 11)
    LABEL_INSTANCES: Layer = (206, 0)
    LABEL_SETTINGS: Layer = (202, 0)
    LUMERICAL: Layer = (733, 0)
    M1: Layer = (41, 0)
    M2: Layer = (45, 0)
    M3: Layer = (49, 0)
    N: Layer = (20, 0)
    NP: Layer = (22, 0)
    NPP: Layer = (24, 0)
    OXIDE_ETCH: Layer = (6, 0)
    P: Layer = (21, 0)
    PDPP: Layer = (27, 0)
    PP: Layer = (23, 0)
    PPP: Layer = (25, 0)
    PinRec: Layer = (1, 10)
    PinRecM: Layer = (1, 11)
    SHALLOWETCH: Layer = (2, 6)
    SILICIDE: Layer = (39, 0)
    SIM_REGION: Layer = (100, 0)
    SITILES: Layer = (190, 0)
    SLAB150: Layer = (2, 0)
    SLAB150CLAD: Layer = (2, 9)
    SLAB90: Layer = (3, 0)
    SLAB90CLAD: Layer = (3, 1)
    SOURCE: Layer = (110, 0)
    TE: Layer = (203, 0)
    TEXT: Layer = (66, 0)
    TM: Layer = (204, 0)
    Text: Layer = (66, 0)
    VIA1: Layer = (44, 0)
    VIA2: Layer = (43, 0)
    VIAC: Layer = (40, 0)
    WGCLAD: Layer = (111, 0)
    WGN: Layer = (34, 0)
    WGclad_material: Layer = (36, 0)


LAYER = LayerMapDemo


# c = gf.Component()
# top = c << gf.components.nxn(north=8, south=0, east=0, west=0)
# bot = c << gf.components.nxn(north=2, south=2, east=2, west=2, xsize=10, ysize=10)
# top.dmovey(100)

# routes = gf.routing.route_bundle(
#     c,
#     ports1=bot.ports,
#     ports2=top.ports,
#     radius=5,
#     sort_ports=True,
# )



# c = gf.Component()
# c.add_polygon([(-8, -6), (6, 8), (7, 17), (9, 5)], layer=(1, 0))

# c.show()

def mmi1x2(width_mmi: float = 9, **kwargs) -> gf.Component:
    c = gf.components.mmi1x2(width_mmi=width_mmi)
    return c


def mmi2x2(width_mmi: float = 9, **kwargs) -> gf.Component:
    c = gf.components.mmi2x2(width_mmi=width_mmi)
    return c

cells = dict(mmi1x2=mmi1x2, mmi2x2=mmi2x2)


from gdsfactory.generic_tech import get_generic_pdk

generic_pdk = get_generic_pdk()

pdk1 = gf.Pdk(
    name="fab1",
    layers=LAYER,
    cells=cells,
    layer_views=generic_pdk.layer_views,
)
pdk1.activate()



c = pdk1.get_component(dict(component="mmi1x2", settings=dict(length_mmi=10)))
c.plot()