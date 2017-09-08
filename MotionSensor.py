import time
from Sensor import *
 
class MotionSensor(Sensor):
    
    def __init__(self, pin):
        Sensor.__init__(self,pin)
        self.mail = 0
        self.prev_state = 1
        print "inital state: %d" % (self.getState())
 
    def onStateChange(self, channel):
        #print "%s: pin: %d state: %d" % (time.asctime(), channel, self.getState())
        if self.prev_state == 0 and self.getState() == 1:
            self.mail += 1
            print "You got mail! Total mail: %d" % (self.mail)
        self.prev_state = self.getState()
        
            

 
def main():
    sensor = MotionSensor(17)
    sensor.setEvent(GPIO.BOTH)
    while True:
        time.sleep(1)
 
if __name__ == "__main__":
    main()
