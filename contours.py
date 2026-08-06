import cv2 as cv 
import numpy as np 
img = cv.imread('test11.jpg')
resized = cv.resize(img,(500,500),interpolation=cv.INTER_LINEAR)
gray = cv.cvtColor(resized,cv.COLOR_BGR2GRAY)
thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)
canny = cv.Canny(gray,125,175)
contours,hierachies = cv.findContours(canny,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
blank = np.zeros((500, 500, 3), dtype=np.uint8)
cv.drawContours(blank, contours, -1, (120, 0, 200), 1)
cv.imshow('Contours Draw',blank)
cv.waitKey(0)
cv.destroyAllWindows()

