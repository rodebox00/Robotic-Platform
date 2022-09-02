from gpio import *
import time 

class Tachometer:
    
    def __init__(self, gpio):
        self.gpio = Gpio(gpio)
    
    def init(self):	#Function to init the associated gpio
        self.gpio.export()	
        self.gpio.setDirection("in")
        
    def getvelowheel(self):
        current_time = time.time()
        ticks = 0
        
        while((time.time() - current_time) < 1):	#Sample during 1 second
            print("Tiempo %f " %(current_time))
            print("Tiempo Actual %f " %(time.time()))
            var = self.gpio.getValue()
            while(var ==  self.gpio.getValue()):
                    if((time.time() - current_time) > 1):
                        ticks = ticks - 1
                        print("hohoho")
                        break
                    pass
            ticks = ticks + 1
        print("HE terminado")
        return ticks
    
    def exit(self):	#Function to unexport the associated gpio
    	self.gpio.unexport()