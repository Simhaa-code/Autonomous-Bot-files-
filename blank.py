import cv2 as cv
import numpy as np 
blank = np.zeros((500,500,), dtype=np.uint8)
cv.imshow("blank Screen",blank)
cv.waitKey(0)
cv.destroyAllWindows()