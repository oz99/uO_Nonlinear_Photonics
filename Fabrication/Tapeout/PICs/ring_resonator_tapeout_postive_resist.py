from functools import partial
# from pydantic import validate_call
import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
from shapely.geometry.polygon import Polygon
import shapely as sp
import argparse

PDK = get_generic_pdk()
PDK.activate()



def main(args):

    length1 = args.length1
    layer = args.layer

    iteration_width = args.iteration_width
    MinWidth = args.MinWidth
    MaxWidth = args.MaxWidth
    wall_width = args.wall_width

    ring_gap = args.ring_gap
    ring_radius = args.ring_radius
    ring_wg_width = args.ring_wg_width

    c = gf.Component("ring_tapeout_positive_resist")
    out = gf.Component("ring_tapeout_outer")
    final = gf.Component("ring_set_final")

    #d = gf.Component("test")
    #center = c << gf.components.rectangle(size=(length1, width), layer=layer)
    ring_gaps = []

    #number of waveguide steps will be determined
    ring_gap = ring_gap-iteration_width
    steps = int((MaxWidth-ring_gap)/iteration_width)



    for i in range(0, steps+1):
        ring_gap = ring_gap + iteration_width

        ring = c << gf.components.ring_double_pn(add_gap=ring_gap, drop_gap=ring_gap, radius=ring_radius, width=ring_wg_width, doping_angle=85, doped_heater=True, doped_heater_angle_buffer=10, doped_heater_layer='NPP', doped_heater_width=0.5, doped_heater_waveguide_offset=2.175)
        # Create straight waveguides that go 5mm to either end of the chip
        
        
        b = c << gf.components.straight(length=length1/2,width=ring_wg_width)
        d = c << gf.components.straight(length=length1/2,width=ring_wg_width)
        e = c << gf.components.straight(length=length1/2,width=ring_wg_width)
        f = c << gf.components.straight(length=length1/2,width=ring_wg_width)

        
        ring_gaps.append(ring_gap-(iteration_width/2)) 
        total_y = sum(ring_gaps)     
        ring.center = ([length1/2,total_y+(50*i)]) ## This ensure all the waveguide are 1000nm apart

        b.connect("o1", destination=ring["o1"])
        d.connect("o1", destination=ring["o2"])
        e.connect("o1", destination=ring["o3"])
        f.connect("o1", destination=ring["o4"])

        d_ref1 = out.add_ref(c)  # Reference the Component "c" that 3 references in it
        d_ref2 = out << c

        d_ref2.move([300, 200])

        # ring_out = d << gf.components.ring_double_pn(add_gap=ring_gap, drop_gap=ring_gap, radius=ring_radius, width=new_width, doping_angle=85, doped_heater=True, doped_heater_angle_buffer=10, doped_heater_layer='NPP', doped_heater_width=0.5, doped_heater_waveguide_offset=2.175)
        # # Create straight waveguides that go 5mm to either end of the chip
        
        
        # b = d << gf.components.straight(length=length1/2,width=ring_wg_width+wall_width)
        # d = d << gf.components.straight(length=length1/2,width=ring_wg_width+wall_width)
        # e = d << gf.components.straight(length=length1/2,width=ring_wg_width+wall_width)
        # f = d << gf.components.straight(length=length1/2,width=ring_wg_width+wall_width)

       

        # b.connect("o1", destination=ring_out["o1"])
        # d.connect("o1", destination=ring_out["o2"])
        # e.connect("o1", destination=ring_out["o3"])
        # f.connect("o1", destination=ring_out["o4"])

        # combine = final << gf.geometry.boolean(ring, ring_out, operation="xor")

        #width=ring_wg_width, layer=layer
        
        # c1 = gf.components.rectangle(size=(length1, width), layer=layer).ref()
        
        # c2 = gf.components.rectangle(size=(length1, width+wall_width), layer=layer).ref()
        #xor of the two above rectangles
        
 
        # c1.center = ([length1/2,total_y+(1000*i)]) ## This ensure all the waveguide are 1000nm apart
        # c2.center = ([length1/2,total_y+(1000*i)])


        # # c3 = gf.geometry.boolean(c1, c2, operation="xor")
        # c.flatten()
        # ring.name = f"ring_{ring_gap}_nm"
       

        ###### Create rings with varying radius and gap



        ## Add rectangles to all corners of the L shape


    # Save the component to a GDSII file with high precision
    #d.write_gds("L_meta_prox.gds",with_metadata=True)
    
    gdspath = c.write_gds("ring_tapeout_pos_resist.gds", precision=1e-9, unit=1e-6,with_metadata=True)

    # Display the GDSII file using gdsfactory's viewer
    gf.show(gdspath)

    # gf.write_gds("L_w_proximity.gds", with_metadata=True)

    ## Extract and Save Netlist [Connections, Instances, Placements, Ports, Name]
    #elems_yaml = c.get_netlist_yaml()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--ring_gap', type=int, default=0.2, help='spacing between waveguides')
    parser.add_argument('--ring_radius', type=int, default=10, help='spacing between waveguides')
    parser.add_argument('--ring_wg_width', type=int, default=0.42, help='spacing between waveguides')
    
    
    parser.add_argument('--iteration_width', type=int, default=0.025, help='spacing between waveguides')
    parser.add_argument('--MinWidth', type=int, default=0.5, help='Minimum Width of the waveguide')
    parser.add_argument('--MaxWidth', type=int, default=0.50, help='Maximum Width of the waveguide')
    parser.add_argument('--wall-width', type=int, default=1, help='Maximum Width of the waveguide')



    parser.add_argument('--length1', type=int, default=5000, help='Length of the waveguide')
    parser.add_argument('--layer', type=int, default=1, help='Layer number for the L shape')



    parser.add_argument('-NetlistNew', action='store_true', default=True, help='Set True to Activate (default: False)')
    args = parser.parse_args()
    main(args)
