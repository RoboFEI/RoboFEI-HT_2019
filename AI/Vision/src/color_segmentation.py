#! /usr/bin/env python

import cv2
import cv2.cv as cv
import numpy as np

def nothing(x,y):
    pass

cv2.namedWindow('image')
# create trackbars for color change
cv2.createTrackbar('H_Low','image',0,255,nothing)
cv2.createTrackbar('H_High','image',0,255,nothing)
cv2.createTrackbar('S_Low','image',0,255,nothing)
cv2.createTrackbar('S_High','image',255,255,nothing)
cv2.createTrackbar('V_Low','image',0,255,nothing)
cv2.createTrackbar('V_High','image',255,255,nothing)

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    ret, frame = cap.read()
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # get current positions of four trackbars
    h_high  = cv2.getTrackbarPos('H_High','image')
    h_low = cv2.getTrackbarPos('H_Low','image')
    s_high = cv2.getTrackbarPos('S_High','image')
    s_low = cv2.getTrackbarPos('S_Low','image')
    v_high = cv2.getTrackbarPos('V_High','image')
    v_low = cv2.getTrackbarPos('V_Low','image')
    
    #orange:
    lower_blue = np.array([h_low,s_low,v_low]) 
    upper_blue = np.array([h_high,s_high,v_high])
    
    # Threshold the HSV image to get only orange colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

	#erosion
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(mask,kernel,iterations=3)

    #dilation
    dilation = cv2.dilate(erosion,kernel,iterations=3)

    img = cv2.medianBlur(dilation,21)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask=dilation)

    momento = cv2.moments(img)
    try:
        cx = int(momento['m10']/momento['m00'])
        cy = int(momento['m01']/momento['m00'])
        area = momento['m00']
        print cx, cy, area
    except ZeroDivisionError:
        pass

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,'Press: ',(30,30), font, 0.5, 160)
    cv2.putText(img,'o for orange',(30,50), font, 0.5, 160)
    cv2.putText(img,'y for yellow',(30,70), font, 0.5, 160)
    cv2.putText(img,'g for green',(30,90), font, 0.5, 160)
    cv2.putText(img,'v for violet',(30,110), font, 0.5, 160)
    cv2.putText(img,'r for red',(30,130), font, 0.5, 160)
    cv2.putText(img,'b for blue',(30,150), font, 0.5, 160)
    cv2.putText(img,'Esc for exit',(30,170), font, 0.5, 160)

    cv2.imshow('image',img)
    cv2.imshow('frame',frame)
    cv2.imshow('cor',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    if k ==  98: #b - blue
        cv2.setTrackbarPos('H_High', 'image', 130)
        cv2.setTrackbarPos('H_Low', 'image', 75)
    if k ==  111: #o - orange
        cv2.setTrackbarPos('H_High', 'image', 22)
        cv2.setTrackbarPos('H_Low', 'image', 0)
    if k ==  121: #y - yellow
        cv2.setTrackbarPos('H_High', 'image', 38)
        cv2.setTrackbarPos('H_Low', 'image', 22)
    if k ==  103: #g - green
        cv2.setTrackbarPos('H_High', 'image', 92)
        cv2.setTrackbarPos('H_Low', 'image', 75)     
    if k ==  118: #v - violet
        cv2.setTrackbarPos('H_High', 'image', 160)
        cv2.setTrackbarPos('H_Low', 'image', 130)  
    if k ==  114: #r - red
        cv2.setTrackbarPos('H_High', 'image', 179)
        cv2.setTrackbarPos('H_Low', 'image', 160) 

cv2.destroyAllWindows()
