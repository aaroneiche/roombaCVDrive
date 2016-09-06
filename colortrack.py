# 69, 119, 172
import logging
import cv2
import numpy as np              #importing libraries
cap = cv2.VideoCapture(1)       #creating camera object
import heapq

# lower = (54, 66, 180)
lower = (157,112,69)
upper = (185, 255, 255)


while( cap.isOpened() ) :
    ret,img = cap.read()        #reading the frames
    img = cv2.flip(img,1)

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
            ((x1, y1), radius1) = cv2.minEnclosingCircle(c1)
            ((x2, y2), radius2) = cv2.minEnclosingCircle(c2)


            M1 = cv2.moments(c1)
            center1 = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))

            M2 = cv2.moments(c2)
            center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))

            #draw matching circles.
            cv2.circle(img, (int(x1), int(y1)), int(radius1),(255, 0, 0), 3)
            cv2.circle(img, (int(x2), int(y2)), int(radius2),(0, 255, 0), 3)


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
