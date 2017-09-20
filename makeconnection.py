#!/usr/bin/python

import pymodbus     # modbus library for client connection
import time         # check execution time
import struct       # using struct from convert from HEX to IEEE745
import sched        # used to schedule task
import csvwriter    # library to write csv file
import logging

from pymodbus.client.sync import ModbusSerialClient as ModbusClient

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Cliente connection
portName = "/dev/ttyUSB0"
methName = "RTU"
stpBits = 2
baudSpeed = 9600

# Data that needs to be read from register
usedRegister = 7000
slaveUnit = 1
begin_Coils = 0
total_Coils = 4  # tow coils are one register -  32 bits


# Convert IEE745 and dump in a csv file
def writeRegister(startReg, endReg):
    # Obtain all registers divided in 16bit registers
    regFrame = (client.read_holding_registers(usedRegister, endReg, unit=slaveUnit)).registers[:]
    try:
        while startReg < endReg:
            # Convert obtained values to hexadecimal
            packFrame = struct.pack('>HH', regFrame[startReg], regFrame[startReg + 1])

            # Unpack received frame as IEEE754 format (float)
            unpackFrame ="%3f" % struct.unpack('>f', packFrame)

            #create output File
            csvwriter.createFile(startReg)

            #write on the created File
            csvwriter.writeToCSV(startReg,unpackFrame)

            #read next register
            startReg += 2
    except:
        print("ERROR :IEE754 Function - list index out of range")
        raise


# Read register and schedule the delay
def readRegister(local_handler, t):
    try:
        if client.connect():
            writeRegister(begin_Coils, total_Coils)
        else:
            print("Client is not connected")
            client.close()
    except:
        print("Please check the used tty device")
        raise

    #stopTs = time.time()
    #timeDiff = stopTs - startTs
    #print "\nTime execution %s sec" % timeDiff

    # Delay 1 second the recall  scheduler.enterabs(time, priority, action, argument)
    local_handler.enterabs(t + 0.1, 1, readRegister, (local_handler, t + 0.1))


try:
    #startTs = time.time()

    # Connect to the device via modbus
    client = ModbusClient(method=methName, port=portName, stopbits=stpBits, baudrate=baudSpeed)
    handler = sched.scheduler(time.time, time.sleep)
    t = time.time()

    # Indicate the schedule function  scheduler.enter(delay, priority, action, argument)
    handler.enter(0, 1, readRegister, (handler, t))
    handler.run()

except:
    print("Process was stoped unexpectedly ")
