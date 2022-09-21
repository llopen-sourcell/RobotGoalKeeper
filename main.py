import cv2
from cvzone import ColorFinder,findContours
import numpy as np
#from SerComm import write_read
cap = cv2.VideoCapture(0)

myColorFinder = ColorFinder(False)

#hsvVals={'hmin': 6, 'smin': 101, 'vmin': 126, 'hmax': 13, 'smax': 234, 'vmax': 255}
hsvVals={'hmin': 27, 'smin': 35, 'vmin': 153, 'hmax': 43, 'smax': 255, 'vmax': 255}
posListX,posListY = [],[]
xList = [item for item in range(1280)]

while True:
    success,img = cap.read()
    #img = img[:, 500:]
    imgColor,mask = myColorFinder.update(img,hsvVals)
    imgContours,contours = findContours(img,mask,minArea=1000)

    if contours:
        posListX.append(contours[0]['center'][0])
        posListY.append(contours[0]['center'][1])
        cx,cy = contours[0]['center'] 
        print(cx,cy)
        
    if posListX:
        A,B,C = np.polyfit(posListX,posListY,2)

        for i,(posX,posY) in enumerate(zip(posListX,posListY)):
            pos = (posX,posY)
            cv2.circle(imgContours,pos,2,(0,255,255),cv2.FILLED)
            if i == 0:
                cv2.line(imgContours,pos,pos,(0,255,0),2)
            else:    
                cv2.line(imgContours,pos,(posListX[i-1],posListY[i-1]),(0,255,0),2)
        for x in xList:
            y=int(A*x**2 + B*x + C)
            cv2.circle(imgContours,(x,y),2,(0,255,255),cv2.FILLED)
        #write_to_arduino(x,y)
    imgColor = cv2.resize(imgColor, (0,0), None, 0.7, 0.7 )

    cv2.imshow("Image Color",imgContours)
    cv2.imshow("contours",imgColor)
    cv2.waitKey(10)
    if cv2.waitKey(33) == ord('a'):
        posListX,posListY = [],[]          
        #cv2.waitKey(-1) #wait until any key is pressed 
    
        