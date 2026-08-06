import cv2 as cv 
import numpy as np 
img = cv.imread("test12.jpg")
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
canny = cv.Canny(gray,125,175)
cv.imshow('Canny image',canny)
cv.waitKey(0)
cv.destroyAllWindows()