# 69, 119, 172
import logging
import cv2
import numpy as np              #importing libraries
cap = cv2.VideoCapture(1)       #creating camera object
import heapq

from RoombaSCI import RoombaAPI

#Initialize Roomba
roomba = RoombaAPI("/dev/tty.FireFly-E812-SPP",115200);
if roomba:
    roomba.start()
    roomba.safe()

roombaCommandSent = False

driving = False

# lower = (54, 66, 180) # Daylight lower range for pink Wilson Raquet balls.
lower = (157,112,69)
upper = (185, 255, 255)

#Initialization Squares
iSquares = ((320,800),(960,800),(320,1000),(960,1000))
initSize = 50


# def getBallData(contour):
#     ((x, y), radius) = cv2.minEnclosingCircle(contour)
#     return (x,y,radius)

def getBallData(contour):
    ((x, y), radius) = cv2.minEnclosingCircle(contour)
    orientation = "R" if x > 600 else "L"

    return {"side": orientation, "x":x, "y":y, "r":radius}

def drawFeedbackCircles(image,ballData):
    cv2.putText(image, str(int(ballData['r'])), (int(ballData['x']),int(ballData['y'])), cv2.FONT_HERSHEY_SIMPLEX, 2,(127,127,0),3)
    cv2.circle(image, (int(ballData['x']), int(ballData['y'])), int(ballData['r']),(255, 0, 0), 3)


def drawStartSquare(image,(x,y)):
    cv2.rectangle(image,(x-50,y-50),(x+50,y+50),(0,150,0),2)

def drawStopSquare(image,(x,y)):
    cv2.rectangle(image,(x-50,y-50),(x+50,y+50),(0,0,200),2)



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


    if driving:
        drawStartSquare(img,(iSquares[0][0],iSquares[0][1]))
        drawStartSquare(img,(iSquares[1][0],iSquares[1][1]))
    else :
        drawStartSquare(img,(iSquares[2][0],iSquares[2][1]))
        drawStartSquare(img,(iSquares[3][0],iSquares[3][1]))


    if len(cnts) > 1 :
        # Get the 2 largest contours
        c1,c2 = heapq.nlargest(2,cnts,key=cv2.contourArea)

        # Make sure the contours we're looking at are big enough to be matching balls.
        if cv2.contourArea(c1) > 600 and cv2.contourArea(c2) > 600:

            b1 = getBallData(c1)
            b2 = getBallData(c2)


            # checkInitialized(img,(iSquares[0][0],iSquares[0][1]))
            # checkInitialized(img,(iSquares[1][0],iSquares[1][1]))

            drawFeedbackCircles(img,b1)
            drawFeedbackCircles(img,b2)



            if not roombaCommandSent:
                # roomba.clean()
                roombaCommandSent = True


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
