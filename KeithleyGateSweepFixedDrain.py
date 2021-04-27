# Keithley Gate Sweep (for fixed Vds) for 2400 SourceMeter

# Import Required Packages
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import pyvisa as visa

# Variable intake and assignment
startv = sys.argv[1]
stopv = sys.argv[2]
stepv = sys.argv[3]
fixedv = sys.argv[4]
filename = sys.argv[5]
direction = sys.argv[6]
startvprime = float(startv)
stopvprime = float(stopv)
stepvprime = float(stepv)
steps = (stopvprime - startvprime) / stepvprime 

# Choose GPIB Channel 25 as Drain-Source and 26 as Gate, as well as interface resource for group trigger
rm = visa.ResourceManager()
rm.list_resources()
Keithley = rm.open_resource('GPIB0::25::INSTR')
Keithleygate = rm.open_resource('GPIB0::26::INSTR')
intfc = rm.open_resource('GPIB0::INTFC')

# Initial Communication with instruments and setting data transfer timne limit
Keithley.write("*RST")
Keithleygate.write("*RST")
Keithley.timeout = 25000
Keithleygate.timeout = 25000

# Turn off concurrent functions and set the gate keithley to measure current and source sweep voltage
Keithleygate.write(":SENS:FUNC:CONC OFF")
Keithleygate.write(":ROUT:TERM REAR")
Keithleygate.write(":SOUR:FUNC VOLT")
Keithleygate.write(":SENS:FUNC 'CURR:DC' ")
Keithleygate.write(":SOUR:VOLT:MODE SWE")

# turn off concurrent functions and set keithley to measure current and source fixed voltage
Keithley.write(":SENS:FUNC:CONC OFF")
Keithley.write(":ROUT:TERM REAR")
Keithley.write(":SOUR:FUNC VOLT")
Keithley.write(":SENS:FUNC 'CURR:DC' ")
Keithley.write(":SOUR:VOLT:MODE FIXED")


# set keithley and gate keithey parameters: fixed voltage, compliance current (in A), and data aquisition
Keithley.write(":SOUR:VOLT:LEV ", fixedv)
Keithley.write(":TRIG:COUN ", str(int(steps))) # this tells the measurement to be done at every step on the sweep
Keithley.write(":SENS:CURR:PROT 10E-1")
Keithley.write(":FORM:ELEM CURR")
Keithleygate.write(":SENS:CURR:PROT 10E-1")
Keithleygate.write(":FORM:ELEM CURR")


# set gate keithley sweep parameters: Voltage starting, ending, and spacing values based on input, sweep direction 
Keithleygate.write(":SOUR:VOLT:STAR ", startv)
Keithleygate.write(":SOUR:VOLT:STOP ", stopv)
Keithleygate.write(":SOUR:VOLT:STEP ", stepv)
Keithleygate.write(":SOUR:SWE:RANG AUTO")
Keithleygate.write(":SOUR:SWE:SPAC LIN")
Keithleygate.write(":SOUR:SWE:POIN ", str(int(steps)))
if direction == 'down':
    Keithleygate.write(":SOUR:SWE:DIR DOWN")
else:
    Keithleygate.write(":SOUR:SWE:DIR UP")
Keithleygate.write(":TRIG:COUN ", str(int(steps)))


# Turn output on, set up group trigger, and execute sweep, collecting ACSII current values
Keithley.write(":OUTP ON")
Keithleygate.write(":OUTP ON")
Keithley.write(":ARM:SOUR BUS")
Keithleygate.write(":ARM:SOUR BUS")
Keithley.write(":INIT")
Keithleygate.write(":INIT")
intfc.group_execute_trigger(Keithley, Keithleygate)
yvalues = Keithley.query_ascii_values(":FETC?")
yvaluesgate = Keithleygate.query_ascii_values(":FETC?")

# turn output off
Keithleygate.write(":OUTP OFF")
Keithley.write(":OUTP OFF")
Keithleygate.write(":SOUR:VOLT 0")
Keithley.write(":SOUR:VOLT 0")

# Create xvalues array
xvalues = np.arange(startvprime,stopvprime,stepvprime)
if direction == 'down':
    xvalues = np.flip(xvalues)

# Plot values and save output to data folder in home directory
plt.plot(xvalues,yvalues)
plt.xlabel(' Gate Voltage (V)')
plt.ylabel(' Drain-Source Current (A)')
plt.title('Gate Sweep')
plt.figtext(0.7, 0.2, 'Vds=' + str(fixedv) + 'V', fontsize=15)
plt.show()
np.savetxt(os.getcwd() + '/data/' + filename, (xvalues,yvalues,yvaluesgate)) 
