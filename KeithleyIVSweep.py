# Keithley IV Sweep for 2400 SourceMeter

# Import Packages
import sys
import pyvisa as visa
import matplotlib.pyplot as plt
import numpy as np

# Variable intake and Assignment
startv = sys.argv[1]
stopv = sys.argv[2]
stepv = sys.argv[3]
filename = sys.argv[4]
instr = sys.argv[5]
direction = sys.argv[6]
startvprime = float(startv)
stopvprime = float(stopv)
stepvprime = float(stepv)
steps = (stopvprime - startvprime) / stepvprime 

# Identify insstruments and assign them as a resource based on variable input
rm = visa.ResourceManager()
rm.list_resources()
if instr == 'gate':
    Keithley = rm.open_resource('GPIB0::26::INSTR')
else:
    if instr == 'source':
        Keithley = rm.open_resource('GPIB0::25::INSTR')
    else:
        print('please select an instrument: gate or source')
    
# Initial communication with instrument and delay timer set. 
Keithley.write("*RST")
Keithley.timeout = 25000

# Turn off concurrent functions and set sensor to current with fixed voltage
Keithley.write(":SENS:FUNC:CONC OFF")
Keithley.write(":ROUT:TERM REAR")
Keithley.write(":SOUR:FUNC VOLT")
Keithley.write(":SENS:FUNC 'CURR:DC' ")

# Voltage starting, ending, and spacing values based on input
Keithley.write(":SOUR:VOLT:STAR ", startv)
Keithley.write(":SOUR:VOLT:STOP ", stopv)
Keithley.write(":SOUR:VOLT:STEP ", stepv)
Keithley.write(":SOUR:SWE:RANG AUTO")
Keithley.write(":FORM:ELEM CURR")

# Set compliance current (in A), sweep direction, and data acquisition
Keithley.write(":SENS:CURR:PROT 1")
Keithley.write(":SOUR:SWE:SPAC LIN")
Keithley.write(":SOUR:SWE:POIN ", str(int(steps)))
if direction == 'down':
    Keithleygate.write(":SOUR:SWE:DIR DOWN")
else:
    Keithleygate.write(":SOUR:SWE:DIR UP")
Keithley.write(":TRIG:COUN ", str(int(steps)))


# Set sweep mode and turn output on
Keithley.write(":SOUR:VOLT:MODE SWE")
Keithley.write(":OUTP ON")

# Initiate sweep, collect ACSII current values, and turn output off
result = Keithley.query(":READ?")
yvalues = Keithley.query_ascii_values(":FETC?")
Keithley.write(":OUTP OFF")
Keithley.write(":SOUR:VOLT 0")

# Create xvalues array
xvalues = np.arange(startvprime,stopvprime,stepvprime)

# Plot values and save output to data folder in parent directory
plt.plot(xvalues,yvalues)
plt.xlabel(' Drain-Source Voltage (V)')
plt.ylabel(' Drain-Source Current (A)')
plt.title('IV Curve')
plt.show()
np.savetxt(os.getcwd() + '/data/' + filename, (xvalues,yvalues)) 