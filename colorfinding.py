import cv2
from cvzone import ColorFinder,findContours


myColorFinder = ColorFinder(True)

hsvValue={'hmin': 49, 'smin': 43, 'vmin': 52, 'hmax': 80, 'smax': 255, 'vmax': 255}
while True:
    img = cv2.imread('new.jpg')
    img = img[0:900, :]
    imgcolor,mask = myColorFinder.update(img,hsvValue)
    img = cv2.resize(img,(0,0),None,0.7,0.7)
    cv2.imshow("Image",img)
    cv2.imshow("Image Colour",imgcolor)
    cv2.waitKey(50)