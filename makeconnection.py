#!/usr/bin/python

import pymodbus                             # modbus library for client connection
import time                                 # check execution time
import struct                               # ussing struct from convert from HEX to IEEE745
import sched                                # used to get information every second

from pymodbus.client.sync import ModbusSerialClient as ModbusClient

#Cliente connection
portName="/dev/ttyRasPi"
methName="RTU"
stpBits=2
baudSpeed=9600

# Data that needs to be read from register
regStart = 0x1B58   # 7000
slaveUnit = 1
begin_Coils = 0
total_Coils = 92     # tow coils are one register -  32 bits

#Print requiered information
def printReg(startReg,convertedReg):
    print 'Register', 7000 + startReg, 'is %.3f' % convertedReg

# Convert IEE745 with the ussage of the structure
def IEE754(startReg,endReg):
    # Obtain all registers divided in 16bit registers
    regFrame = (client.read_holding_registers(regStart, endReg, unit=slaveUnit)).registers[:]
    try:
        while startReg < endReg:
            # Convert obtained values to hexadecimal
            packFrame = struct.pack('>HH', regFrame[startReg], regFrame[startReg + 1])
            # Unpack received frame as IEEE754 format (float)
            unpackFrame = struct.unpack('>f', packFrame)
            printReg(startReg,unpackFrame)
            # Increment the loop, 0,2,4 etc
            startReg += 2
    except:
        print("ERROR :IEE754 Function - list index out of range")
        raise

# Read register and schedule the delay
def readRegister(local_handler, t):
    try:
        if client.connect():
            IEE754(begin_Coils,total_Coils)
        else:
            print("results were none")
            client.close()
    except:
        print("Unknown Exception")
        raise
    
    stopTs = time.time()
    timeDiff = stopTs - startTs
    print "\nTime execution %s sec" % timeDiff

    #Delay 1 second the recall
    local_handler.enterabs(t + 0.1, 1, readRegister, (local_handler, t+0.1))


try:
        startTs = time.time()
        # Connect to the device via modbus
        client= ModbusClient(method = methName, port=portName,stopbits=stpBits,baudrate=baudSpeed)
        handler = sched.scheduler(time.time, time.sleep)
        t = time.time()
        #Indicate the schedule function
        handler.enter(0, 1, readRegister, (handler, t))
        handler.run()
except:
    print("Unexpected ERROR:")
