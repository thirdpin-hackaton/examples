import minimalmodbus
import serial.tools.list_ports
import time

mb = None
minimalmodbus.BAUDRATE = 9600
minimalmodbus.TIMEOUT = 1
minimalmodbus.PARITY = 'E'
def FindDevice():
    global mb

    for p in list(serial.tools.list_ports.comports()):
        if (p.vid == 0x0403) and (p.pid == 0x6015):
        #if (p.vid == 0x1b5c) and (p.pid == 0x0104):
            mb = minimalmodbus.Instrument(str(p.device), 247, mode='rtu')
            if not mb.serial.is_open:
                mb.serial.open()
            print('Device Found!')
            return True
    
    return False


FindDevice()

while(1):
    # mb.write_bit(0,1, functioncode=0x05)
    # time.sleep(1)
    # mb.write_bit(8, 1, functioncode=0x05)
    # time.sleep(1)

	humi      = mb.read_float(0x0016,numberOfRegisters = 2, functioncode=0x04)
	humi1      = mb.read_float(0x0014,numberOfRegisters = 2, functioncode=0x04)
	humi2      = mb.read_float(0x0012,numberOfRegisters = 2, functioncode=0x04)
	temp      = mb.read_float(0x0022,numberOfRegisters = 2, functioncode=0x04)
	temp1      = mb.read_float(0x0034,numberOfRegisters = 2, functioncode=0x04)
	temp2      = mb.read_float(0x0020,numberOfRegisters = 2, functioncode=0x04)
	temp3      = mb.read_float(0x0018,numberOfRegisters = 2, functioncode=0x04)

	print('temp:   %.1f\tC'  % float(temp))
	print('temp1:   %.1f\tC'  % float(temp1))
	print('temp2:   %.1f\tC'  % float(temp2))
	print('temp3:   %.1f\tC'  % float(temp3))
	print('humi:   %.1f\tC'  % float(humi))
	print('humi1:   %.1f\tC'  % float(humi1))
	print('humi2:   %.1f\tC'  % float(humi2))
	print('\n')
    
	time.sleep(1)
    # status       = mb.read_register(start_reg + 1, functioncode=0x03)
    # current      = mb.read_register(start_reg + 2, functioncode=0x03)
    # power        = mb.read_register(start_reg + 3, functioncode=0x03)
	#print(address)

	