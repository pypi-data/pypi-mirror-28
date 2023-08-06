#include <Servo.h>

# For testing purposes...
def trace(func, args):
    print func, args

HIGH="HIGH"
LOW="LOW"
OUTPUT="OUTPUT"

def digitalWrite(*args):         trace("digitalWrite", args)
def delayMicroseconds(*args):    trace("delayMicroseconds", args)
def pinMode(*args):              trace("pinMode", args)
def analogRead(*args):           trace("analogRead", args); return 0
def millis(*args):               trace("millis", args); return 0

class Servo(object):
    def __init__(self):
        self.pin = None
    def writeMicroseconds(self, number):
        if self.pin != None:
            trace("Servo.writeMicroseconds", [self.pin, number])
        else:
            trace("Servo.writeMicroseconds", number)
    def attach(self, pin):
        trace("Servo.attach", pin)
        self.pin = pin

# ::::::::::::::
# InternetLinks.ino
# ::::::::::::::
# Arduino Software:      http://arduino.cc/en/Main/Software
# USB Drivers:           http://www.silabs.com/products/mcu/Pages/USBtoUARTBridgeVCPDrivers.aspx
# DAGU Product Support:  https://sites.google.com/site/daguproducts/

# ::::::::::::::
# IOpins.h
# ::::::::::::::

FLHpin = 6      # Front Left  Hip        - digital output   D6
FRHpin = 11     # Front Right Hip        - digital output  D11
RLHpin = 5      # Rear  Left  Hip        - digital output   D5
RRHpin = 4      # Rear  Right Hip        - digital output   D4

FLKpin = 12     # Front Left  Knee       - digital output  D12
FRKpin = 13     # Front Right Knee       - digital output  D13
RLKpin = 2      # Rear  Left  Knee       - digital output   D2
RRKpin = 3      # Rear  Right Knee       - digital output   D3

PANpin = 14     # Neck  Pan   A0         - digital output  D14
TILpin = 15     # Neck  Tilt  A1         - digital output  D15

IRleft = 2      # Compound Eye Left      - analog  input    A2
IRright = 4     # Compound Eye Right     - analog  input    A3
IRup = 3        # Compound Eye Up        - analog  input    A4
IRdown = 5      # Compound Eye Down      - analog  input    A5
IRleds = 8      # Compound Eye LEDs      - digital output   D8

# ::::::::::::::
# Constants.h
# ::::::::::::::
Speed = 40           # time in mS allowed for each cycle for walk - must allow for servo speed
Stepsize = 250       # size of steps
Boredom = 6000       # time in milliseconds before robot gets bored and sits down

LRscalefactor = 2    # LR & UD scalefactors used to adjust pan/tilt servo responsiveness
UDscalefactor = 2    # smaller values will prevent overshoot but can make servos slow to respond
distancemax = 200    # distance values smaller than this are assumed out of range
bestdistance = 500   # robot will try to maintain this distance from the object

FLHcenter = 1500     # Front Left  Hip  center position - ajust to suit servos
FRHcenter = 1500     # Front Righ  Hip  center position - ajust to suit servos
RLHcenter = 1500     # Rear  Left  Hip  center position - ajust to suit servos
RRHcenter = 1500     # Rear  Right Hip  center position - ajust to suit servos

FLKcenter = 1500     # Front Left  Knee center position - ajust to suit servos
FRKcenter = 1500     # Front Righ  Knee center position - ajust to suit servos
RLKcenter = 1500     # Rear  Left  Knee center position - ajust to suit servos
RRKcenter = 1500     # Rear  Right Knee center position - ajust to suit servos

PANcenter = 1500     # Pan  servo center position
TILcenter = 1500     # Tilt servo center position

LRmax = 2300         # Pan  center position +800 - head turned 80 degrees  left
LRmin = 700          # Pan  center position -800 - head turned 80 degrees right
UDmax = 2000         # Look up   - adjust so head does not try to bend backward
UDmin = 700          # look down - ajust so head looks down without straining servo

IRdelay = 200        #  microseconds to wait while phototransistors respond to changes in IR

