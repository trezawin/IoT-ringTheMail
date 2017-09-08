import RPi.GPIO as GPIO
import time
from Board import Board
from MQPublisher import Publisher

class MailSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.IN)
        self.mail = 0
        self.totalMail = 0
        self.prev_state = self.getState() #set inital state (1)
        self.timer = 0.0
        self.openMail = False
 
    def getState(self):
        return GPIO.input(self.pin)

    def getPrevState(self):
        return self.prev_state

    def setPrevState(self):
        self.prev_state = self.getState()

    def receivedMail(self):
        if self.prev_state == 0 and self.getState() == 1:
            return True

    def addMail(self):
        self.mail += 1

    def resetMail(self):
        self.mail = 0

    def getMail(self):
        return self.mail

    def addTimer(self):
        self.timer += 0.1

    def resetTimer(self):
        self.timer = 0

    def getTimer(self):
        return self.timer

    def addTotalMail(self):
        self.totalMail += 1

    def resetTotalMail(self):
        self.totalMail = 0

    def getTotalMail(self):
        return self.totalMail

    def openMailBox(self):
        self.openMail = True

    def closeMailBox(self):
        self.openMail = False

    def isOpenMailBox(self):
        return self.openMail


def main():

    sensor = MailSensor(17)
    board = Board()
    publisher = Publisher("myid", "userID", "localhost")
    
    #print "Initial State: %d" % (sensor.getPrevState())
    #print "Timer: %s" % (sensor.getTimer()) 

    while True:
        time.sleep(0.1)
        sensor.addTimer()

        #always check if the mailbox is open, if light sensor return more than 200 means mailbox is open
        #print "INFO: Open Checking " + str(board.light())
        if board.light() < 220:
            if not sensor.isOpenMailBox():
                sensor.openMailBox()
                print "WARNING: MailBox Opened!"
                if sensor.getTotalMail() > 0:
                    msg = "The mails had been collected."
                    publisher = Publisher("myid", "userID", "localhost")
                    publisher.pushToMQ("postBox1", msg)
                    print "MESSAGE SENT: " + msg
                    sensor.resetTotalMail()
                    sensor.resetMail()
                else:
                    print "There isn't any mail in the mailbox."
                sensor.resetTimer()

        #stall the programm when mailbox is open
        while sensor.isOpenMailBox():
            time.sleep(5)
            #print "INFO: Close Checking " + str(board.light())
            if board.light() >= 220:
                sensor.closeMailBox()
                print "INFO: MailBox Closed!"

        
        #print "Timer: %s" % (sensor.getTimer()) 
        if str(sensor.getTimer()) == "8.0":
            if sensor.getMail() > 0:
                msg = "You have %s new mails in your mailbox" % (sensor.getTotalMail())
                print "MESSAGE SENT: " + msg
                publisher = Publisher("myid", "userID", "localhost")
                publisher.pushToMQ("postBox1", msg)
                sensor.resetTimer()
                sensor.resetMail()
            else:
                sensor.resetTimer()
                #print "WARNING: You have no mails! Timer: %s" % (sensor.getTimer())
        #print "Previous State: %d" % (sensor.getPrevState())
        #print "Current State: %d" % (sensor.getState())
                
        if sensor.receivedMail():
            sensor.addMail()
            sensor.addTotalMail()
            sensor.resetTimer()
            print "You got a new mail! Total number of new mails: %d" % (sensor.getMail())
        sensor.setPrevState()
 
if __name__ == "__main__":
    main()
