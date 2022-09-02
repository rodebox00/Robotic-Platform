import os

class Pwm:

    exists = False
    duty_cicle = -1
    period = -1

    def __init__(self, pwmchip, pin):
        self.pwmchip = pwmchip
        self.pin = pin
        """try:
            self.unexport()
        except: 
            print("ola?")"""
    
    def export(self):
        if(not (os.path.exists("/sys/class/pwm/pwm-%d:%d" %(self.pwmchip, self.pin)))):
            with open("/sys/class/pwm/pwmchip%d/export" % (self.pwmchip), "w") \
                 as fichero:
                fichero.write(str(self.pin))
                fichero.close()
        self.exists = True
        
    def unexport(self):
        """if(os.path.exists("/sys/class/pwm/pwm-%d:%d" %(self.pwmchip, self.pin))):   
            with open("/sys/class/pwm/pwmchip%d/unexport" % (self.pwmchip), "w") \
                 as fichero:
                fichero.write(str(self.pin))
                fichero.close()
        self.exists = False"""
        pass
        

    def start(self):
        if(self.exists):
            with open("/sys/class/pwm/pwm-%d:%d/enable"
                      % (self.pwmchip, self.pin), "w") as fichero:
                fichero.write(str(1))
                fichero.close()
        else: raise Exception

    def stop(self):
        if(self.exists):
            with open("/sys/class/pwm/pwm-%d:%d/enable"
                      % (self.pwmchip, self.pin), "w") \
                 as fichero:
                fichero.write()
                fichero.close()
        else: raise Exception

    def status(self):
        if(self.exists):
            with open("/sys/class/pwm/pwm-%d:%d/enable"
                      % (self.pwmchip, self.pin), "r") \
                 as fichero:
                var = fichero.read()
                fichero.close()
            return var
        else: raise Exception

    def setPeriod(self, periodo):
        if(periodo < 0 or self.duty_cicle > periodo or not self.exists):
            raise Exception

        with open("/sys/class/pwm/pwm-%d:%d/period"
                  % (self.pwmchip, self.pin), "w") \
             as fichero:
            fichero.write(str(periodo))
            fichero.close()
        self.period = periodo
        
    def getPeriod(self):
        if(self.exists):
            with open("/sys/class/pwm/pwm-%d:%d/period"
                      % (self.pwmchip, self.pin), "r") \
                 as fichero:
                var = int(fichero.read())
                fichero.close()
                return var
        else: Exception

    def setDutyCicle(self, duty):
        print("Duty %d: " %(duty))
        if(duty < 0 or duty > self.period or not self.exists):
            raise Exception(duty, self.period)

        with open("/sys/class/pwm/pwm-%d:%d/duty_cycle"
                  % (self.pwmchip, self.pin), "w") as fichero:
            fichero.write(str(duty))
            fichero.close()
        self.duty_cycle = duty

    def getDutyCicle(self):
        if(self.exists):
            with open("/sys/class/pwm/pwm-%d:%d/duty_cycle"
                      % (self.pwmchip, self.pin), "r") as fichero:
                var = int(fichero.read())
                fichero.close()
                return var
        else: Exception