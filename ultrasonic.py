from gpio import *
import time

class Ultrasonic:
    timeMax = 0.235  # Maximun wait of echo

    def __init__(self, triggerGpio, echoGpio):
        self.echo = Gpio(echoGpio)
        self.trigger = Gpio(triggerGpio)

    def init(self):
        self.echo.export()
        self.echo.setDirection("in")
        self.trigger.export()
        self.trigger.setDirection("out")
        print(self.echo.port)
        print(self.trigger.port)

    def echoInMicroseconds(self):
        self.trigger.setValue(0)
        time.sleep(100*10**-6)

        self.trigger.setValue(1)
        time.sleep(10*10**-6)

        self.trigger.setValue(0)

        init_time = time.time()
        end_time = time.time()
        base_time = time.time()

        while self.echo.getValue() == 0:
            init_time = time.time()
            if(base_time + self.timeMax < init_time):
                return -1

        base_time = time.time()

        while self.echo.getValue() == 1:
            end_time = time.time()
            if(base_time + self.timeMax < init_time):
                return -1

        return (end_time-init_time)*10**6

    def distanceInMillimeters(self):
        duration = self.echoInMicroseconds()
        print("Duracion %f" %(duration))
        if(duration == -1):
            return -1
        distance = (duration/2)*0.343
        print("Distance %f" %(distance))
        return distance

    def exit(self):
        self.echo.unexport()
        self.trigger.unexport()