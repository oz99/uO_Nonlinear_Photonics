import gdsfactory as gf
from gdsfactory.generic_tech.layer_map import LAYER
# from gdsfactory.technology import LogicalLayer

from gdsfactory.generic_tech.layer_stack import get_layer_stack

# layer_stack220 = get_layer_stack()

## Add some waveguides to the layer stack


# c = gf.c.straight_heater_doped_rib(length=100)

## Add a ring resonator waveguide beneath the structure above 
c = gf.c.ring_single()
c.show()



# c.show()

# e = gf.Component("L_shape_proximity_correction_array")

# r1 = e.add_ref(component=array_unit_cell,
#     name="L_shape_proximity_correction_array_unit_cell",
#     spacing=spacing,
#     columns=columns,
#     rows=rows)


# nm = 1e-3
# thickness_wg = 220 * nm
# thickness_slab_deep_etch = 90 * nm
# thickness_slab_shallow_etch = 150 * nm

# sidewall_angle_wg = 0
# layer_core = LogicalLayer(layer=LAYER.WG)
# layer_shallow_etch = LogicalLayer(layer=LAYER.SHALLOW_ETCH)
# layer_deep_etch = LogicalLayer(layer=LAYER.DEEP_ETCH)


# layers = {
#     "core": LayerLevel(
#         layer=layer_core - layer_deep_etch - layer_shallow_etch,
#         thickness=thickness_wg,
#         zmin=0.0,
#         material="si",
#         mesh_order=2,
#         sidewall_angle=sidewall_angle_wg,
#         width_to_z=0.5,
#         derived_layer=layer_core,
#     ),
#     "shallow_etch": LayerLevel(
#         layer=LogicalLayer(layer=LAYER.SHALLOW_ETCH),
#         thickness=thickness_wg - thickness_slab_shallow_etch,
#         zmin=0.0,
#         material="si",
#         mesh_order=1,
#         derived_layer=LogicalLayer(layer=LAYER.SLAB150),
#     ),
#     "deep_etch": LayerLevel(
#         layer=LogicalLayer(layer=LAYER.DEEP_ETCH),
#         thickness=thickness_wg - thickness_slab_deep_etch,
#         zmin=0.0,
#         material="si",
#         mesh_order=1,
#         derived_layer=LogicalLayer(layer=LAYER.SLAB90),
#     ),
#     "slab150": LayerLevel(
#         layer=LogicalLayer(layer=LAYER.SLAB150),
#         thickness=150e-3,
#         zmin=0,
#         material="si",
#         mesh_order=3,
#     ),
#     "slab90": LayerLevel(
#         layer=LogicalLayer(layer=LAYER.SLAB90),
#         thickness=thickness_slab_deep_etch,
#         zmin=0.0,
#         material="si",
#         mesh_order=2,
#     ),
# }


# layer_stack = LayerStack(layers=layers)

# c = gf.c.grating_coupler_elliptical_trenches()
# s = c.to_3d(layer_stack=layer_stack)
# s.show()