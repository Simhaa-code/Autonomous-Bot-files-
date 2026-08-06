import cv2 as cv
haar_cascade = cv.CascadeClassifier("haar_cascadefacedetect")
img = cv.imread("test14.webp")
face_rect = haar_cascade.detectMultiScale(img,scaleFactor=1.1,minNeighbors=3)
print (f"numbe rface detected ={len(face_rect)}")
for (x,y,w,h) in face_rect:
    cv.rectangle(img,(x,y),(x+y,w+h),(0,255,0),2)

cv.imshow("facedetection",img)
cv.waitKey(0)