# ::::::::::::::
# PlayfulPuppy.ino
# ::::::::::::::


# -------------------------------------------------------------- define global variables and servos here ---------------------------
time = 0l           # "l" to hint 'unsigned long'  // timer used to control walk speed
sit = 0l            # "l" to hint 'unsigned long'  // timer used to determine lazyness and control sit movement
trick = 0l          # "l" to hint 'unsigned long'  // timer used to control jump, shake hand and lie down movement

LShift = 0          # int    // Speed and direction of left legs
RShift = 0          # int    // Speed and direction of right legs
Raise = 0           # int    // amount to lift legs by
cycle = 0           # int    // counter to control leg movements

pan=PANcenter       # int    // position of pan  servo - start at center
tilt=TILcenter      # int    // position of tilt servo - start at center

distance = 0        # int    // aproximate distance of object (average of sensor readings)
temp = 0L           # long   // tempory value used in various calculations

leftIRvalue = 0     # int   // Left  sensor value after correcting for ambient light
rightIRvalue = 0    # int   // Right sensor value after correcting for ambient light
upIRvalue = 0       # int   // Upper sensor value after correcting for ambient light
downIRvalue = 0     # int   // Lower sensor value after correcting for ambient light

# define hip servos
FLHservo = Servo()  # Servo FLHservo
FRHservo = Servo()  # Servo FRHservo
RLHservo = Servo()  # Servo RLHservo
RRHservo = Servo()  # Servo RRHservo

# define knee servos
FLKservo = Servo()  # Servo FLKservo
FRKservo = Servo()  # Servo FRKservo
RLKservo = Servo()  # Servo RLKservo
RRKservo = Servo()  # Servo RRKservo

# define pan, tilt and tail wag servos
PANservo = Servo()  # Servo PANservo
TILservo = Servo()  # Servo TILservo




#setup()
# def setup():
FLHservo.attach(FLHpin)                                    # attach hip  servos
FRHservo.attach(FRHpin)
RLHservo.attach(RLHpin)
RRHservo.attach(RRHpin)

FLKservo.attach(FLKpin)                                    # attach knee servos
FRKservo.attach(FRKpin)
RLKservo.attach(RLKpin)
RRKservo.attach(RRKpin)

PANservo.attach(PANpin)                                    # attach head servos
TILservo.attach(TILpin)

FLHservo.writeMicroseconds(FLHcenter)                      # Center servos
FRHservo.writeMicroseconds(FRHcenter)
RLHservo.writeMicroseconds(RLHcenter)
RRHservo.writeMicroseconds(RRHcenter)
FLKservo.writeMicroseconds(FLKcenter)
FRKservo.writeMicroseconds(FRKcenter)
RLKservo.writeMicroseconds(RLKcenter)
RRKservo.writeMicroseconds(RRKcenter)
PANservo.writeMicroseconds(PANcenter)
TILservo.writeMicroseconds(TILcenter)

pinMode(IRleds,OUTPUT)                                     # enable digital output to control IR leds on compound eye

