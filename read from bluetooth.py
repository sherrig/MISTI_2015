import serial
import matplotlib.pyplot as plt
import numpy as np
import binascii

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
    LSB = hex(ord(str(new[2])))
    MSB = hex(ord(str(new[4])))
    LSB2 = repr(LSB).replace("0x", "") [1:-1]
    MSB2 = repr(MSB).replace("0x", "") [1:-1]
    if len(LSB2)<2:
        LSB2 = "0"+LSB2
    number = str(MSB2)+str(LSB2)
    value = int(number,16)
##    if LSB.isupper():
##        raise IndexError
##    if MSB.isupper():
##        raise IndexError
##    try:
##        int(LSB)
##        raise IndexError
##    except ValueError:
##        try:
##            int(MSB)
##            raise IndexError
##        except ValueError:
##        
##            LSB2 = repr(LSB).replace("\\x", "") [1:-1]
##            MSB2 = repr(MSB).replace("\\x", "") [1:-1]
##            if len(LSB2)<2:
##                LSB2 = "0"+LSB2
##            number = str(MSB2)+str(LSB2)
##            value = int(number,16)
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
    if len(LSB5)<2:
        LSB5 = "0" + LSB5
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
    return [data_in, value]

def suggest (value):
    ser.flushInput()
    start_string = '\xffU'
    end_string = '\x00\xff'
    number = hex (value)
    number = repr(number).replace("0x", "") [1:-1]
    if len (number)<2:
        number = '0' + number
    number = binascii.unhexlify(number)
    opposite_bit = hex(255 - int(value))
    opposite_bit = repr(opposite_bit).replace("0x", "") [1:-1]
    if len (opposite_bit)<2:
        opposite_bit = '0' + opposite_bit
    opposite_bit = binascii.unhexlify(opposite_bit)
    output = start_string + number + opposite_bit + end_string
    ser.write(output)
    return output


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
        angle = 10
        weight = number[0:2]
        weight = int(weight)*5.71 - 24.814
        status = number[2]
        status = int(status)

    elif len(number) == 2:
        angle = 10
        weight = number[0]
        weight = int(weight)*5.71 - 24.814
        status = number[1]
        status = int(status)
        

    return [angle, weight, status]




           
def graph():
    angle_success = []
    angle_fail = []
    weight_success = []
    weight_fail = []
    
    while True:
        x = raw_input("Ready? Press 'Y'. ")
        total = 0
        
        if x == 'Y':    #wait until the robot sends some data
            data = getData()
            print data
            value = data[1]
            if value < 31000:   #if the robot is in data collection mode
                stat_list = parse(value)
                if stat_list[2] == 1:   #if the robot succeeded
                    angle_success.append(stat_list[0])
                    weight_success.append(stat_list[1])
                    total += 1
                else:
                    angle_fail.append(stat_list[0])
                    weight_fail.append(stat_list[1])
                    total += 1

                plt.plot(weight_success,angle_success,'bx',weight_fail,angle_fail,'ro')     #scatter points

                #order 1 regression -- only do if there are at least 5 points
                if total >= 5:
                        
                    regression = np.polyfit(weight_success,angle_success,1)     
                    #generate a bunch of values for the line
                    x_vals = range(int(min(weight_success)),int(max(weight_success)))
                    y_vals = []
                    for x in x_vals:
                        y = regression[0]*x + regression[1]
                        y_vals.append(y)
                    plt.plot(x_vals,y_vals,'g')     #plot the regression line

##                #order 2 regression.
##                regression = np.polyfit(weight_success,angle_success,2)
##                x_vals = range(min(weight_success),max(weight_success))
##                y_vals = []
##                for x in x_vals:
##                    y = regression[0]*(x^2) + regression[1]*x + regression[2]
##                    y_vals.append(y)
##                plt.plot(x_vals,y_vals,'g')
                
                plt.show()

            else: #the robot is in asking mode
                temp = str(value)
                num = int(temp[len(temp)-2:len(temp)])  #look at the last 2 digits of the getData number
                weight = num*5.71 - 24.814

                
                #order 1 regression:
                regression = np.polyfit(weight_success,angle_success,1) 

                #find the corresponding angle from the regression
                angle = weight*regression[0] + regression[1]
                offset = int((angle - 10.142)/3.51)

##                #order 2:
##                regression = np.polyfit(weight_success,angle_success,2)
##                angle = regression[0]*(weight^2) + regression[1]*weight + regression[2]
##                offset = int((angle - 10.142)/3.51)
                

                #now send the robot the angle offset
                print offset
                suggest(offset)
                
                
    
