# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 09:49:30 2023

@author: G.A.S. Flizikowski, gasflizikowski@gmail.com

Driver for Newport 2918c with connection via pyvisa usb 
"""

import pyvisa as visa
import matplotlib.pyplot as plt
import numpy as np
import time

class Newport2936R:
        
    def __init__(self, usb_address):
        self.usb_address = usb_address
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.open_resource(usb_address)
        
    def write(self, cmd_str):
        try:
            self.instrument.write(cmd_str)
            print("({}) write command successfully sent to Power Meter.".format(cmd_str))
        except:
            print("ERROR: Failed to send write command to Power Meter. Try using the built-in __write__() function.")
        
    def read(self, cmd_str):
        try:
            out = self.instrument.query(cmd_str)
            print("{} read command successfully sent to Power Meter.".format(cmd_str))
            print(out)
        except:
            print("ERROR: Failed to send read command to Power Meter. Try using the built-in __query__() function.")
            print(out)       
      
    def GetInfo(self):
        try:
            info = self.instrument.query('*IDN?')
            print(info)
        except:
            print("Unable to retreive instrument information.")

    def GetChannel(self):
        try:
            chn = self.instrument.query('PM:CHANnel?')
            print('Current channel is number {}'.format(chn))
        except:
            print("Unable to retreive instrument information.")
            
    def SetChannel(self, channel):
    # channel = 1 or 2
        self.instrument.write('PM:CHANnel {}'.format(channel))
        chn = int(self.instrument.query('PM:CHANnel?'))
        if chn==channel:
            print('Channel has been correctly set to {}.'.format(channel))
        else:
            print('ERROR: Unable to set channel to desired value.')
            
    def GetLambda(self):
        try:
            lbd = self.instrument.query('PM:Lambda?')
            print('Current lambda is {} nm'.format(lbd))
        except:
            print("Unable to retreive instrument information.")
            
    def SetLambda(self, channel, lamb):
        Newport2936R.SetChannel(self, channel)
        self.instrument.write('PM:Lambda {}'.format(lamb))
        lbd = int(self.instrument.query('PM:Lambda?'))
        if lbd==lamb:
            print('Lambda of channel {} has been correctly set to {} nm.'.format(channel,lamb))
        else:
            print('ERROR: Unable to set channel to desired value.')    
            
    def GetPowerCH1(self):
        try:
            pwr = self.instrument.query('PM:PWS?')
            pwr = float(pwr.split()[0])
            return pwr
        except:
            print("Unable to retreive instrument information.")
            
    def GetPowerCH2(self):
        try:
            pwr = self.instrument.query('PM:PWS?')
            pwr = float(pwr.split()[2])
            return pwr
        except:
            print("Unable to retreive instrument information.")
            
    def GetPowerBoth(self):
        try:
            pwr1 = Newport2936R.GetPowerCH1(self)
            pwr2 = Newport2936R.GetPowerCH2(self)
            return print(pwr1,pwr2)
        except:
            print("Unable to retreive instrument information.")
            
    ##Add functions to add sensitivity input
            
    
            
    def close(self):
        self.instrument.close()     
            
if __name__ == "__main__":
    instrument_address = 'USB0::0x104D::0xCEC7::NI-VISA-40005::RAW'
    
    # Create an instance of the InstrumentController class
    instrument = Newport2936R(instrument_address)

    try:
        # Query the instrument's identity
        identity = instrument.query_identity()
        print(f"Instrument identity: {identity}")

    finally:
        # Close the instrument connection when done
        instrument.close()