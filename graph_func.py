def graph():
    angle_success = []
    angle_fail = []
    weight_success = []
    weight_fail = []
    
    while True:
        x = raw_input("Ready? Press 'Y'. ")
        
        if x == 'Y':    #wait until the robot sends some data
            value = getData()
            if value < 63000:   #if the robot is in data collection mode
                stat_list = parse(value)
                if stat_list[2] == 1:   #if the robot succeeded
                    angle_success.append(stat_list[0])
                    weight_success.append(stat_list[1])
                else:
                    angle_fail.append(stat_list[0])
                    weight_fail.append(stat_list[1])

                plt.plot(weight_success,angle_success,'bx',weight_fail,angle_fail,'ro')     #scatter points

                #order 1 regression
                regression = np.polyfit(weight_success,angle_success,1)     
                #generate a bunch of values for the line
                x_vals = range(min(weight_success),max(weight_success))
                y_vals = []
                for x in x_vals:
                    y = regression[0]*x + regression[1]
                    y_vals.append(y)
                plt.plot(x_vals,y_vals,'g')     #plot the regression line

##                #order 2 regression
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
                
                
                
                
                
            
