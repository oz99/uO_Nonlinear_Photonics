from functools import partial
# from pydantic import validate_call
import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
from shapely.geometry.polygon import Polygon
import shapely as sp

PDK = get_generic_pdk()
PDK.activate()

## Note units are in nm.

#meta = gf.read.import_gds('c:\\UO\\Git_dump\\uO_Nonlinear_Photonics\\Fabrication\\Metasurfaces\\gdsii\\metasurface.gds')
dose = gf.read.import_gds('c:\\users\\test\\Proximity_correction_array.gds') 
father_component = gf.Component("father_component")

dose_ref = father_component.add_ref(dose)

dose_ref1 = father_component.add_ref(dose)
dose_ref2 = father_component.add_ref(dose)
dose_ref3 = father_component.add_ref(dose)


dose_ref.move((10000,10000))
dose_ref1.move((34000,10000))


dose_ref2.move((10000,35000))

dose_ref3.move((34000,35000))

father_component.show()

gdspath = father_component.write_gds(f"Proximity_correction_dose_test.gds", precision=1e-9, unit=1e-9,with_metadata=True)

