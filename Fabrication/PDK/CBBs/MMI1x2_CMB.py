import gdsfactory as gf
import yaml
import numpy as np
import argparse
import re

def main(args):
    c = gf.Component("MMI1x2_OW")

    ## Parameters
    w = args.width
    tp_w = args.taperwidth
    tp_length = args.taperlength
    mmi_width = args.mmiwidth
    mmi_length = args.mmilength
    mmi_gap = args.mmigap
    str_len = args.straightlength
    device_name = 'MMI1x2_OW'

    ## Cross-Sections of Waveguides
    layer = (1,0)
    xs = gf.cross_section.cross_section(width=w, offset=0, layer=layer)

     # Define Input/Output Waveguides 
    portsName=['Port1','Port2', 'Port3']
    a = gf.Component(portsName[0])
    a.add_polygon([(0, str_len, str_len, 0), (w/2, w/2, -(w/2), -(w/2))], layer=layer)
    a.add_port(name="o1", center=[str_len-str_len, w-w], width = w, orientation=180, layer=layer, port_type='optical')
    a.add_port(name="o2", center=[str_len, w-w], width = w, orientation=0, layer=layer, port_type='optical')
    a.info['Width'] = float(w)
    a.info['Length'] = float(str_len)
    wg_in = c << a

    b = gf.Component(portsName[1])
    xpts1 = [str_len+tp_length+mmi_length+tp_length, str_len+tp_length+mmi_length+tp_length+str_len, str_len+tp_length+mmi_length+tp_length+str_len, str_len+tp_length+mmi_length+tp_length]
    ypts1 = [mmi_gap/2+tp_w/2-w/2, mmi_gap/2+tp_w/2-w/2, mmi_gap/2+tp_w/2+w/2, mmi_gap/2+tp_w/2+w/2]
    b.add_polygon((xpts1, ypts1), layer=layer)
    b.add_port(name="o1", center=[str_len+tp_length+mmi_length+tp_length, mmi_gap/2+tp_w/2], width = w, orientation=180, layer=layer, port_type='optical')
    b.add_port(name="o2", center=[str_len+tp_length+mmi_length+tp_length+str_len, mmi_gap/2+tp_w/2], width = w, orientation=0, layer=layer, port_type='optical')
    b.info['Width'] = float(w)
    b.info['Length'] = float(str_len)
    wg_thru = c << b

    d = gf.Component(portsName[2])
    xpts2 = [str_len+tp_length+mmi_length+tp_length, str_len+tp_length+mmi_length+tp_length+str_len, str_len+tp_length+mmi_length+tp_length+str_len, str_len+tp_length+mmi_length+tp_length]
    ypts2 = [-(mmi_gap/2+tp_w/2-w/2), -(mmi_gap/2+tp_w/2-w/2), -(mmi_gap/2+tp_w/2+w/2), -(mmi_gap/2+tp_w/2+w/2)]
    d.add_polygon((xpts2, ypts2), layer=layer)
    d.add_port(name="o1", center=[str_len+tp_length+mmi_length+tp_length, -(mmi_gap/2+tp_w/2)], width = w, orientation=180, layer=layer, port_type='optical')
    d.add_port(name="o2", center=[str_len+tp_length+mmi_length+tp_length+str_len, -(mmi_gap/2+tp_w/2)], width = w, orientation=0, layer=layer, port_type='optical')
    d.info['Width'] = float(w)
    d.info['Length'] = float(str_len)
    wg_drop = c << d

    ## Define MMI Tapers and Body
    mmi1x2 = gf.Component("MMI1x2")

    # Define Input Taper
    tp_in1 = gf.Component("InputTaper")
    xpts = [str_len, str_len+tp_length, str_len+tp_length, str_len]
    ypts = [w/2, tp_w/2, -(tp_w/2), -(w/2)]
    tp_in1.add_polygon((xpts, ypts), layer=layer)
    tp_in1.add_port(name="o1", center=[str_len, w-w], width = w, orientation=180, layer=layer, port_type='optical')
    tp_in1.add_port(name="o2", center=[str_len+tp_length, tp_w-tp_w], width = tp_w, orientation=0, layer=layer, port_type='optical')
    input_taper1 = mmi1x2 << tp_in1
    input_taper1.connect("o1", wg_in.ports["o2"])

    # Define MMI Body
    mmi = gf.Component("MMI")
    xpts_mmi = [str_len+tp_length, str_len+tp_length+mmi_length, str_len+tp_length+mmi_length, str_len+tp_length]
    ypts_mmi = [mmi_width/2, mmi_width/2, -(mmi_width/2), -(mmi_width/2)]
    mmi.add_polygon((xpts_mmi, ypts_mmi), layer=layer)
    mmi.add_port(name="o1", center=[str_len+tp_length, w-w], width = w, orientation=180, layer=layer, port_type='optical')
    mmi.add_port(name="o2", center=[str_len+tp_length+mmi_length, (mmi_gap/2)+(tp_w/2)], width = w, orientation=0, layer=layer, port_type='optical')
    mmi.add_port(name="o3", center=[str_len+tp_length+mmi_length, -(mmi_gap/2)-(tp_w/2)], width = w, orientation=0, layer=layer, port_type='optical')
    input_mmi = mmi1x2 << mmi

    # Define Output Taper 1
    tp_out1 = gf.Component("Output Taper 1")
    xpts_tp1out = [str_len+tp_length+mmi_length, str_len+tp_length+mmi_length+tp_length, str_len+tp_length+mmi_length+tp_length, str_len+tp_length+mmi_length]
    ypts_tp1out = [(mmi_gap/2)+tp_w, (mmi_gap/2)+(tp_w/2)+(w/2), (mmi_gap/2)+(tp_w/2)-(w/2), mmi_gap/2]
    tp_out1.add_polygon((xpts_tp1out, ypts_tp1out), layer=layer)
    tp_out1.add_port(name="o1", center=[str_len+tp_length+mmi_length, (mmi_gap/2)+(tp_w/2)], width = tp_w, orientation=180, layer=layer, port_type='optical')
    tp_out1.add_port(name="o2", center=[str_len+tp_length+mmi_length+tp_length, (mmi_gap/2)+(tp_w/2)], width = w, orientation=0, layer=layer, port_type='optical')
    output_taper1 = mmi1x2 << tp_out1
    output_taper1.connect("o1", input_mmi.ports["o2"])

    # Define Output Taper 2
    tp_out2 = gf.Component("Output Taper 2")
    xpts_tp2out = [str_len+tp_length+mmi_length, str_len+tp_length+mmi_length+tp_length, str_len+tp_length+mmi_length+tp_length, str_len+tp_length+mmi_length]
    ypts_tp2out = [-((mmi_gap/2)+tp_w), -((mmi_gap/2)+(tp_w/2)+(w/2)), -((mmi_gap/2)+(tp_w/2)-(w/2)), -(mmi_gap/2)]
    tp_out2.add_polygon((xpts_tp2out, ypts_tp2out), layer=layer)
    tp_out2.add_port(name="o1", center=[str_len+tp_length+mmi_length, -((mmi_gap/2)+(tp_w/2))], width = tp_w, orientation=180, layer=layer, port_type='optical')
    tp_out2.add_port(name="o2", center=[str_len+tp_length+mmi_length+tp_length, -((mmi_gap/2)+(tp_w/2))], width = w, orientation=0, layer=layer, port_type='optical')
    output_taper2 = mmi1x2 << tp_out2
    output_taper2.connect("o1", input_mmi.ports["o3"])

    mmi1x2.add_port("o1", center=[str_len, w-w], width = w, orientation=180, layer=layer, port_type='optical')
    mmi1x2.add_port("o2", center=[str_len+tp_length+mmi_length+tp_length, (mmi_gap/2)+(tp_w/2)], width = w, orientation=0, layer=layer, port_type='optical')
    mmi1x2.add_port("o3", center=[str_len+tp_length+mmi_length+tp_length, -((mmi_gap/2)+(tp_w/2))], width = w, orientation=0, layer=layer, port_type='optical')
    x = c << mmi1x2

    x.connect("o1", wg_in.ports["o2"])
    x.connect("o2", wg_thru.ports["o1"])
    x.connect("o3", wg_drop.ports["o1"])
    x.info["mmiWidth"] = float(mmi_width)
    x.info["mmiLength"] = float(mmi_length)
    x.info["mmiGap"] = float(mmi_gap)

    c.add_port(portsName[0], port=wg_in.ports["o1"])
    c.add_port(portsName[1], port=wg_thru.ports["o2"])
    c.add_port(portsName[2], port=wg_drop.ports["o2"])

    ## Flatten GDS to be used in Opti-Compact Model Builder
    c = c.flatten()

    ## Write Final GDS
    c.write_gds('MMI1x2_flatten.gds',with_metadata=True)

    ## Extract and Save Netlist [Connections, Instances, Placements, Ports, Name]
    elems_yaml = c.get_netlist_yaml()
    f = open("Netlist_MMI1x2.yml", "w")
    f.write(elems_yaml)
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-width', type=float, default=0.5, help='Width of the all straight & bend waveguides (default: 0.5 um)')
    parser.add_argument('-taperwidth', type=float, default=1.5, help='Width of interface between In/O straights and MMI region (default: 1 um)')
    parser.add_argument('-taperlength', type=float, default=50, help='Length of the taper section (default: 10 um)')
    parser.add_argument('-mmiwidth', type=float, default=8, help='Width of MMI block in y-direction (default: 2.5 um)')
    parser.add_argument('-mmilength', type=float, default=42, help='Length of MMI block in x-direction (default: 5.5 um)')
    parser.add_argument('-mmigap', type=float, default=2, help='Gap between tapered waveguides in y-direction (default: 0.25 um)')
    parser.add_argument('-straightlength', type=float, default=5, help='Length of straight waveguides of MZI arms (default: 5 um)')
    parser.add_argument('-NetlistNew', action='store_true', default=True, help='Set True to Activate (default: False)')
    args = parser.parse_args()
    main(args)