# 69, 119, 172
import logging
import cv2
import numpy as np              #importing libraries
cap = cv2.VideoCapture(1)       #creating camera object
import heapq

# lower = (54, 66, 180) # Daylight lower range for pink Wilson Raquet balls.
lower = (157,112,69)
upper = (185, 255, 255)

def drawFeedbackCircles(contour,image):
    ((x, y), radius) = cv2.minEnclosingCircle(contour)
    orientation = "R" if x > 600 else "L"

    cv2.putText(image, str(int(radius)), (int(x),int(y)), cv2.FONT_HERSHEY_SIMPLEX, 2,(127,127,0),3)
    cv2.circle(image, (int(x), int(y)), int(radius),(255, 0, 0), 3)



while( cap.isOpened() ) :
    ret,img = cap.read()        #reading the frames
    img = cv2.flip(img,1)       #mirror the image.

    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lower,upper)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 1 :
        # Get the 2 largest contours
        c1,c2 = heapq.nlargest(2,cnts,key=cv2.contourArea)

        # Make sure the contours we're looking at are big enough to be matching balls.
        if cv2.contourArea(c1) > 600 and cv2.contourArea(c2) > 600:

            drawFeedbackCircles(c1,img)
            drawFeedbackCircles(c2,img)

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
