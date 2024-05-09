from functools import partial
# from pydantic import validate_call
import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
from shapely.geometry.polygon import Polygon
import shapely as sp

PDK = get_generic_pdk()
PDK.activate()

### units are in nm

prox5nm = gf.read.import_gds('c:\\Users\\test\\L_meta_prox_corr_5nm.gds', read_metadata = True)
prox5nm.name = "L_meta_prox_corr_5nm"

prox10nm = gf.read.import_gds('c:\\Users\\test\\L_meta_prox_corr_10nm.gds', read_metadata = True)
prox10nm.name = "L_meta_prox_corr_10nm"

prox15nm = gf.read.import_gds('c:\\Users\\test\\L_meta_prox_corr_15nm.gds', read_metadata = True)
prox15nm.name = "L_meta_prox_corr_15nm"

prox20nm = gf.read.import_gds('c:\\Users\\test\\L_meta_prox_corr_20nm.gds', read_metadata = True)
prox20nm.name = "L_meta_prox_corr_20nm"

prox25nm = gf.read.import_gds('c:\\Users\\test\\L_meta_prox_corr_25nm.gds', read_metadata = True)
prox25nm.name = "L_meta_prox_corr_25nm"

prox30nm = gf.read.import_gds('c:\\Users\\test\\L_meta_prox_corr_30nm.gds', read_metadata = True)
prox30nm.name = "L_meta_prox_corr_30nm"

prox35nm = gf.read.import_gds('c:\\Users\\test\\L_meta_prox_corr_35nm.gds', read_metadata = True)
prox35nm.name = "L_meta_prox_corr_35nm"

prox40nm = gf.read.import_gds('c:\\Users\\test\\L_meta_prox_corr_40nm.gds', read_metadata = True)
prox40nm.name = "L_meta_prox_corr_40nm"

prox45nm = gf.read.import_gds('c:\\Users\\test\\L_meta_prox_corr_45nm.gds', read_metadata = True)
prox45nm.name = "L_meta_prox_corr_45nm"

prox50nm = gf.read.import_gds('c:\\Users\\test\\L_meta_prox_corr_50nm.gds', read_metadata = True)
prox50nm.name = "L_meta_prox_corr_50nm"

prox55nm = gf.read.import_gds('c:\\Users\\test\\L_meta_prox_corr_55nm.gds', read_metadata = True)
prox55nm.name = "L_meta_prox_corr_55nm"


prox60nm = gf.read.import_gds('c:\\Users\\test\\L_meta_prox_corr_60nm.gds', read_metadata = True)
prox60nm.name = "L_meta_prox_corr_60nm"

parent_component = gf.Component("parent_layout")


prox5nm_ref = parent_component.add_ref(prox5nm)
prox10nm_ref = parent_component.add_ref(prox10nm)
prox15nm_ref = parent_component.add_ref(prox15nm)
prox20nm_ref = parent_component.add_ref(prox20nm)
prox25nm_ref = parent_component.add_ref(prox25nm)
prox30nm_ref = parent_component.add_ref(prox30nm)
prox35nm_ref = parent_component.add_ref(prox35nm)
prox40nm_ref = parent_component.add_ref(prox40nm)
prox45nm_ref = parent_component.add_ref(prox45nm)
prox50nm_ref = parent_component.add_ref(prox50nm)
prox55nm_ref = parent_component.add_ref(prox55nm)
prox60nm_ref = parent_component.add_ref(prox60nm)

prox5nm_ref.move((0,0))
prox10nm_ref.move((300,0))
prox15nm_ref.move((600,0))
prox20nm_ref.move((900,0))
prox25nm_ref.move((1200,0))
prox30nm_ref.move((1500,0))
prox35nm_ref.move((1800,0))
prox40nm_ref.move((2100,0))
prox45nm_ref.move((2400,0))
prox50nm_ref.move((2700,0))
prox55nm_ref.move((3000,0))
prox60nm_ref.move((3300,0))

parent_component.show() 

gdspath = parent_component.write_gds(f"Proximity_correction_row.gds", precision=1e-9, unit=1e-9,with_metadata=True)