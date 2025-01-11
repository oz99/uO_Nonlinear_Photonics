
from functools import partial
# from pydantic import validate_call
import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk
from shapely.geometry.polygon import Polygon
import shapely as sp
import argparse
import numpy as np

PDK = get_generic_pdk()
PDK.activate()


def main(args):

    c = gf.Component("BBB-InGaAsP-OI") # Top Hierarchical Component

    coupler_length = args.coupler_length
    edge_coupling_width = args.edge_coupling_width
 
    die_width = args.die_width
    die_height = args.die_height

    test_wg_width=args.test_wg_width
    test_wg_rows = args.test_wg_rows
    test_wg_spacing = args.test_wg_spacing

    test_wg_bend_min_radius = args.test_wg_bend_min_radius
    test_wg_bend_max_radius = args.test_wg_bend_max_radius
    test_wg_bend_rows = args.test_wg_bend_rows
    test_wg_bend_spacing = args.test_wg_bend_spacing
    bend_output_offset = args.output_offset

    straight_loss_wg1 = args.straight_loss_wg1
    straight_loss_wg2 = args.straight_loss_wg2
    straight_loss_bend_radius = args.straight_loss_bend_radius
    straight_loss_wg_rows = args.straight_loss_wg_rows
    straight_loss_wg_gap = args.straight_loss_wg_gap
    straight_loss_min_wg_length = args.straight_loss_min_wg_length
    straight_loss_max_wg_length = args.straight_loss_max_wg_length

    bend_loss_1_wg1 = args.bend_loss_1_wg1
    bend_loss_1_wg2 = args.bend_loss_1_wg2
    bend_loss_1_bend_radius = args.bend_loss_1_bend_radius
    bend_loss_1_wg_rows = args.bend_loss_1_wg_rows
    bend_loss_1_wg_gap = args.bend_loss_1_wg_gap
    bend_loss_1_min_wg_length = args.bend_loss_1_min_wg_length
    bend_loss_1_max_wg_length = args.bend_loss_1_max_wg_length
    
#################################################################################################################################################################################
    # Components for the test waveguides at the begining of the die
    edge_coupler_array = gf.Component("test_waveguides")
    input_edge_coupler = edge_coupler_array << gf.components.edge_coupler_silicon(length=coupler_length, width1=edge_coupling_width, width2=test_wg_width, with_two_ports=True, cross_section='strip', port_names=('o1', 'o2'), port_types=('edge_coupler', 'optical'), with_bbox=True)
    input_edge_coupler.move((0, die_height-500))
    output_edge_coupler = edge_coupler_array << gf.components.edge_coupler_silicon(length=coupler_length, width1=test_wg_width, width2=edge_coupling_width, with_two_ports=True, cross_section='strip', port_names=('o1', 'o2'), port_types=('optical', 'edge_coupler'), with_bbox=True)
    output_edge_coupler.move((die_width-coupler_length, die_height-500))

    Couplers = c.add_ref(edge_coupler_array, columns=1, rows=test_wg_rows, spacing=[0, -test_wg_spacing])
    coupler_y_coord = [die_height-500 -(i * test_wg_spacing) for i in range(test_wg_rows)]
    coupler_y_coord += [die_height-500-(i*test_wg_spacing) for i in range(test_wg_rows)]
    ports1 = [gf.Port(f"left_{i}", center=(coupler_length, coupler_y_coord[i]), width=test_wg_width, orientation=0,
                      layer=(1,0),cross_section='strip') for i in range(test_wg_rows)]
    ports2 = [gf.Port(f"right_{i}", center=(die_width-coupler_length, coupler_y_coord[i]), width=test_wg_width, 
                      orientation=180, layer=(1,0),cross_section='strip') for i in range(test_wg_rows)]
    
    gf.routing.route_bundle(c, ports1, ports2, route_width=test_wg_width, cross_section='strip')
    test_wg_length = die_width-(2*coupler_length)

    for i in range(test_wg_rows):
        text_str_wg = c << gf.components.text(text=f"test-{i+1}_str-wg_{test_wg_width}um-width_{test_wg_length}um-length", size=10, layer=(1,0))
        text_str_wg.move((coupler_length/3, coupler_y_coord[i]+25))
    
