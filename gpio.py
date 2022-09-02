import os

class Gpio:
    exists = False
    
    def __init__(self, gpio):
        self.port = gpio
        # Asume thah the gpio start with an out value (verify!)
        self.direction = "out"
        try:
            self.unexport()
        except: 
            print("ola?")
            
    def export(self):
        if(not (os.path.exists("/sys/class/gpio/gpio%d/" % (self.port)))):
            with open("/sys/class/gpio/export", "w") as fichero:
                fichero.write(str(self.port))
                fichero.close()
        self.exists = True

    def unexport(self):
        if(os.path.exists("/sys/class/gpio/gpio%d/" %(self.port))):
            print("UNEXPORT %d" %(self.port))
            with open("/sys/class/gpio/unexport", "w") as fichero:
                fichero.write(str(self.port))
                fichero.close()
            self.exists = False
        else: raise Exception
        
    def setDirection(self, arg):
        if(arg == "in" or arg == "out" or self.exists == False):
            self.direction = arg
            with open("/sys/class/gpio/gpio%d/direction" % (self.port), "w") as fichero:
                fichero.write(str(arg))
                fichero.close()
        else: raise Exception

    def setValue(self, arg):
        if(self.direction == "in" or self.exists == False):
            raise Exception
        if(arg == 1 or arg == 0):
            with open("/sys/class/gpio/gpio%d/value" % (self.port), "w") as fichero:
                fichero.write(str(arg))
                fichero.close()

    def getDirection(self):
        if(self.exists == True):
            with open("/sys/class/gpio/gpio%d/direction" % (self.port), "r") as fichero:
                val = str(fichero.read())
                fichero.close()
                return va
        else: raise Exception 

    def getValue(self):
        if(self.exists == True):
            with open("/sys/class/gpio/gpio%d/value" % (self.port), "r") as fichero:
                val = int(fichero.read())
                fichero.close()
                return val
        else: raise Exception 
