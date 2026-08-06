import cv2 as cv 
import numpy as np 
img = cv.imread ("test1.jpg")
blank = np.zeros((500,500,3), dtype=np.uint8)
blank[:] = (0, 255, 0)
cv.rectangle(blank,(100,100),(500,300),(0,255,255),2)
cv.putText(blank,"COLOR TEST",(180,220),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
cv.imshow("Green Screen",blank)
cv.waitKey(0)
cv.destroyAllWindows()