####################################################################################################################################################################################
    # Section for the bend loss measurements
    bend_edge_coupler_array = gf.Component("Bend_loss_measurement")
    bend_Couplers = c.add_ref(bend_edge_coupler_array, columns=1, rows=1, spacing=[0, -test_wg_bend_spacing])

    ## Below was a previous method that worked but took to much space. It's a good example of using coordinates to place the components. There is an easier methods by using connect.
    # bend_input_edge_coupler = bend_edge_coupler_array << gf.components.edge_coupler_silicon(length=coupler_length, width1=edge_coupling_width, width2=test_wg_width, with_two_ports=True, cross_section='strip', port_names=('o1', 'o2'), port_types=('edge_coupler', 'optical'), with_bbox=True)
    # bend_input_edge_coupler.move((0, die_height-500-(test_wg_rows*test_wg_spacing)-500))
    # bend_output_edge_coupler = bend_edge_coupler_array << gf.components.edge_coupler_silicon(length=coupler_length, width1=test_wg_width, width2=edge_coupling_width, with_two_ports=True, cross_section='strip', port_names=('o1', 'o2'), port_types=('optical', 'edge_coupler'), with_bbox=True)
    # bend_output_edge_coupler.move((die_width-coupler_length, die_height-500-(test_wg_rows*test_wg_spacing)-500-bend_output_offset))   
    
    # # For bent waveguides and measuring bend losses. Note there is a change of straight WG distance. We would need to also measure the straight losses by keeping 
    # # the bend radius constant and changing the straight waveguide length.  
    # bend_Couplers = c.add_ref(bend_edge_coupler_array, columns=1, rows=test_wg_bend_rows, spacing=[0, -test_wg_bend_spacing])
    # bend_coupler_y_coord = [die_height-500-(i*test_wg_bend_spacing)-500-(test_wg_rows*test_wg_spacing) for i in range(test_wg_bend_rows)]
    # bend_coupler_y_coord += [die_height-500-(i*test_wg_bend_spacing)-500-(test_wg_rows*test_wg_spacing) for i in range(test_wg_bend_rows)]
    # bend_ports1 = [gf.Port(f"left_{i}", center=(coupler_length, bend_coupler_y_coord[i]), width=test_wg_width, orientation=0,
    #                   layer=(1,0),cross_section='strip') for i in range(test_wg_bend_rows)]
    # bend_ports2 = [gf.Port(f"right_{i}", center=(die_width-coupler_length, bend_coupler_y_coord[i]-bend_output_offset), width=test_wg_width, 
    #                   orientation=180, layer=(1,0),cross_section='strip') for i in range(test_wg_bend_rows)]
    # radii_change = np.linspace(test_wg_bend_max_radius, test_wg_bend_min_radius,  test_wg_bend_rows)
   
    # for i in range(test_wg_bend_rows):
    #     gf.routing.route_single(c, port1=bend_ports1[i], port2=bend_ports2[i], cross_section='strip', route_width=test_wg_width, radius=(radii_change[i]))
    #     straight_length =  die_width-(2*coupler_length)-(2*(radii_change[i]))        #create identifying text for the radii of each bend on the left
    #     text_bends = c << gf.components.text(text=f"{radii_change[i]}um-bend_{straight_length}um-str-wg", size=10, layer=(1,0))
    #     text_bends.move((coupler_length/3, bend_coupler_y_coord[i]+25))

    ########################## Section above wave previously working ############################################################################################################
    
    bend_input_edge_coupler = {}
    bend_output_edge_coupler = {}
    text_bends = {}
    offset_wg = {}
    
    bend_coupler_y_coord = [die_height-500-(i*test_wg_bend_spacing)-500-(test_wg_rows*test_wg_spacing) for i in range(test_wg_bend_rows)]
    bend_coupler_y_coord += [die_height-500-(i*test_wg_bend_spacing)-500-(test_wg_rows*test_wg_spacing) for i in range(test_wg_bend_rows)]
    
    radii_change = np.linspace(test_wg_bend_max_radius, test_wg_bend_min_radius,  test_wg_bend_rows)
   
    for i in range(test_wg_bend_rows):
        
        bend_input_edge_coupler[str(i)] = bend_edge_coupler_array << gf.components.edge_coupler_silicon(length=coupler_length, width1=edge_coupling_width, width2=test_wg_width, with_two_ports=True, cross_section='strip', port_names=('o1', 'o2'), port_types=('edge_coupler', 'optical'), with_bbox=True)
        bend_input_edge_coupler[str(i)].move((0, die_height-500-(test_wg_rows*test_wg_spacing)-500-(i*test_wg_bend_spacing)))
        bend_output_edge_coupler[str(i)] = bend_edge_coupler_array << gf.components.edge_coupler_silicon(length=coupler_length, width1=test_wg_width, width2=edge_coupling_width, with_two_ports=True, cross_section='strip', port_names=('o1', 'o2'), port_types=('optical', 'edge_coupler'), with_bbox=True)
        bend_output_edge_coupler[str(i)].move((die_width-coupler_length, die_height-500-(test_wg_rows*test_wg_spacing)-500-bend_output_offset-(i*test_wg_bend_spacing)))  

    
        offset_wg[str(i)] = bend_edge_coupler_array << gf.components.straight(length=5000-(100*i), width=test_wg_width, cross_section='strip')

        offset_wg[str(i)].connect('o1', bend_input_edge_coupler[str(i)].ports['o2'])
        
        gf.routing.route_single(c, port1=offset_wg[str(i)].ports['o2'], port2=bend_output_edge_coupler[str(i)].ports['o1'], cross_section='strip', route_width=test_wg_width, radius=(radii_change[i]))
        
        straight_length =  die_width-(2*coupler_length)-(2*(radii_change[i]))        #create identifying text for the radii of each bend on the left
        text_bends[str(i)] = c << gf.components.text(text=f"{radii_change[i]}um-bend_{straight_length}um-str-wg", size=10, layer=(1,0))
        text_bends[str(i)].move((coupler_length/3, bend_coupler_y_coord[i]+25))



 #####################################################################################################################################################################################   
    # Section for the straight loss measurements
    straight_loss_measurement = gf.Component("Straight_loss_measurement")
    straight_loss_coupler = c.add_ref(straight_loss_measurement, columns=1, rows=1, spacing=[0, -straight_loss_wg_gap])
    length_change = np.linspace(straight_loss_min_wg_length, straight_loss_max_wg_length, straight_loss_wg_rows)
    straight_loss_input_edge_coupler = {}
    straight_loss_output_edge_coupler = {}
    sraight_loss_wg_1 = {}
    straight_loss_circular_bends = {}
    straight_loss_circular_bends2 = {}
    sraight_loss_wg_2 = {}
    straight_loss_circular_bends3 = {}
    straight_loss_circular_bends4 = {}

    text_straight_loss = {}

    
    for i in range(straight_loss_wg_rows):
        text_straight_loss[str(i)] = straight_loss_measurement << gf.components.text(text=f"straight_loss_{die_width-(2*coupler_length)+2*(straight_loss_min_wg_length+length_change[i])}um-straight_with_{straight_loss_bend_radius}um-bends", size=10, layer=(1,0))
        text_straight_loss[str(i)].move((coupler_length/3, die_height-500-(test_wg_rows*test_wg_spacing)-500-(test_wg_bend_spacing*test_wg_bend_rows)-500+25-(i*straight_loss_wg_gap) )) 

        straight_loss_input_edge_coupler[str(i)] = straight_loss_measurement << gf.components.edge_coupler_silicon(length=coupler_length, width1=edge_coupling_width, width2=test_wg_width, with_two_ports=True, cross_section='strip', port_names=('o1', 'o2'), port_types=('edge_coupler', 'optical'), with_bbox=True)
        straight_loss_input_edge_coupler[str(i)].move((0, die_height-500-(test_wg_rows*test_wg_spacing)-500-(test_wg_bend_spacing*test_wg_bend_rows)-500-(i*straight_loss_wg_gap)))
        straight_loss_output_edge_coupler[str(i)] = straight_loss_measurement << gf.components.edge_coupler_silicon(length=coupler_length, width1=test_wg_width, width2=edge_coupling_width, with_two_ports=True, cross_section='strip', port_names=('o1', 'o2'), port_types=('optical', 'edge_coupler'), with_bbox=True)
        straight_loss_output_edge_coupler[str(i)].move((die_width-coupler_length, die_height-500-(test_wg_rows*test_wg_spacing)-500-(test_wg_bend_spacing*test_wg_bend_rows)-500+(4*straight_loss_bend_radius)-(i*straight_loss_wg_gap)))   

        sraight_loss_wg_1[str(i)] = straight_loss_measurement << gf.components.straight(length=straight_loss_min_wg_length+length_change[i], width=test_wg_width, cross_section='strip')
        straight_loss_circular_bends[str(i)] = straight_loss_measurement << gf.components.bend_circular(radius=straight_loss_bend_radius, width=test_wg_width, cross_section='strip')
        straight_loss_circular_bends2[str(i)] = straight_loss_measurement << gf.components.bend_circular(radius=straight_loss_bend_radius, width=test_wg_width, cross_section='strip')
        sraight_loss_wg_2[str(i)] = straight_loss_measurement << gf.components.straight(length=straight_loss_min_wg_length+length_change[i], width=test_wg_width, cross_section='strip')
        straight_loss_circular_bends3[str(i)] = straight_loss_measurement << gf.components.bend_circular(radius=straight_loss_bend_radius, width=test_wg_width, cross_section='strip')
        straight_loss_circular_bends4[str(i)] = straight_loss_measurement << gf.components.bend_circular(radius=straight_loss_bend_radius, width=test_wg_width, cross_section='strip')

        sraight_loss_wg_1[str(i)].connect('o1', straight_loss_input_edge_coupler[str(i)].ports['o2'])
        straight_loss_circular_bends[str(i)].connect('o1', sraight_loss_wg_1[str(i)].ports['o2'])
        straight_loss_circular_bends2[str(i)].connect('o1', straight_loss_circular_bends[str(i)].ports['o2'])
        sraight_loss_wg_2[str(i)].connect('o1', straight_loss_circular_bends2[str(i)].ports['o2'])
        straight_loss_circular_bends3[str(i)].connect('o2', sraight_loss_wg_2[str(i)].ports['o2'])
        straight_loss_circular_bends4[str(i)].connect('o2', straight_loss_circular_bends3[str(i)].ports['o1'])

        gf.routing.route_single(straight_loss_measurement, port1=straight_loss_circular_bends4[str(i)].ports['o1'], port2=straight_loss_output_edge_coupler[str(i)].ports['o1'], cross_section='strip', route_width=test_wg_width, radius=straight_loss_bend_radius)
