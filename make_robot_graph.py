#import matplotlib.pyplot as plt
#import numpy
import serial

#xxyyz --> this is the form that the incoming bytes will be in
#z = 1: success, 0: failure
#xx = angle, needs to be converted
#yy = weight, needs to be converted

#input will be some 5 digit number


#initialize and open port
ser = serial.Serial()
ser.port = 'COM5'
ser.baudrate = 57600
ser.timeout = 0.5
ser.open()
ser.flushInput()


#Read data input
def readPacket(data_in):
    if len(data_in)>12:
        new = data_in[len(data_in)-6:len(data_in)]
    else:
        new = data_in
    LSB = new[2]
    MSB = new[4]
    LSB2 = repr(LSB).replace("\\x", "") [1:-1]
    MSB2 = repr(MSB).replace("\\x", "") [1:-1]
    number = str(MSB2)+str(LSB2)
    value = int(number,16)
    return value

    
    
def readPacketInverse(data_in):
    if len(data_in)>12:
        new = data_in[len(data_in)-6:len(data_in)]
    else:
        new = data_in
    LSB_in = new[3]
    MSB_in = new[5]
    LSB2_in = repr(LSB_in).replace("\\x", "") [1:-1]
    LSB3 = 255 - int(LSB2_in, 16)
    LSB4 = hex(LSB3)
    LSB5 = repr(LSB4).replace("0x", "") [1:-1]
    MSB2_in = repr(MSB_in).replace("\\x", "") [1:-1]
    MSB3 = 255 - int(MSB2_in, 16)
    MSB4 = hex(MSB3)
    MSB5 = repr(MSB4).replace("0x", "") [1:-1]
    number = str(MSB5)+str(LSB5)
    
    value = int(number,16)
    return value

def getData():
    data_in = ser.read(400)
    try:
        value = readPacket(data_in)
    except ValueError:
        value = readPacketInverse(data_in)
    except IndexError:
        try:
            value = readPacketInverse(data_in)
        except:
            value = data_in
    ser.flushInput()        
    return value

def suggest (value):
    ser.write(value)

def parse(number):
    number = str(number)
    if len(number) == 5:

        angle = number[0:2]
        angle = int(angle)*3.51 + 10.142
        weight = number[2:4]
        weight = int(weight)*5.71 - 24.814
        status = number[4]
        status = int(status)

    elif len(number) == 4:
        angle = number[0:1]
        angle = int(angle)*3.51 + 10.142
        weight = number[1:3]
        weight = int(weight)*5.71 - 24.814
        status = number[3]
        status = int(status)

    elif len(number) == 3:
        angle = 0
        weight = number[0:2]
        weight = int(weight)*5.71 - 24.814
        status = number[2]
        status = int(status)

    elif len(number) == 2:
        angle = 0
        weight = number[0]
        weight = int(weight)*5.71 - 24.814
        status = number[1]
        status = int(status)
        

    return [angle, weight, status]


def graph():
    stats = []
    while len(stats) < 5:
        try:
            value = getData()
            number = parse(value)
            stats.append(number)
            print number
        except:
            continue
    print stats
    
        
            
