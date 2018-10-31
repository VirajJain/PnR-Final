import pigo
import time  # import just in case students need
import random

# setup logs
import logging
LOG_LEVEL = logging.INFO
LOG_FILE = "/home/pi/PnR-Final/log_robot.log"  # don't forget to make this file!
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


class Piggy(pigo.Pigo):
    """Student project, inherits teacher Pigo class which wraps all RPi specific functions"""

    def __init__(self):
        """The robot's constructor: sets variables and runs menu loop"""
        print("I have been instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 92
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 30
        self.HARD_STOP_DIST = 15
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 140
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 143
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        if __name__ == "__main__":
            while True:
                self.stop()
                self.menu()

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "s": ("Check status", self.status),
                "h": ("Open House", self.open_house),
                "q": ("Quit", quit_now),
                "t": ("Test", self.skill_test)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    def skill_test(self):
        """tests my skill"""
        choice = raw_input("Left/Right or Turn Until Clear?")

        if "l" in choice:
            self.wide_scan(count=4)   # scan the area
            #picks left or right

            # create two variables, left_total and right_total
            left_total = 0
            right_total = 0
            # loop from self.MIDPOINT - 60 to self.MIDPOINT
            for angle in range(self.MIDPOINT - 60, self.MIDPOINT):
                if self.scan[angle]:
                    # add up the numbers to right_total
                    right_total += self.scan[angle]
            # loop from self.MIDPOINT to self.MIDPOINT + 60
            for angle in range(self.MIDPOINT, self.MIDPOINT + 60):
                # add up the numbers to left_total
                if self.scan[angle]:
                    left_total += self.scan[angle]
            # if right is bigger:
            if right_total > left_total:
                # turn right
                self.encR(17)
            # if left is bigger
            if left_total > right_total:
                # turn left
                self.encL(17)
        else:

            # while it's not clear
            while not self.is_clear():
                # turn
                self.encL(1)
            pass


    def open_house(self):
        """reacts to dist in funny way"""
        while True:
            if self.dist() < 20:
                self.set_speed(90, 90)
                self.half_backward()
                for x in range(4):
                    self.head_left()
                    self.head_right()
                self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
                for x in range(2):
                    self.encL(17)
                    self.encR(17)
                    self.encR(17)
                    self.encL(17)
                self.half_forward()
                self.move_right_fully()
                self.move_left_fully()
            time.sleep(.1)

    # YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        """executes a series of methods that add up to a compound dance"""
        if not self.safe_to_dance():
            print("\n---- Not Safe to Dance----\n")
            return
        print("\n---- LET'S DANCE ----\n")
        ##### WRITE YOUR FIRST PROJECT HERE
        #Ride, 21 Pilots
        #start at 27 seconds
        for x in range(2):
            for y in range(3):
                self.half_forward()
                self.chill_medium()
                self.half_backward()
                self.chill_medium()
            for y in range(8):
                self.head_left()
                self.chill_short()
                self.head_right()
                self.chill_medium()
            self.head_left()
            self.chill_short()
            self.head_right()
        self.finisher()
        #THANKS RICKY
        self.x_up()

    def head_left(self):
        """moving head left"""
        self.servo(self.MIDPOINT + 20)

    def head_right(self):
        """moving head right"""
        self.servo(self.MIDPOINT - 20)

    def forward(self):
        """moving forward"""
        self.encF(18)

    def half_forward(self):
        """moving a little forward"""
        self.encF(9)

    def backward(self):
        """moving backward"""
        self.encB(18)

    def half_backward(self):
        """"moving a little backward"""
        self.encB(9)

    def move_left_fully(self):
        """"rotate left a full circle"""
        self.encL(25)

    def move_right_fully(self):
        '''rotate right a full circle'''
        self.encR(25)

    def chill_short(self):
        """"not move for a short period of time"""
        time.sleep(0.01)

    def chill_medium(self):
        """"not move for a reasonable amount of time"""
        time.sleep(0.1)

    def chill_long(self):
        """not move for a long period of time"""
        time.sleep(1)

    def safe_to_dance(self):
        """circles around and checks for obstacles"""
        # check for problems
        for x in range(4):
            if not self.is_clear():
                return False
            self.encL(7)
        # if we find no problems
        return True

    def finisher(self):
        """FINISH HIM"""
        for x in range(4):
            self.encL(28)
            self.encR(28)
            for y in range(4):
                self.servo(self.MIDPOINT + 20)
                self.servo(self.MIDPOINT - 20)

###From Ricky
    def x_up(self):
        """supposed to make an X formation"""
        for x in range(4):
            self.encB(9)
            self.encR(2)
            self.encF(9)
            self.encL(2)
            self.encB(9)
            self.encL(2)
            self.encF(9)
            self.encR(2)

    def obstacle_count(self):
        """scans and estimates the number of obstacles within sight"""
        self.wide_scan(count = 1)
        found_something = False
        counter = 0
        for ang, distance in enumerate(self.scan):
            if distance and distance < 150 and not found_something:
                found_something = True
                counter += 1
                print("Object # %d found, I think" % counter)
            if distance and distance > 150 and found_something:
                found_something = False
        print("\n----I SEE %d OBJECTS----\n" % counter)

    def safety_check(self):
        """subroutine of the dance method"""
        self.servo(self.MIDPOINT)  # look straight ahead
        for loop in range(4):
            if not self.is_clear():
                print("NOT GOING TO DANCE")
                return False
            print("Check #%d" % (loop + 1))
            self.encR(8)  # figure out 90 deg
        print("Safe to dance!")
        return True

    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        while True:
            if self.is_clear():
                self.cruise()
            else:
                self.encR(8)
                #don't have a perfect right turn :(

    def cruise(self):
        """ drive straight while path is clear """
        self.fwd()
        while self.dist() > self.SAFE_STOP_DIST:
            time.sleep(.01)
        self.stop()
####################################################
############### STATIC FUNCTIONS

def error():
    """records general, less specific error"""
    logging.error("ERROR")
    print('ERROR')


def quit_now():
    """shuts down app"""
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy


try:
    g = Piggy()
except (KeyboardInterrupt, SystemExit):
    pigo.stop_now()
except Exception as ee:
    logging.error(ee.__str__())
