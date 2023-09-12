# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 17:40:09 2023

@author: G.A.S. Flizikowski, gasflizikowski@gmail.com

control test of motor KDC101
"""

from KDC101 import KDC101
import time

def main():
    
    index_number = 0

    # Create an instance of the InstrumentController class
    instrument = KDC101(index_number)
    
    try:
        model = 'PRMTZ8'
        instrument.SetStageModel(model)
        # instrument.SetPosition(150)
        # print(instrument.GetScale())
        #instrument.GetPosition()
        
        #print(instrument.is_moving())
        
        #instrument.GetPosition()
        
        instrument.SendHome()
        instrument.SetPosition(10) #Initial guess
        
        
        #instrument.StepFwd()
        #instrument.StepBwd()
        
        
        # print(instrument.GetStatus())
        # time.sleep(1)
        # instrument.obj.close()
        # # instrument.SetPosition(120)
        #print(instrument.is_moving())
        
        #instrument.get_status_n()
       
    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the instrument connection when done
        instrument.obj.close()
        

if __name__ == "__main__":
    main()