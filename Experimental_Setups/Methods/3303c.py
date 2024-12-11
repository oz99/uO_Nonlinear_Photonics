
#INITIALIZATION
import math
import pyvisa
import time

#Keithley
from pymeasure.instruments.keithley import Keithley2400
sm = Keithley2400("USB0::0x05E6::0x2450::04577394::INSTR")
#Siglet
pm = pyvisa.ResourceManager()
pm.list_resources()
inst = pm.open_resource('USB0::0xF4EC::0x1430::SPD3EGGD6R3960::INSTR',)
inst.write("INST CH1")
print(inst.query("INST?"))

#set amperage on siglet
inst.write("CH1:CURR 0.8")
inst.write("OUTP CH1,ON")
print(inst.query("CH1:CURR?"),"Amps")

setpoint = 30.0 #temperature setpoint
pi = 0.01 #voltage increment
pmvolt = 1 #initial voltage setting
roundTemp = 1
stabletime= 10
time.sleep(20)#pause for calibration

while setpoint > roundTemp:
    #resistance to temperature calculation
    RT = sm.resistance
    print(RT, "ohms")
    temp = (-3.9083e-3 + math.sqrt((3.9083e-3**2)-(4*-5.775e-7*((RT/100)-1))))/(2*-5.775e-7) #pt100 datasheet equation
    roundTemp = round(-temp-3.18559, 6)
    inst.write("CH1:VOLT " + str(pmvolt))
    vnow = inst.query("CH1:VOLT?")#reads voltage value
    print(vnow, "volts", "while temperature is", roundTemp,"C")
    pmvolt+=pi
    time.sleep(7)#allow the siglet to reach commanded voltage
else: 
    print("setpoint was reached")
    sm.beep(1000, 2)
