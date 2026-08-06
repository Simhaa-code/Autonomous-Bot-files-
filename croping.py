import cv2 as cv
import numpy as np 
img = cv.imread('test12.jpg')
resized = cv.resize(img,(500,500),interpolation=cv.INTER_LINEAR)
cv.imshow('croped',resized)
cv.waitKey(0)
cv.destroyAllWindows()