while True:
    # loop()
    # ============================================================== Main Loop ==========================================================
    # def loop():
    # return;                                    # enable to freeze robot when setting servo center positions
    # IReye()                                                    # read eye sensors allowing for ambient light
    # ::::::::::::::
    # IReye.ino
    # ::::::::::::::
    # def IReye(): # ================================================== Read IR compound eye =========================
    #
    digitalWrite(IRleds,HIGH)                                  #  turn on IR LEDs to read TOTAL IR LIGHT (ambient + reflected)
    delayMicroseconds(IRdelay)                                 # allow time for phototransistors to respond.
    leftIRvalue  = analogRead(IRleft)                          # TOTAL IR = AMBIENT IR + LED IR REFLECTED FROM OBJECT
    rightIRvalue = analogRead(IRright)                         # TOTAL IR = AMBIENT IR + LED IR REFLECTED FROM OBJECT
    upIRvalue    = analogRead(IRup)                            # TOTAL IR = AMBIENT IR + LED IR REFLECTED FROM OBJECT
    downIRvalue  = analogRead(IRdown)                          # TOTAL IR = AMBIENT IR + LED IR REFLECTED FROM OBJECT
    #
    digitalWrite(IRleds, LOW)                                  # turn off IR LEDs to read AMBIENT IR LIGHT (IR from indoor lighting and sunlight)
    delayMicroseconds(IRdelay)                                 # allow time for phototransistors to respond.
    leftIRvalue  = leftIRvalue - analogRead(IRleft)            # REFLECTED IR = TOTAL IR - AMBIENT IR
    rightIRvalue = rightIRvalue - analogRead(IRright)          # REFLECTED IR = TOTAL IR - AMBIENT IR
    upIRvalue    = upIRvalue - analogRead(IRup)                # REFLECTED IR = TOTAL IR - AMBIENT IR
    downIRvalue  = downIRvalue - analogRead(IRdown)            # REFLECTED IR = TOTAL IR - AMBIENT IR
    #
    distance = (leftIRvalue + rightIRvalue + upIRvalue + downIRvalue) / 4 # distance of object is mean of reflected IR


    #IRtrack()                                                  # track objects with head
    # ::::::::::::::
    # IRtrack.ino
    # ::::::::::::::
    #def IRtrack(): # =============================================== Track object in range ==========================
    # global pan
    # global tilt
    if distance < distancemax:                          #  nothing in range - return head to center position
        if pan>PANcenter:
            pan = pan - 5
        if pan<PANcenter:
            pan = pan + 5
        if tilt>TILcenter:
            tilt = tilt - 3
        if tilt < TILcenter:
            tilt = tilt + 3
    else:
        # ---------------------------------------------------------- Track object with head --------------------
        # Consider meaning of "/" in embedded context
        panscale = (leftIRvalue + rightIRvalue) / LRscalefactor  # panscale & tiltscale used to adjust servo response according to distance
        tiltscale = (upIRvalue + downIRvalue) / UDscalefactor    # adjust LRscalefactor and UDscalefactor to tweak servo responsiveness
        #
        leftright = (rightIRvalue - leftIRvalue) * 5 / panscale
        pan = pan + leftright
        updown = (downIRvalue - upIRvalue) * 5 / tiltscale
        tilt = tilt + updown
        # 
        if pan < LRmin: pan=LRmin
        if pan > LRmax: pan=LRmax
        if tilt < UDmin: tilt=UDmin
        if tilt > UDmax: tilt=UDmax
    #
    # 
    # PANservo.writeMicroseconds(pan)
    # TILservo.writeMicroseconds(tilt)
    PANservo.writeMicroseconds(1500-(pan-1500))                 #  reverses direction of pan/tilt servos
    TILservo.writeMicroseconds(1500-(tilt-1500))


    # ------------------------------------------------------------ Decide what to do --------------------------------------------------
    if millis() - sit < Boredom:       # puppy is playing
        # Follow()                                      # follow object with body to keep in range
        # ::::::::::::::
        # Follow.ino
        # ::::::::::::::
        # def Follow(): # ================================================= Body follows object ============================
        # global LShift
        # global RShift
        LShift = 0                                                   # reset left and right speeds
        RShift = 0
        if not (distance<distancemax):   # nothing to follow - stop moving

            # ----------------------------------------Turn body to follow object if head turns too far ------------------
            temp = pan - PANcenter 
            if abs(temp) > 300:                                        # if the head turns off center by more than 300
              LShift = temp/2                                            # adjust left and right speeds to turn towards the object
              RShift = -temp/2

            # ------------------------------------------------------------ Move forward or backward to follow object ---------------------------------------
            temp = (distance - bestdistance) * 15 / 10                     # *15/10 = *1.5 but with whole numbers
            LShift = LShift - temp
            RShift = RShift - temp

            if(LShift>Stepsize):
                LShift=Stepsize

            if(LShift<-Stepsize):
                LShift=-Stepsize

            if(RShift>Stepsize):
                RShift=Stepsize

            if(RShift<-Stepsize):
                RShift=-Stepsize

        # Play()                                        # follows object or jump
        # ::::::::::::::
        # Play.ino
        # ::::::::::::::
        # def Play():
        # global LShift
        # global RShift
        # global time
        Raise = 150 +((abs(LShift) + abs(RShift)) /2)      # adjust hight of step to suit stride
        if Raise < 200:                                    # not worth moving - stand still
            LShift = 0
            RShift = 0
            Raise = 0
        else:
            sit = millis()                                 # reset sit timer if moving
            trick = millis()                               # reset trick timer

        if tilt < 980:                                     # if looking straight up then jump!
            # Jump()
            # ::::::::::::::
            # Jump.ino
            # ::::::::::::::
            # ============================================================ Jump onto rear legs ==============================================
            # def Jump():

            pan = PANcenter
            tilt = 1700
            # ------------------------------------------------------------ Lean forward -------------------------------------
            PANservo.writeMicroseconds(1500-(pan-1500))                #  move head into correct position
            TILservo.writeMicroseconds(1500-(tilt-1500))               #  head looks down when on hind legs
            RLHservo.writeMicroseconds(RLHcenter-600)                  # put rear hips backward to shift balance
            RRHservo.writeMicroseconds(RRHcenter+600) 
            FLKservo.writeMicroseconds(FLKcenter-600)                  #  straighten front knees in preparation to jump
            FRKservo.writeMicroseconds(FRKcenter-600) 
            delay(350)                                                 # wait for body to fall fall forward
            #
            # ------------------------------------------------------------ Jump up on back legs ----------------------------------
            FLHservo.writeMicroseconds(FLHcenter+600)                  # front hips forward
            FRHservo.writeMicroseconds(FRHcenter-600)
            RLHservo.writeMicroseconds(RLHcenter+600)                  # rear hips forward
            RRHservo.writeMicroseconds(RRHcenter-600)
            FLKservo.writeMicroseconds(FLKcenter+300)                  # front knees bent inward to push up
            FRKservo.writeMicroseconds(FRKcenter+300)
            RLKservo.writeMicroseconds(RLKcenter+100)                  # Bend knees slightly to create pivot point
            RRKservo.writeMicroseconds(RRKcenter+100)

            trick = millis()                                           # reset trick timer
            while millis()-trick<2000:                                  # minimum time to stay on back legs
                # IReye()                                                  # read eye sensors allowing for ambient light
                # ::::::::::::::
                # IReye.ino
                # ::::::::::::::
                # def IReye(): # ================================================== Read IR compound eye =========================
                #
                digitalWrite(IRleds,HIGH)                                  #  turn on IR LEDs to read TOTAL IR LIGHT (ambient + reflected)
                delayMicroseconds(IRdelay)                                 # allow time for phototransistors to respond.
                leftIRvalue  = analogRead(IRleft)                          # TOTAL IR = AMBIENT IR + LED IR REFLECTED FROM OBJECT
                rightIRvalue = analogRead(IRright)                         # TOTAL IR = AMBIENT IR + LED IR REFLECTED FROM OBJECT
                upIRvalue    = analogRead(IRup)                            # TOTAL IR = AMBIENT IR + LED IR REFLECTED FROM OBJECT
                downIRvalue  = analogRead(IRdown)                          # TOTAL IR = AMBIENT IR + LED IR REFLECTED FROM OBJECT
                #
                digitalWrite(IRleds, LOW)                                  # turn off IR LEDs to read AMBIENT IR LIGHT (IR from indoor lighting and sunlight)
                delayMicroseconds(IRdelay)                                 # allow time for phototransistors to respond.
                leftIRvalue  = leftIRvalue - analogRead(IRleft)            # REFLECTED IR = TOTAL IR - AMBIENT IR
                rightIRvalue = rightIRvalue - analogRead(IRright)          # REFLECTED IR = TOTAL IR - AMBIENT IR
                upIRvalue    = upIRvalue - analogRead(IRup)                # REFLECTED IR = TOTAL IR - AMBIENT IR
                downIRvalue  = downIRvalue - analogRead(IRdown)            # REFLECTED IR = TOTAL IR - AMBIENT IR
                #
                distance = (leftIRvalue + rightIRvalue + upIRvalue + downIRvalue) / 4 # distance of object is mean of reflected IR

                # ::::::::::::::
                # IRtrack.ino
                # ::::::::::::::
                # IRtrack()                                                # track objects with head
                #def IRtrack(): # =============================================== Track object in range ==========================
                # global pan
                # global tilt
                if distance < distancemax:                          #  nothing in range - return head to center position
                    if pan>PANcenter:
                        pan = pan - 5
                    if pan<PANcenter:
                        pan = pan + 5
                    if tilt>TILcenter:
                        tilt = tilt - 3
                    if tilt < TILcenter:
                        tilt = tilt + 3
                else:
                    # ---------------------------------------------------------- Track object with head --------------------
                    # Consider meaning of "/" in embedded context
                    panscale = (leftIRvalue + rightIRvalue) / LRscalefactor  # panscale & tiltscale used to adjust servo response according to distance
                    tiltscale = (upIRvalue + downIRvalue) / UDscalefactor    # adjust LRscalefactor and UDscalefactor to tweak servo responsiveness
                    #
                    leftright = (rightIRvalue - leftIRvalue) * 5 / panscale
                    pan = pan + leftright
                    updown = (downIRvalue - upIRvalue) * 5 / tiltscale
                    tilt = tilt + updown
                    # 
                    if pan < LRmin: pan=LRmin
                    if pan > LRmax: pan=LRmax
                    if tilt < UDmin: tilt=UDmin
                    if tilt > UDmax: tilt=UDmax
                #
                # 
                # PANservo.writeMicroseconds(pan)
                # TILservo.writeMicroseconds(tilt)
                PANservo.writeMicroseconds(1500-(pan-1500))                 #  reverses direction of pan/tilt servos
                TILservo.writeMicroseconds(1500-(tilt-1500))


                if distance > distancemax :
                    trick=millis()                       # reset the timer as long as object in range

            #------------------------------------------------------------ return body to standing on 4 legs --------------------
            RLKservo.writeMicroseconds(RLKcenter-300)                  # straighten rear knees slightly to lower body back down
            RRKservo.writeMicroseconds(RRKcenter-300)
            FLKservo.writeMicroseconds(FLKcenter)                      # straighten front knees to land on feet
            FRKservo.writeMicroseconds(FRKcenter)
            delay(100)                                                 # allow time for servos to respond

            RLHservo.writeMicroseconds(RLHcenter)                      # return rear hips to normal position
            RRHservo.writeMicroseconds(RRHcenter)
            delay(100)                                                 # allow time for servos to respond
            RLKservo.writeMicroseconds(RLKcenter)                      # return rear knees to normal position
            RRKservo.writeMicroseconds(RRKcenter)
            delay(100)                                                 # slow down to prevent robot falling backward

            RLKservo.writeMicroseconds(RLKcenter - 300)    # allow robot to fall back on it's feet
            RRKservo.writeMicroseconds(RRKcenter - 300)
            delay(250)
            sit = millis()                                 # reset sit timer

        if millis() - time > Speed:                        # time for next step in robot gait
            time = millis()                                # reset leg movement timer
            WalkingMotion()                                # take a step
            # ::::::::::::::
            # WalkingMotion.ino
            # ::::::::::::::
            # def WalkingMotion():
            # This function controls the leg movements to walk and turn.
            # Turning is done by make the legs on one side go foward while the other side go backward.
            # The intergers LShift and RShift determine the size and direction of the step for left and right sides.
            # Cycle controls the walking sequence.
            cycle = cycle + 1                                    # increment counter
            if cycle > 9:
                cycle=0                                          # reset counter if greater than 9

            # Note: some movements require more time than others
            #       depending on how far servos must travel.
            #       This is why 6 moves take 10 steps.
            if cycle == 0:
                FRKservo.writeMicroseconds(FRKcenter - Raise)    # raise front right leg
                RLKservo.writeMicroseconds(RLKcenter - Raise)    # raise rear  left  leg
                FLHservo.writeMicroseconds(FLHcenter - LShift)   # move  front left  leg forward / backward
                RRHservo.writeMicroseconds(RRHcenter + RShift)   # move  rear  right leg forward / backward

            elif cycle == 1:
                FRHservo.writeMicroseconds(FRHcenter - RShift)   # move  front right leg forward / backward
                RLHservo.writeMicroseconds(RLHcenter + LShift)   # move  rear  left  leg forward / backward

            elif cycle == 3:
                FRKservo.writeMicroseconds(FRKcenter)            # lower front right leg
                RLKservo.writeMicroseconds(RLKcenter)            # lower rear  left  leg

            elif cycle == 5:
                FLKservo.writeMicroseconds(FLKcenter - Raise)    # raise front left  leg
                RRKservo.writeMicroseconds(RRKcenter - Raise)    # raise rear  right leg
                FRHservo.writeMicroseconds(FRHcenter + RShift)   # move  front right leg forward / backward
                RLHservo.writeMicroseconds(RLHcenter - LShift)   # move  rear  left  leg forward / backward

            elif cycle == 6:
                FLHservo.writeMicroseconds(FLHcenter+LShift)     # move  front left  leg forward / backward
                RRHservo.writeMicroseconds(RRHcenter-RShift)     # move  rear  right leg forward / backward

            elif cycle == 8:
                FLKservo.writeMicroseconds(FLKcenter)            # lower front left  leg
                RRKservo.writeMicroseconds(RRKcenter)            #  lower rear  right leg

    else:                              # puppy is bored
        # SitShakeLiedown()                             # sits down, shakes hands or lies down
        # 
        # ::::::::::::::
        # SitShakeLiedown.ino
        #  ::::::::::::::
        # def SitShakeLiedown():
            temp = millis() - sit                     # time since last walked
            if temp < Boredom + 800:                  # Puppy in the process of sitting down
                #SittingMotion()                       # make puppy sit down slowly
                # ::::::::::::::
                # SittingMotion.ino
                # ::::::::::::::
                # def SittingMotion():
                # ---------------------------------------------------------- Sit Down -------------------------------------
                cycle = 9
                temp = (temp - Boredom) * 4                        # controls speed of sitting motion
                if temp > 3000:
                   temp = 3000

                FLHservo.writeMicroseconds(FLHcenter)              # center front hip servos
                FRHservo.writeMicroseconds(FRHcenter)

                RLHservo.writeMicroseconds(RLHcenter + (temp/6))   # set rear hips forward
                RRHservo.writeMicroseconds(RRHcenter - (temp/6))

                FLKservo.writeMicroseconds(FLKcenter)              # center front knees
                FRKservo.writeMicroseconds(FRKcenter)

                RLKservo.writeMicroseconds(RLKcenter - (temp/7))   # straighten rear knees
                RRKservo.writeMicroseconds(RRKcenter - (temp/7))

            if tilt < 800:
                sit=millis()                            # reset sit timer if puppy looking straight up
                RLHservo.writeMicroseconds(RLHcenter)   # straighten rear hips in preparation to get up
                RRHservo.writeMicroseconds(RRHcenter)
                delay(150)                              # slow down standing process to prevent robot falling backward

            else:
                # ---------------------------------------------------------- Shake Hands / Lie Down -------------------------------------------------
                if tilt < 1700:
                    trick = millis()                              # reset timer if looking up

                temp = millis() - trick                           # time how long head is looking down

                # --------------------------------------------- hand position determines trick - head follows hand - if head is central then robot will lie down
                if temp > 600:                                       # if head is looking down for more than 600mS

                    temp = (temp - 1000) * 4                          # use timer to control speed of movement
                    if temp > 3000:
                        temp=3000

                    if pan > PANcenter - 150:                            # if head is looking to the right, shake right paw
                        FRHservo.writeMicroseconds(FRHcenter - (temp/6))    # move front right hip forward
                        FRKservo.writeMicroseconds(FRKcenter - (temp/5))    # straighten front right knee

                    if pan < PANcenter + 150:                               # if head is looking to the left, shake left paw
                        FLHservo.writeMicroseconds(FLHcenter + (temp/6))    # move front left  hip forward
                        FLKservo.writeMicroseconds(FLKcenter - (temp/5))    # straighten front right knee
