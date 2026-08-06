import cv2 as cv
import numpy as np 
blank = np.zeros((500,500,3),dtype='uint8')
blank[:]= (255,0,0)
cv.rectangle(blank,(100,100),(500,300),(0,255,255),2)
cv.putText(blank,"COLOR TEST",(180,220),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
cv.circle(blank,(200,200),5,(0,255,0),3)
cv.imshow('blue screen',blank)
cv.waitKey(0)
cv.destroyAllWindows()
