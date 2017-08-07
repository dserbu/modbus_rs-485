import pymodbus
import serial
from pymodbus.pdu import ModbusRequest
#initialize a serial RTU client instance
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

#count= the number of registers to read
#unit= the slave unit this request is targeting
#address= the starting address to read from

client= ModbusClient(method = "rtu", port="/dev/ttyUSB0",timeout=0.5,stopbits = 1, bytesize = 8,baudrate=19200)

#Connect to the serial modbus server
connection = client.connect()
print connection

#Starting add, num of reg to read, slave unit.
#result= client.read_holding_registers(0x1B58,2)
result= client.read_holding_registers(0x1B58,2,unit=1)

print "AAAAAAAAAaa: %s" %(result)
#closes the underlying socket connection
client.close()