#############################################################################################################################################################################################
    # 2nd Confirmation of bend loss measurement

    bend_loss_measurement_1 = gf.Component("Bend_loss_measurement_fixed_radii")
    bend_loss_measurement_1_repeater = gf.Component("Bend_loss_measurement_repeater")
    bend_loss_coupler_1 = c.add_ref(bend_loss_measurement_1, columns=1, rows=1, spacing=[0, -bend_loss_1_wg_gap])
    bend_loss_1_input_edge_coupler = {}
    bend_loss_1_output_edge_coupler = {}
    bend_loss_1_wg_1 = {}
    bend_loss_1_circular_bends = {}
    bend_loss_1_circular_bends2 = {}
    bend_loss_1_wg_2 = {}
    bend_loss_1_circular_bends3 = {}
    bend_loss_1_circular_bends4 = {}

    bend_loss_coupler_1_repeater = {}

    text_bend_loss_1 = {}

    ref = {}

    for i in range(bend_loss_1_wg_rows):
        text_bend_loss_1[str(i)] = bend_loss_measurement_1 << gf.components.text(text=f"bend_loss_1_{die_width-(2*coupler_length)+2*(bend_loss_1_min_wg_length+length_change[i])}um-straight_with_{bend_loss_1_bend_radius}um-bends", size=10, layer=(1,0))
        text_bend_loss_1[str(i)].move((coupler_length/3, die_height-500-(test_wg_rows*test_wg_spacing)-500-(test_wg_bend_spacing*test_wg_bend_rows)-500+25-(i*bend_loss_1_wg_gap) )) 

        bend_loss_1_input_edge_coupler[str(i)] = bend_loss_measurement_1 << gf.components.edge_coupler_silicon(length=coupler_length, width1=edge_coupling_width, width2=test_wg_width, with_two_ports=True, cross_section='strip', port_names=('o1', 'o2'), port_types=('edge_coupler', 'optical'), with_bbox=True)
        bend_loss_1_input_edge_coupler[str(i)].move((0, die_height-500-(test_wg_rows*test_wg_spacing)-500-(test_wg_bend_spacing*test_wg_bend_rows)-500-(straight_loss_wg_rows*straight_loss_wg_gap)-500-(i*bend_loss_1_wg_gap)))
        bend_loss_1_output_edge_coupler[str(i)] = bend_loss_measurement_1 << gf.components.edge_coupler_silicon(length=coupler_length, width1=test_wg_width, width2=edge_coupling_width, with_two_ports=True, cross_section='strip', port_names=('o1', 'o2'), port_types=('optical', 'edge_coupler'), with_bbox=True)
        bend_loss_1_output_edge_coupler[str(i)].move((die_width-coupler_length, die_height-500-(test_wg_rows*test_wg_spacing)-500-(test_wg_bend_spacing*test_wg_bend_rows)-500-(straight_loss_wg_rows*straight_loss_wg_gap)-500-(i*bend_loss_1_wg_gap)))   
        

        ## Use a ref instead since it's all the same component just repeated? 


        # bend_loss_1_wg_1[str(i)] = bend_loss_measurement_1 << gf.components.straight(length=bend_loss_1_min_wg_length+length_change[i], width=test_wg_width, cross_section='strip')
        bend_loss_1_circular_bends[str(i)] = bend_loss_measurement_1_repeater << gf.components.bend_circular(radius=bend_loss_1_bend_radius, width=test_wg_width, cross_section='strip')
        bend_loss_1_circular_bends2[str(i)] = bend_loss_measurement_1_repeater << gf.components.bend_circular(radius=bend_loss_1_bend_radius, width=test_wg_width, cross_section='strip')
        # bend_loss_1_wg_2[str(i)] = bend_loss_measurement_1 << gf.components.straight(length=bend_loss_1_min_wg_length+length_change[i], width=test_wg_width, cross_section='strip')
        bend_loss_1_circular_bends3[str(i)] = bend_loss_measurement_1_repeater << gf.components.bend_circular(radius=bend_loss_1_bend_radius, width=test_wg_width, cross_section='strip')
        bend_loss_1_circular_bends4[str(i)] = bend_loss_measurement_1_repeater << gf.components.bend_circular(radius=bend_loss_1_bend_radius, width=test_wg_width, cross_section='strip')

        bend_loss_1_circular_bends[str(i)].connect('o1', bend_loss_1_input_edge_coupler[str(i)].ports['o2'])
        bend_loss_1_circular_bends2[str(i)].connect('o2', bend_loss_1_circular_bends[str(i)].ports['o2'])
        bend_loss_1_circular_bends3[str(i)].connect('o2', bend_loss_1_circular_bends2[str(i)].ports['o1'])
        bend_loss_1_circular_bends4[str(i)].connect('o1', bend_loss_1_circular_bends3[str(i)].ports['o1'])

        # bend_loss_measurement_1_repeater_ref = bend_loss_measurement_1.add_ref(bend_loss_measurement_1_repeater, columns=1+i, rows=1, spacing=[500, 0] )  # Reference the Component "p" that has the polygon in it

        # bend_loss_copy = bend_loss_measurement_1 << gf.copy(bend_loss_measurement_1_repeater)
        
        # bend_loss_coupler_1_repeater[str(i)] = bend_loss_measurement_1
        

        # ref[str(i)] = bend_loss_measurement_1.add_ref(bend_loss_measurement_1_repeater)  # Reference the Component "c" that 3 references in it
        # d_ref2 = c2 << c  # Use the "<<" operator to create a 2nd reference to c.plot()
        # d_ref3 = c2 << c  # Use the "<<" operator to create a 3rd reference to c.plot()

        # d_ref1.move([20, 0])
        # d_ref2.move([40, 0])

        # .add_ref(bend_loss_measurement_1_repeater, columns=i, rows=1, spacing=[500, 0])

        bend_loss_coupler_1_repeater[str(i)] = bend_loss_measurement_1.add_ref(bend_loss_measurement_1_repeater, columns=i, rows=1, spacing=[500, 0])
        print(bend_loss_coupler_1_repeater[str(i)])
        # gf.routing.route_single(bend_loss_measurement_1, port1=bend_loss_1_circular_bends4[str(i)].ports['o2'], port2=bend_loss_1_output_edge_coupler[str(i)].ports['o1'], cross_section='strip', route_width=test_wg_width, radius=bend_loss_1_bend_radius)


