from asyncore import write
import math
import serial
import cv2
import time
from cvzone import ColorFinder,findContours
import numpy as np

cap = cv2.VideoCapture(1)
cap.set(3,620)
cap.set(4,480)
myColorFinder = ColorFinder(False)
arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)
#hsvVals={'hmin': 6, 'smin': 101, 'vmin': 126, 'hmax': 13, 'smax': 234, 'vmax': 255}
hsvVals={'hmin': 11, 'smin': 56, 'vmin': 234, 'hmax': 43, 'smax': 237, 'vmax': 255}
posListX,posListY = [],[]
xList = [item for item in range(1280)]
depthh=0
flag=True
angleList=[]

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

while True:
    success,img = cap.read()
    #img = img[:, 500:]
    imgColor,mask = myColorFinder.update(img,hsvVals)
    imgContours,contours = findContours(img,mask,minArea=1000)

    if contours:
        posListX.append(contours[0]['center'][0])
        posListY.append(contours[0]['center'][1])
        cx,cy = contours[0]['center']
        dx,dy=cx,cy 
        cy = np.abs(cy-480)
        
        #print(int(contours[0]['area']))
        depthh = -0.002249*int(contours[0]['area']) + 46.72
        cv2.putText(imgContours,'Depth= '+str(int(depthh)),(30,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
        cv2.putText(imgContours,'X = '+str(int(cx)),(30,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
        cv2.putText(imgContours,'Y = '+str(int(cy)),(30,90),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
        if depthh < 25:
            
            cv2.line(imgContours, (310, 480), (dx, dy), (0, 255, 0), thickness=2)
            if dx==310:
                pass
            else:
                slope_m = (dy-480) / (dx-310)
             
            angle = math.degrees(math.atan(slope_m))
            if angle < 0:
                angle+=180
            angleList.append(angle)
            if len(angleList) > 5 and flag == True:
                write_read(str(math.ceil(angle)))
                #print(math.ceil(angle))
                flag=False
            cv2.putText(imgContours,'angle'+str(int(angle)),(cx+10,dy+10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
    if posListX:
        
        cv2.circle(imgContours,(cx,cy),2,(0,255,255),cv2.FILLED)
        #write_to_arduino(x,y)
    #imgColor = cv2.resize(imgColor, (0,0), None, 0.7, 0.7 )
    
    cv2.imshow("Image Color",imgContours)
    
    cv2.waitKey(50)
    if cv2.waitKey(33) == ord('a'):
        posListX,posListY = [],[]           
    if cv2.waitKey(1) == ord('p'):
        flag=True
