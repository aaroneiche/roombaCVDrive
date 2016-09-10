# 69, 119, 172
import logging
import cv2
import numpy as np              #importing libraries
cap = cv2.VideoCapture(1)       #creating camera object
import heapq
import time

from RoombaSCI import RoombaAPI

#Initialize Roomba
roomba = RoombaAPI("/dev/tty.FireFly-E812-SPP",115200);
if roomba:
    roomba.start()
    roomba.safe()

roombaCommandSent = False
roombaLastCommand = 0


driving = False
leftBaseVal = 0
rightBaseVal = 0

# lower = (54, 66, 180) # Daylight lower range for pink Wilson Raquet balls.
lower = (157,112,69)
upper = (185, 255, 255)

#Initialization Squares
iSquares = ((320,800),(960,800),(320,900),(960,900))
initSize = 50


def getBallData(contour):
    ((x, y), radius) = cv2.minEnclosingCircle(contour)
    orientation = "R" if x > 600 else "L"

    return {"side": orientation, "x":x, "y":y, "r":radius}

def drawFeedbackCircles(image,ballData):
    cv2.putText(image, str(ballData['r'] * 5), (int(ballData['x']-100),int(ballData['y']+100)), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,180),2)
    cv2.circle(image, (int(ballData['x']), int(ballData['y'])), int(ballData['r']),(255, 0, 0), 3)


def drawStartSquare(image,(x,y)):
    cv2.rectangle(image,(x-50,y-50),(x+50,y+50),(0,150,0),2)

def drawStopSquare(image,(x,y)):
    cv2.rectangle(image,(x-50,y-50),(x+50,y+50),(0,0,200),2)

def doRoombaDrive(lspeed,rspeed):
    global roombaLastCommand
    logging.warn("Driving at " + str(lspeed) + "|" + str(rspeed))
    if time.time() > (roombaLastCommand+0.5):
        roomba.drive_direct(lspeed,rspeed)
        roombaLastCommand = time.time()

def roombaStop():
    roomba.drive_direct(0,0)

#Sort of our Main Loop.
while( cap.isOpened() ) :
    ret,img = cap.read()        #reading the frames
    img = cv2.flip(img,1)       #mirror the image.

    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lower,upper)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    cv2.rectangle(img,(0,400),(1280,600),(0,0,200),2)


    if len(cnts) > 1 :
        # Get the 2 largest contours
        c1,c2 = heapq.nlargest(2,cnts,key=cv2.contourArea)

        # Make sure the contours we're looking at are big enough to be matching balls.
        if cv2.contourArea(c1) > 600 and cv2.contourArea(c2) > 600:

            b1 = getBallData(c1)
            b2 = getBallData(c2)

            if b1['side'] == 'R':
                left = b1
                right = b2
            else:
                left = b2
                right = b1

            drawFeedbackCircles(img,left)
            drawFeedbackCircles(img,right)

            #Check if we're in the driving area.
            if 400 < left['y'] < 600 and 400 < right['y'] < 600:
                if not driving:
                    driving = True
                    rightBaseVal = right['r']
                    leftBaseVal = left['r']

                rdiff = right['r'] - rightBaseVal
                ldiff = left['r'] - leftBaseVal

                if ldiff < 0:
                    lval = -70 + int(ldiff)
                else:
                    lval = +70 + int(ldiff)

                if rdiff < 0:
                    rval = -70 + int(rdiff)
                else:
                    rval = +70 + int(rdiff)

                if driving:
                    doRoombaDrive(lval ,rval)

                if 600 > left['y'] > 400:
                    cv2.putText(img, str(lval), (250,100),cv2.FONT_HERSHEY_SIMPLEX, 1,(127,127,0),3)
                if 600 > right['y'] > 400:
                    cv2.putText(img, str(rval), (700,100),cv2.FONT_HERSHEY_SIMPLEX, 1,(127,127,0),3)
            else:
                if driving:
                    # doRoombaDrive(0,0)
                    roombaStop()
                    logging.warn("Turning off.")
                    driving = False
                    logging.warn(driving)


    cv2.imshow('input',img)     #displaying the frames


    #handle
    k = cv2.waitKey(10)
    if k == 27:
        break
    if(k == 115): #s
        #sample
        logging.warn("toggling sample")
        sample = not sample
    if(k == 109): #m
        #mask
        logging.warn("toggling mask")
        mask = not mask