#############################################################################################################################################################################################    
    # Now for the creation of the frame
    frame = c << gf.components.die(size=(die_width, die_height), street_width=100, street_length=100, die_name='Ozan W. Oner',
                                    text_size=250, text_location='SW', layer='FLOORPLAN', bbox_layer='FLOORPLAN', text='text', draw_corners=False)
    frame.move((die_width/2, die_height/2))
###########################################################################################################################################################################################
    # Now for the writing of the GDS file and viewing it in KLayout. Ensure Klayout is open for the viewing to work with KLive
    gdspath = c.write_gds("BBBs-InGaAsP-OI.gds", precision=1e-9, unit=1e-6,with_metadata=True)
    gf.show(gdspath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()



    parser.add_argument('--die_width', type=int, default=10000, help='width of the die in um')
    parser.add_argument('--die_height', type=int, default=25400, help='height of the Die in um')

    # Note that inverse tapers generally give better performance. Try to have a smaller width at the end of the taper where the fiber is than the waveguide.
    parser.add_argument('--coupler_length', type=int, default=300, help='length of the edge coupler')
    parser.add_argument('--edge_coupling_width', type=int, default=0.1, help='width of the edge coupler to the fiber')

    parser.add_argument('--ring_gap', type=int, default=0.2, help='spacing between waveguides')

    parser.add_argument('--test_wg_width', type=int, default=0.5, help='Width of the test waveguides')
    parser.add_argument('--test_wg_rows', type=int, default=5, help='Number of waveguides to test')
    parser.add_argument('--test_wg_spacing', type=int, default=127, help='Spacing between the waveguides')

    # Bend loss measurement parameters
    parser.add_argument('--test_wg_bend_min_radius', type=int, default=10, help='minimum bend radius for the waveguides')
    parser.add_argument('--test_wg_bend_max_radius', type=int, default=100, help='maximum bend radius for the waveguides')
    parser.add_argument('--test_wg_bend_rows', type=int, default=19, help='number of rows for waveguide bends')
    parser.add_argument('--test_wg_bend_spacing', type=int, default=150, help='spacing between the waveguides for bends')
    parser.add_argument('--output_offset', type=int, default=250, help='offset for the output edge coupler')
    
    # The following has not been implemented yet. I intend for it to be used as the spacing between various sets of WGs
    parser.add_argument('--distance_between_sets', type=int, default=500, help='Spacing between the straight and bent waveguides')

    ## Straight_loss_measurement parameters
    parser.add_argument('--straight_loss_wg1', type=int, default=1000, help='Length of the straight waveguide 1')
    parser.add_argument('--straight_loss_wg2', type=int, default=1000, help='Length of the straight waveguide 2')

    parser.add_argument('--straight_loss_min_wg_length', type=int, default=1000, help='smallest straight waveguide length')
    parser.add_argument('--straight_loss_max_wg_length', type=int, default=8000, help='largest straight waveguide length')   
    parser.add_argument('--straight_loss_wg_rows', type=int, default=15, help='largest straight waveguide length')   
    parser.add_argument('--straight_loss_wg_gap', type=int, default=250, help='spacing between the straight loss waveguides')

    parser.add_argument('--straight_loss_bend_radius', type=int, default=50, help='Bend radius for the circular bends in the straight loss measurement')

    
    # Bend loss parameters

    parser.add_argument('--bend_loss_1_wg1', type=int, default=1000, help='Length of the straight waveguide 1')
    parser.add_argument('--bend_loss_1_wg2', type=int, default=1000, help='Length of the straight waveguide 2')

    parser.add_argument('--bend_loss_1_min_wg_length', type=int, default=1000, help='smallest straight waveguide length')
    parser.add_argument('--bend_loss_1_max_wg_length', type=int, default=8000, help='largest straight waveguide length')   
    parser.add_argument('--bend_loss_1_wg_rows', type=int, default=15, help='largest straight waveguide length')   
    parser.add_argument('--bend_loss_1_wg_gap', type=int, default=250, help='spacing between the straight loss waveguides')

    parser.add_argument('--bend_loss_1_bend_radius', type=int, default=50, help='Bend radius for the circular bends in the straight loss measurement')
    
    ########### Add section for y-splitter. MMI. Couplers
    


    args = parser.parse_args()
    main(args)

