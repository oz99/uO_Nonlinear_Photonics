# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 10:45:48 2023

@author: rboydlabo
"""

import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
import time

from Newport2936R import Newport2936R

def main():
    instrument_address = 'USB0::0x104D::0xCEC7::NI-VISA-40005::RAW'

    # Create an instance of the InstrumentController class
    instrument = Newport2936R(instrument_address)

    try:      
        # instrument.GetInfo()
        # instrument.GetChannel()
        # instrument.SetChannel(2)
        # instrument.GetLambda()
        # instrument.SetLambda(1, 1310)
        # instrument.GetLambda()
        # instrument.GetPowerCH1()
        # instrument.GetPowerCH2()
        instrument.GetPowerBoth()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the instrument connection when done
        instrument.close()

if __name__ == "__main__":
    main()
