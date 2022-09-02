from gpio import *
from pwm import *
from direction import *

class Wheel:

    def __init__(self, forwardGpio, backGpio, pwm,
                 pwm_pin, period, duty_cycle):
        
        self.forwardGpio = Gpio(forwardGpio)
        self.backGpio = Gpio(backGpio)
        self.pwm = Pwm(pwm, pwm_pin)
        self.period = period
        self.duty_cycle = duty_cycle

    def init(self):  # Init pwms and gpios
        print("AQUI")
        self.forwardGpio.export()
        print("AQUI 2")
        self.backGpio.export()
        self.forwardGpio.setDirection("out")
        self.backGpio.setDirection("out")
        self.pwm.export()
        
        self.pwm.setPeriod(self.period)
        self.pwm.setDutyCicle(self.duty_cycle)
        self.pwm.start()

    def goForward(self):
        self.backGpio.setValue(0)
        self.forwardGpio.setValue(1)

    def goBack(self):
        self.forwardGpio.setValue(0)
        self.backGpio.setValue(1)

    def stop(self):
        self.backGpio.setValue(0)
        self.forwardGpio.setValue(0)

    def setdutyCicle(self, duty_cy):
        self.pwm.setDutyCicle(duty_cy)
        self.duty_cycle = duty_cy

    def getdutyCicle(self):
        return self.pwm.getDutyCicle()

    def getPeriod(self):
        return self.pwm.getPeriod()

    def run(self, speed, direct):
        if direct == Direction.FORWARD:
            self.goForward()
        elif direct == Direction.BACK:
            self.goBack()
        elif direct == Direction.STOP:
            self.stop()
        else:
            raise Exception
        
        print("tengo que seleccionar %d" %(speed))
        self.setdutyCicle(speed)

    def exit(self):
        self.forwardGpio.unexport()
        self.backGpio.unexport()
        self.pwm.unexport()