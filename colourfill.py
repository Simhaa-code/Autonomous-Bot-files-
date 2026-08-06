import cv2 as cv 
import numpy as np
blank = np.zeros((500,500,3), dtype='uint8')
blank[:] = (255,0,0)
cv.imshow('blue scren',blank)
cv.waitKey(0)
cv.destroyAllWindows()