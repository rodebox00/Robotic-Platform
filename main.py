from ultrasonic import *
from wheel import *
from direction import *
from tachometer import *
import time

gpios = [177, 178, 208, 164, 165, 166, 234, 209]
gpios = [177, 178, 208, 164, 165, 166] #Gpos that we are going to use
tachometerGpios = [208, 177] #Gpios that we use for the tachometers <<tachometer left, tachometer right>>
ultrasonicGpios = [234, 209] #Gpos that we use with the ultrasonic <<Gpio trigger, Gpio echo>>
pwmchips = [2]  
pwms_pines = [1, 0]   #Pines of the pwmchips that we use <<[left wheel, right wheel]>>
period = 4000   #Period of time for pwms
gpios_out = [164, 165, 166, 178]    #What gpios are established as out
gpios_run_forward = [178, 166]    #What gpios are established to move the robot forward <<[left wheel, right wheel]>>
gpios_run_back = [164, 165]    #What gpios are established to move the robot back <<[left wheel, right wheel]>>
KP = 10
desired_speed = 2   #Default desired speed
twisting = False    #Know if the platform is twisting or not
ttiwst = 0

def proportional_speed(wheel, tachometer):  #Function to calculate that the two wheels go synchronized
    global desired_speed
    e = desired_speed - tachometer.getvelowheel()
    u = KP * e
    vel = u + wheel.getdutyCicle()
    vel = max(0,vel)
    vel = min(period,vel)
    print(u)
    wheel.setdutyCicle(vel)
    
def calcDesiredSpeed(lwheel, rwheel, lTacho, rTacho):
    global period, desired_speed
    lwheel.run(period, Direction.FORWARD)  #We set the max dutyCicle to get the max velocity
    print("1")
    rwheel.run(period, Direction.FORWARD)  
    print("2")
    l = lTacho.getvelowheel()
    r = rTacho.getvelowheel()
    print("3")
    if(r > l): desired_speed = l
    else: desired_speed = r
    lwheel.run(int(period/2), Direction.FORWARD)  #We set the half max dutyCicle to get the max velocity
    rwheel.run(int(period/2), Direction.FORWARD)

def manageTwist(val, leftwheel, rightwheel):
    global twisting, ttiwst
    
    if ((val == -1 or val > 310) and twisting and (time.time()-ttiwst) > 0.35):
        rightwheel.goForward()
        twisting = False
    elif ((val > 60 and val < 310) and twisting):
        rightwheel.goForward()
        twisting = False
    elif (val  < 50 and not twisting):
        rightwheel.goBack()
        twisting = True
    elif (val  < 50 and twisting):
        ttiwst = time.time()
    else:
        pass



def main():
    leftwheel = Wheel(forwardGpio = gpios_run_forward[0], backGpio = gpios_run_back[0], pwm = pwmchips[0],
                 pwm_pin = pwms_pines[0], period = period, duty_cycle = 2000)
    rightwheel = Wheel(forwardGpio = gpios_run_forward[1], backGpio = gpios_run_back[1], pwm = pwmchips[0],
                 pwm_pin = pwms_pines[1], period = period, duty_cycle = 2000)
    
    leftTachometer = Tachometer(tachometerGpios[0])
    rightTachometer = Tachometer(tachometerGpios[1])
    
    ultrasonic = Ultrasonic(ultrasonicGpios[0], ultrasonicGpios[1])
    
    leftwheel.init()
    rightwheel.init()
    leftTachometer.init()
    rightTachometer.init()
    ultrasonic.init()
    
    
    calcDesiredSpeed(leftwheel, rightwheel, leftTachometer, rightTachometer)   #Get the desired speed
    current_time = time.time()
    
    
    
    while(time.time() - current_time < 2000):
        """leftwheel.run(period, Direction.FORWARD)
        rightwheel.run(period, Direction.FORWARD)"""
        proportional_speed(leftwheel, leftTachometer)
        proportional_speed(rightwheel, rightTachometer)
        
        val = ultrasonic.distanceInMillimeters()
        print("DISTANCIA %d " %(val))
        manageTwist(val, leftwheel, rightwheel)
        
        print("Velocidad izquierda %d" %(leftTachometer.getvelowheel()))
        print("Velocidad derecha %d" %(rightTachometer.getvelowheel()))
    
if __name__ == "__main__":
    main()