import pymodbus
#import serial
import time                                 # check execution time
import struct                               # ussing struct from convert from HEX to IEEE745
import binascii
from ctypes import create_string_buffer     # avoiding buffer overhead by providing a buffer that was created earlier
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


#Cliente connection
portName="/dev/ttyRasPi"
methName="RTU"
stpBits=2
baudSpeed=9600

#Time calculation
regsSp = 10

#Data that needs to be read from register
regStart=0x1B58 #7000
numCoils=16
slaveUnit=1


client= ModbusClient(method = methName, port=portName,stopbits=stpBits,baudrate=baudSpeed)

startTs = time.time()
try:
    if client.connect():
        #Obtain all registers splited in 16bit registers
        regFrame = (client.read_holding_registers(regStart, numCoils, unit=slaveUnit)).registers[:]

        # Convert obtained values to hexadecimal
        packFrame = struct.pack('>HH', regFrame[0], regFrame[1])

        # Unpack received frame as IEEE754 format (float)
        unpackFrame = struct.unpack('>f', packFrame)

        # Print inforamtion from unpacked frame
        print "%.3f V" % unpackFrame
        # Print the entire register with all coils
        print regFrame

        #z = "%s%s" % (coil0)
        #''.join(chr(int(x, 16)) for x in regFrame.split())
    else:
        print("results were none")
        client.close()
except:
    print("Unknown Exception")
    raise

#Calculate time execution
stopTs = time.time()
timeDiff = stopTs - startTs
print "Time execution %s sec" % timeDiff