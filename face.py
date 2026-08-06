import cv2 as cv

haar_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

img = cv.imread('test.jpg')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

faces = haar_cascade.detectMultiScale(gray, 1.1, 3)

for (x,y,w,h) in faces:
    cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

cv.imshow('Detected Faces', img)

cv.waitKey(0)