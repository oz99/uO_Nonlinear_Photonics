
# Introduction
This Process Design Kit (PDK) allows for users to construct a Nonlinear On Insulator (NOI) layout file in a GDSII file format. NOI is an SiO2/InGaAsP/SiO2/Si stack, with InGaAsP being the guiding layer. InGaAsP is a dispersive material capable of many nonlinear processes. They have yet to be exploited on a system level in Photonic Integrated Circuits (PICs). Here we strive to facilitate PICs on NOI to conduct sensing, (quantum)computation and communications. 

GDSII files are an essential part of the semiconductor fabrication process as it's the file format (schematic) used for lithography. There are two main lithography techniques, photolithography and electron-beam (e-beam) lithography. Photolithography is used in an industrial setting for volume production and Multi-Project Wafer (MPW) runs whereas e-beam lithography is used in small batches for research and academics. E-beam is still an essential part volume manufacturing and/or MPWs as most masks for photolithogry are fabricated using e-beam. 

The layout of this PDK is intended to appease the largest number of users by providing Basic Building Blocks (BBBs), Composite Building Blocks (CBBs) and Basic Technolohy Blocks (BTBs). The BBB design is being done offline. Once verification/characterization of fabricated BBBs is completed we will share the PDK to the public. If you are interested in supporting PDK component development please contact Ozan Oner (ooner083@uottawa.ca).

### Basic Building Blocks (BBBs)
BBBs provide the user fundamental control of devices by using the most elementary building blocks.

### Composite Building Blocks (CBBs)
CBBs provide the user with a collecton of BBBs specified for a function. 

### Basic Technology Blocks (BTBs)
BTBs are physical structures that can have different functions. i.e. if an semiconductor optical amplifier (SOA) is reversed biased it can also be used as a detector. 
