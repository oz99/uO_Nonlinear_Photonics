# -*- coding: utf-8 -*-
"""
Created 2023-08-30

@author: G.A.S. Flizikowski, gasflizikowski@gmail.com
        Ozan W. Oner, ooner083@uottawa.ca

Device file for the Ando OSA
"""

import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
import time

class AQ6315B:

    def __init__(self, visa_address):
        self.visa_address = visa_address
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.open_resource(visa_address)
             
#    def __del__(self):
#        #Closes the channel
#        self.close()
                   
    def reset_inst(self):
        try: 
            self.instrument.write('*RST')
            print('OSA successfully reset.')
        except:
            print('Unable to reset OSA.')
            
    def GetInfo(self):
        # identifies manufacturer, model, PN, firmware version.
        try:
            info = self.instrument.query('*IDN?')
            print(info)
        except:
            print("Unable to retreive instrument information.")
                
    def write(self, cmd_str):
        try:
            self.instrument.write(cmd_str)
            print("({}) write command successfully sent to OSA.".format(cmd_str))
        except:
            print("ERROR: Failed to send write command to OSA. Try using the built-in __write__() function.")
        
    def read(self, cmd_str):
        try:
            out = self.instrument.query(cmd_str)
            print("{} read command successfully sent to OSA.".format(cmd_str))
            print(out)
        except:
            print("ERROR: Failed to send read command to OSA. Try using the built-in __query__() function.")
            
    def GetStartWavelength(self):
        WL = self.instrument.query('STAWL?')
        WL = float(WL)#*1e9
        return WL
    
    def SetStartWavelength(self, wavelength):
        StopWL = self.instrument.query('STPWL?')
        StopWL = float(StopWL)#*1e9
        
        if wavelength >= StopWL:
            span = self.instrument.query('SPAN?')
            span = float(span)#*1e9
            #self.instrument.write(':sense:wav:stop {} M'.format((wavelength+span)*1e-9))
            self.instrument.write('STPWL{}'.format((wavelength+span)))
        wavelength = round(wavelength,2)
        #self.instrument.write(':sense:wav:star {} M'.format(wavelength*1e-9))
        self.instrument.write('STAWL{}'.format(wavelength))
        time.sleep(1)
        WL = AQ6315B.GetStartWavelength(self)
        if WL==wavelength:
            print('Start wavelength has been correctly set to {} nm.'.format(wavelength))
        else:
            print('ERROR: Unable to set start wavelength to desired value.')
    
    def GetStopWavelength(self):
        WL = self.instrument.query('STPWL?')
        WL = float(WL)#*1e9
        return WL
        
    def SetStopWavelength(self, wavelength):
        StartWL = self.instrument.query('STAWL?')
        StartWL = float(StartWL)#*1e9
        if wavelength <= StartWL:
            span = self.instrument.query('SPAN?')
            span = float(span)#*1e9
            #self.instrument.write(':sense:wav:star {} M'.format((wavelength-span)*1e9))
            self.instrument.write('STAWL{}'.format((wavelength-span)))
        #self.instrument.write('STPWL{}'.format(wavelength/1e9))
        self.instrument.write('STPWL{}'.format(wavelength))
        time.sleep(1)
        WL = AQ6315B.GetStopWavelength(self)
        if WL == wavelength:
            print('Stop wavelength has been correctly set to {} nm'.format(wavelength))
        else:
            print('ERROR: Unable to set stop wavelength to desired value.')
         
    def GetCenterWavelength(self):
        WL = self.instrument.query('CTRWL?')
        WL = float(WL)#*1e9
        return WL
    
    def SetCenterWavelength(self, wavelength):
        wavelength = round(wavelength,2)
        self.instrument.write('CTRWL{}'.format(wavelength))
        time.sleep(1)
        WL = AQ6315B.GetCenterWavelength(self)
        if abs(WL-wavelength)<=0.1:
            print('Center wavelength has been set correctly to {} nm'.format(wavelength))
        else:
            print('ERROR: Unable to set center wavelength to desired value.')
    
    def GetSpanWavelength(self):
        WL = self.instrument.query('SPAN?')
        WL = float(WL)#*1e9
        return WL
    
    def SetSpanWavelength(self, wavelength):
        wavelength = round(wavelength,2)
        self.instrument.write('SPAN{}'.format(wavelength))
        time.sleep(1)
        WL = AQ6315B.GetSpanWavelength(self)
        if abs(WL-wavelength)<0.5:
            print('Span wavelength has been set correctly.')
        else:
            print('ERROR: Unable to set span wavelength to desired value.')

    def GetReference(self):
        refGet = self.instrument.query('REFL?')
        refGet = float(refGet)#*1e9
        return refGet

    # def SetReference(self, refSet):
    #     self.instrument.write('REFL-{}'.format(refSet))       
    #     time.sleep(1)
    #     refGet = AQ6315B.GetReference(self)
    #     if refGet == refSet:
    #         print('reference level is set correctly to {}'.format(refGet))
    #         else:
    #             print('ERROR: Unable to set reference level to desired value.') 
    
    def GetResolution(self):
        WL = self.instrument.query('RESLN?')
        WL = float(WL)#*1e9
        return WL
    
    def SetResolution(self, rbwSet):
        self.instrument.write('RESLN{}'.format(rbwSet))
        time.sleep(1)
        rbwGet = AQ6315B.GetResolution(self)
        if rbwGet == rbwSet:
            print('Resolution is set correctly to {}'.format(rbwSet))
        else:
            print('ERROR: Unable to set resolution to desired value.')        
    
    def GetSensitivity(self):
        sens = self.instrument.query('SENS?')
        sens = int(sens)
        return sens
    
    def SetSensitivity(self, sensitivity): #takes integer argument for sensitivity.
        self.instrument.write('{}'.format(sensitivity))
        time.sleep(1)
        # truesens = AQ6315B.GetSensitivity(self)
        # if int(truesens) == sensitivity:
        #     print('Sensitivity successfully set to {}.'.format(sensitivity))
        # else:
        #     print('ERROR: Unable to set desired sensitivity.')
        
  
    def GetPoints(self):
        PT = self.instrument.query('SMPL?')
        return int(PT)
    
    def SetPoints(self, Point):
        self.instrument.write('SMPL{}'.format(Point))
        time.sleep(1)
        PT = AQ6315B.GetPoints(self)
        if PT==Point:
            print('Point has been set correctly to {}'.format(Point))
        else:
            print('ERROR: Unable to set Point to desired value')
        
    def GetAverage(self):
        PT = self.instrument.query('AVG?')
        return int(PT)
    
    def SetAverage(self, Average):
        self.instrument.write('AVG{}'.format(Average))
        time.sleep(1)
        AVG = AQ6315B.GetAverage(self)
        if AVG==Average:
            print('Averaging times has been set correctly to {}'.format(Average))
        else:
            print('ERROR: Unable to set Averaging times to desired value')        
        
    def SingleScan(self):
        self.instrument.clear()
        try:
            self.instrument.write('SGL')
            #AQ6315B.write(self, '*CLS') CHECK EQUIPMENT SCREEN
            #AQ6315B.write(self, 'INIT') CHECK EQUIPMENT SCREEN
            print('---------------------------------------')
            print('Scan commands successfully sent to OSA.')
        except:
            print("ERROR: Unable to send single scan commands to OSA.")   
        
    # def GetTrace(self, scan_exists):
    #     # self.instrument.clear()
    #     # AQ6315B.SetStartWavelength(self,1525)
    #     # AQ6315B.SetStopWavelength(self,1575)
    #     #AQ6315B.SetPoints(self,1001)
        
    #     #This section saves the current scan on the Ando. 
    #     #It will start a single scan trace if there is no current scan
    #     if scan_exists == 1:
    #         pass
    #     else:
    #         AQ6315B.SingleScan(self)
            
    def GetIntensity(self):
        yvals = self.instrument.query('LDATA')
        yvals = yvals.split(',')
        yvals[-1] = yvals[-1][:-2] # deletes terminating \n in string of last element
        
        for i,y in enumerate(yvals):
            yvals[i] = float(y) # convert data strings to float values
            yvals = np.array(yvals) # convert to numpy array   
        return yvals
    
    def GetWavelength(self):
        xvals = self.instrument.query('WDATA')
        xvals = xvals.split(',')
        xvals[-1] = xvals[-1][:-2] # deletes terminating \n in string of last element
        
        for i,y in enumerate(xvals):
            xvals[i] = float(y) # convert data strings to float values
        xvals = np.array(xvals) # convert to numpy array
        return xvals
    
    def PlotScan(self):
        wavelength = AQ6315B.GetWavelength(self)
        intensity = AQ6315B.GetIntensity(self)
        
        plt.scatter(wavelength[1:-1], intensity[1:-1])
        plt.grid()
        return plt.show()  
    
    def ExportScan(self, filename_str):
        wavelength = AQ6315B.GetWavelength(self)
        intensity = AQ6315B.GetIntensity(self)
        name = filename_str
        np.savetxt('{}'.format(name), np.column_stack((wavelength[1:-1], intensity[1:-1])),fmt='%s',delimiter='\t')
        return print('Data exported.')
        
        
        
    def close(self):
        self.instrument.close()     
        
        
        
if __name__ == "__main__":
    instrument_address = "GPIB0::1::INSTR"
    
    # Create an instance of the InstrumentController class
    instrument = AQ6315B(instrument_address)

    try:
        # Query the instrument's identity
        identity = instrument.query_identity()
        print(f"Instrument identity: {identity}")

    finally:
        # Close the instrument connection when done
        instrument.close()
        
                 