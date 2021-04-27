# Keithley-IV-Sweep
Python (PyVisa) script for IV (Current-Voltage) measurements on a Keithley 2400 (GPIB/SCIP communication).

Instructions:

  1. Install the necessary Python libraries and drivers (list below)

  2. Place the KeithleyIVSweep.py, KeithleyIVSweepFixedGate.py, and/or KeithleyGateSweepFixedGate.py files in your home (or current Python) directory.
  
  3. From the command line, run one of the following commands (depending on file):
  
    a. 'python KeithleyIVSweep.py startV stopV stepV outputfile direction' 
    b. 'python KeithleyIVSweepFixedGate.py startV stopV stepV gateV outputfile direction'
    c. 'python KeithleyGateSweepFixedDrain.py startgateV stopgateV stepgateV drainV outputfile direction'
  
  4. For example, a gate from -20 V to 20 V with a step voltage of 1 V and drain voltage of 0.5 V would be obtained by running 'python KeithleyGateSweepFixedDrain.py -20 20 1 0.5 Hello.txt up' where the output text file named Hello.txt would be created and stored in your home (or current Python) directory.
  
  5. you can also use the jupyter notebook file: "2400 Keithley Mobility.ipynb" which has built in plotting and analysis features. 
  

### List of all the required programs, drivers and packages required for the succesful communication and control of the Keithley 2400 Duo in order to conduct Semiconductor mobility measurements.

    1. python installation and the following packages. These are easily installed with "pip install package"
        a. pyvisa
        b. scipy
        c. matplotlib
        d. numpy
    3. VISA implementation: https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html#346210
    4. NI GBIP driver: https://www.ni.com/en-us/support/downloads/drivers/download.ni-488-2.html#345631
    
### Changing parameters and controlling the Keithley from the command line

You can modify your version of the python scripts to do different things and even run the instruments from the command line. Start by taking a look at the existing scripts and understanding how the instruments and the VISA driver communicate. Then, read through the this manual (http://research.physics.illinois.edu/bezryadin/labprotocol/Keithley2400Manual.pdf) which will indicate other commands that the keithley will accept and in the form to deliver them. 
    
