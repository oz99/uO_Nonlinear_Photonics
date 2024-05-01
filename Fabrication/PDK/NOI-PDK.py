### Author: Ozan W. Oner
### email: ooner083@uottawa
### This code serves as the basis of the layers for the Nonlinear on Insulator PDK. 
### These parameter stack are for InGaAsP-On-Insulator

import pathlib
from functools import partial
import pytest
from pytest_regressions.data_regression import DataRegressionFixture
import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.config import PATH
from gdsfactory.decorators import has_valid_transformations
from gdsfactory.difftest import difftest
from gdsfactory.generic_tech import get_generic_pdk
from gdsfactory.technology import (
    LayerViews,
    lyp_to_dataclass
)
from gdsfactory.typings import Layer, LayerSpec

from gdsfactory.generic_tech.layer_map import LAYER
from gdsfactory.technology import LayerLevel, LayerStack

nm = 1e-3

class LayerStackParameters:
    Si: Layer = (1, 0)  # Example custom layer for Silicon, layer number 1, datatype 0
    SiN: Layer = (2, 0)  # Example custom layer for Silicon Nitride, layer number 2, datatype 0

    ##################Passive Layer #######################
    thickness_wg: float = 220 * nm
    thickness_slab_deep_etch: float = 90 * nm
    thickness_slab_shallow_etch: float = 150 * nm
    sidewall_angle_wg: float = 10


    ###################Active Layer #######################
    thickness_indium_phosphide = 500*nm

    ##################Oxide (Insulation) Layer#######################
    thickness_clad: float = 3.0
    box_thickness: float = 3.0 ## Do we want 2um instead
    thickness_nitride: float = 350 * nm
    thickness_ge: float = 500 * nm
    gap_silicon_to_nitride: float = 100 * nm
    

    ##################Mealizations Layer#######################
    zmin_heater: float = 1.1
    zmin_metal1: float = 1.1
    thickness_metal1: float = 700 * nm
    zmin_metal2: float = 2.3
    thickness_metal2: float = 700 * nm
    zmin_metal3: float = 3.2
    thickness_metal3: float = 2000 * nm
    
    ##################General Stack Parameters#####################
    undercut_thickness: float = 5.0
    substrate_thickness: float = 10.0


    WAFER: Layer = (99999, 0)

    WG: Layer = (1, 0)
    WGCLAD: Layer = (111, 0)
    SLAB150: Layer = (2, 0)
    SLAB90: Layer = (3, 0)
    DEEPTRENCH: Layer = (4, 0)
    GE: Layer = (5, 0)
    UNDERCUT: Layer = (6, 0)
    WGN: Layer = (34, 0)
    WGN_CLAD: Layer = (36, 0)

    N: Layer = (20, 0)
    NP: Layer = (22, 0)
    NPP: Layer = (24, 0)
    P: Layer = (21, 0)
    PP: Layer = (23, 0)
    PPP: Layer = (25, 0)
    GEN: Layer = (26, 0)
    GEP: Layer = (27, 0)

    HEATER: Layer = (47, 0)
    M1: Layer = (41, 0)
    M2: Layer = (45, 0)
    M3: Layer = (49, 0)
    VIAC: Layer = (40, 0)
    VIA1: Layer = (44, 0)
    VIA2: Layer = (43, 0)
    PADOPEN: Layer = (46, 0)

    DICING: Layer = (100, 0)
    NO_TILE_SI: Layer = (71, 0)
    PADDING: Layer = (67, 0)
    DEVREC: Layer = (68, 0)
    FLOORPLAN: Layer = (64, 0)
    TEXT: Layer = (66, 0)
    PORT: Layer = (1, 10)
    PORTE: Layer = (1, 11)
    PORTH: Layer = (70, 0)
    SHOW_PORTS: Layer = (1, 12)
    LABEL: Layer = (201, 0)
    LABEL_SETTINGS: Layer = (202, 0)
    TE: Layer = (203, 0)
    TM: Layer = (204, 0)
    DRC_MARKER: Layer = (205, 0)
    LABEL_INSTANCE: Layer = (206, 0)
    ERROR_MARKER: Layer = (207, 0)
    ERROR_PATH: Layer = (208, 0)

    SOURCE: Layer = (110, 0)
    MONITOR: Layer = (101, 0)

