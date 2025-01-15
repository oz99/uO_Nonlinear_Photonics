from functools import partial
# from pydantic import validate_call
import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
from shapely.geometry.polygon import Polygon
import shapely as sp

PDK = get_generic_pdk()
PDK.activate()

### units are in nm

c = gf.Component()

test = gf.read.import_gds('c:\\Users\\test\\L_meta_prox_corr_0.015um.gds')

prox15nm = test.flatten()

prox15nm = gf.Component()

#prox15nm = gf.Component("Proximity_correction_row")

#prox15nm.dname = "L_meta_prox_corr_15nm"

#prox15nm = c << gf.read.import_gds('c:\\Users\\test\\L_meta_prox_corr_0.015um.gds')

#parent_component = gf.Component("parent_layout")

#prox15nm_ref = parent_component.add_ref(prox15nm)

#parent_component = parent_component.flatten()
#parent_component.name = "Proximity_correction_row"
gf.show(prox15nm)

gdspath = prox15nm.write_gds(f"Proximity_correction_row.gds",with_metadata=True)