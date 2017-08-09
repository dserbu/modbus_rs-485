import pymodbus
import serial
import time
import binascii
import struct
from pymodbus.pdu import ModbusRequest
#initialize a serial RTU client instance
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
numCoils=2
slaveUnit=1


client= ModbusClient(method = methName, port=portName,stopbits=stpBits,baudrate=baudSpeed)

startTs = time.time()
try:
    if client.connect():
        print ("Port open")
        regFrame = client.read_holding_registers(regStart, numCoils, unit=slaveUnit)
        print (regFrame.registers[:])
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

    #Connect to the serial modbus server
#print connection

#Starting add, num of reg to read, slave unit.
#result= client.read_holding_registers(0x1B58,90,unit=1)
#print "Respons: %s" %(result)
#closes the underlying socket connection
#client.close()