### Following were component Specs
    # def create_layer_stack(self):
    #     # Define layer levels with thickness and zmin for each layer
    #     level_Si = gf.LayerLevel(layer=self.layers['Si'], thickness=220, zmin=0)
    #     level_SiN = gf.LayerLevel(layer=self.layers['SiN'], thickness=150, zmin=220)

    #     # Create and return a LayerStack instance
    #     return gf.LayerStack(levels=[level_Si, level_SiN])

    # @gf.cell
    # def waveguide(self, length=10.0, width=0.5):
    #     # Use a specific layer for the waveguide
    #     return gf.components.straight(length=length, width=width, layer=self.layers['Si'])

    # @gf.cell
    # def ring_resonator(self, radius=10.0, width=0.5, gap=0.2):
    #     # Use a specific layer for the ring resonator
    #     return gf.components.ring_single(radius=radius, width=width, gap=gap, layer=self.layers['Si'])



LAYER = LayerStackParameters()

def get_layer_stack(
    thickness_wg=LayerStackParameters.thickness_wg,
    thickness_slab_deep_etch=LayerStackParameters.thickness_slab_deep_etch,
    thickness_slab_shallow_etch=LayerStackParameters.thickness_slab_shallow_etch,
    sidewall_angle_wg=LayerStackParameters.sidewall_angle_wg,
    thickness_clad=LayerStackParameters.thickness_clad,
    thickness_nitride=LayerStackParameters.thickness_nitride,
    thickness_ge=LayerStackParameters.thickness_ge,
    gap_silicon_to_nitride=LayerStackParameters.gap_silicon_to_nitride,
    zmin_heater=LayerStackParameters.zmin_heater,
    zmin_metal1=LayerStackParameters.zmin_metal1,
    thickness_metal1=LayerStackParameters.thickness_metal1,
    zmin_metal2=LayerStackParameters.zmin_metal2,
    thickness_metal2=LayerStackParameters.thickness_metal2,
    zmin_metal3=LayerStackParameters.zmin_metal3,
    thickness_metal3=LayerStackParameters.thickness_metal3,
    substrate_thickness=LayerStackParameters.substrate_thickness,
    box_thickness=LayerStackParameters.box_thickness,
    undercut_thickness=LayerStackParameters.undercut_thickness,
) -> LayerStack:
    """Returns generic LayerStack.

    based on paper https://www.degruyter.com/document/doi/10.1515/nanoph-2013-0034/html

    Args:
        thickness_wg: waveguide thickness in um.
       thickness_slab_deep_etch: for deep etched slab.
        thickness_shallow_etch: thickness for the etch in um.
        sidewall_angle_wg: waveguide side angle.
        thickness_clad: cladding thickness in um.
        thickness_nitride: nitride thickness in um.
        thickness_ge: germanium thickness.
        gap_silicon_to_nitride: distance from silicon to nitride in um.
        zmin_heater: TiN heater.
        zmin_metal1: metal1.
        thickness_metal1: metal1 thickness.
        zmin_metal2: metal2.
        thickness_metal2: metal2 thickness.
        zmin_metal3: metal3.
        thickness_metal3: metal3 thickness.
        substrate_thickness: substrate thickness in um.
        box_thickness: bottom oxide thickness in um.
        undercut_thickness: thickness of the InGaAsP undercut.
    """

    thickness_deep_etch = thickness_wg - thickness_slab_deep_etch
    thickness_shallow_etch = thickness_wg - thickness_slab_shallow_etch

    return LayerStack(
        layers=dict(
            substrate=LayerLevel(
                layer=LAYER.WAFER,
                thickness=substrate_thickness,
                zmin=-substrate_thickness - box_thickness,
                material="si",
                mesh_order=101,
                background_doping_concentration=1e14, #This is the handle layer. 725um.
                background_doping_ion="Boron",		
                orientation="100",
            ),
            box=LayerLevel(
                layer=LAYER.WAFER,
                thickness=box_thickness,
                zmin=-box_thickness,
                material="sio2",
                mesh_order=9,
            ),
            core=LayerLevel(
                layer=LAYER.WG,
                thickness=thickness_wg,
                zmin=0.0,
                material="InGaAsP",
                mesh_order=2,
                sidewall_angle=sidewall_angle_wg,
                width_to_z=0.5,
                background_doping_concentration=1e14, #Should this be changed? Would it just be the quarternaries of InGaAsP that would be changed?
                background_doping_ion="Boron",		# This includes Boron
                orientation="100",
                info={"active": True},
            ),

            ### Need to add these to the wafermap function
            # shallow_etch=LayerLevel(
            #     layer=LAYER.SHALLOW_ETCH,
            #     thickness=thickness_shallow_etch,
            #     zmin=0.0,
            #     material="InGaAsP",
            #     mesh_order=1,
            #     layer_type="etch",
            #     into=["core"],
            #     derived_layer=LAYER.SLAB150,
            # ),
            # deep_etch=LayerLevel(
            #     layer=LAYER.DEEP_ETCH,
            #     thickness=thickness_deep_etch,
            #     zmin=0.0,
            #     material="InGaAsP",
            #     mesh_order=1,
            #     layer_type="etch",
            #     into=["core"],
            #     derived_layer=LAYER.SLAB90,
            # ),
            clad=LayerLevel(
                layer=LAYER.WAFER,
                zmin=0.0,
                material="sio2",
                thickness=thickness_clad,
                mesh_order=10,
            ),
            slab150=LayerLevel(
                layer=LAYER.SLAB150,
                thickness=150e-3,
                zmin=0,
                material="InGaAsP",
                mesh_order=3,
            ),
            slab90=LayerLevel(
                layer=LAYER.SLAB90,
                thickness=thickness_slab_deep_etch,
                zmin=0.0,
                material="InGaAsP",
                mesh_order=2,
            ),


            nitride=LayerLevel(
                layer=LAYER.WGN,
                thickness=thickness_nitride,
                zmin=thickness_wg + gap_silicon_to_nitride,
                material="sin",
                mesh_order=2,
            ),
            ge=LayerLevel(
                layer=LAYER.GE,
                thickness=thickness_ge,
                zmin=thickness_wg,
                material="ge",
                mesh_order=1,
            ),


            undercut=LayerLevel(
                layer=LAYER.UNDERCUT,
                thickness=-undercut_thickness,
                zmin=-box_thickness,
                material="air",
                z_to_bias=(
                    [0, 0.3, 0.6, 0.8, 0.9, 1],
                    [-0, -0.5, -1, -1.5, -2, -2.5],
                ),
                mesh_order=1,
            ),
            via_contact=LayerLevel(
                layer=LAYER.VIAC,
                thickness=zmin_metal1 - thickness_slab_deep_etch,
                zmin=thickness_slab_deep_etch,
                material="Aluminum",
                mesh_order=1,
                sidewall_angle=-10,
                width_to_z=0,
            ),
            metal1=LayerLevel(
                layer=LAYER.M1,
                thickness=thickness_metal1,
                zmin=zmin_metal1,
                material="Aluminum",
                mesh_order=2,
            ),
            heater=LayerLevel(
                layer=LAYER.HEATER,
                thickness=750e-3,
                zmin=zmin_heater,
                material="TiN",
                mesh_order=2,
            ),
            via1=LayerLevel(
                layer=LAYER.VIA1,
                thickness=zmin_metal2 - (zmin_metal1 + thickness_metal1),
                zmin=zmin_metal1 + thickness_metal1,
                material="Aluminum",
                mesh_order=1,
            ),
            metal2=LayerLevel(
                layer=LAYER.M2,
                thickness=thickness_metal2,
                zmin=zmin_metal2,
                material="Aluminum",
                mesh_order=2,
            ),
            via2=LayerLevel(
                layer=LAYER.VIA2,
                thickness=zmin_metal3 - (zmin_metal2 + thickness_metal2),
                zmin=zmin_metal2 + thickness_metal2,
                material="Aluminum",
                mesh_order=1,
            ),
            metal3=LayerLevel(
                layer=LAYER.M3,
                thickness=thickness_metal3,
                zmin=zmin_metal3,
                material="Aluminum",
                mesh_order=2,
            ),
        )
    )


if __name__ == "__main__":

    LAYER = LayerStackParameters()
    
    
    LAYER_STACK = get_layer_stack()
    # pdk = PDKSetup()
    # print("Layer stack defined:", pdk.layer_stack)
    # wg = pdk.waveguide()
    # rr = pdk.ring_resonator()
    print("Layers have been added to the PDK.")
    print("Layer stack defined:", LayerStackParameters.thickness_wg)
    print("Layer stack defined:", LayerStackParameters.Si)

