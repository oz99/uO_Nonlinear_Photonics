# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 10:19:55 2023

@author: rboydlabo
"""

import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
import time
import logging

# Importing custom libraries for the optical instruments
from OSA import AQ6315B
from Newport2936R import Newport2936R
from KDC101 import KDC101
import csv
import datetime



# Constants for power adjustment loop
MAX_ITERATIONS = 100  # Max iterations for reaching the target power level
TOLERANCE = 1e-6  # Tolerance for difference between actual and target power level

# Initialize logging
logging.basicConfig(filename='lab_log.log', level=logging.INFO)

# Function to adjust the power level to the desired value


# Main function
def main():
    # Initiali

    pm_address = 'USB0::0x104D::0xCEC7::NI-VISA-10002::RAW'
    
    pm =  Newport2936R(pm_address)