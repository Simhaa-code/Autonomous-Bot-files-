import cv2
import numpy as np

cap = cv2.VideoCapture("lanedetection.mp4")

def region_of_interest(img):
    height = img.shape[0]
    width = img.shape[1]

    mask = np.zeros_like(img)

    polygon = np.array([[
        (0, height),
        (width, height),
        (width//2, height//2)
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)

    masked_image = cv2.bitwise_and(img, mask)

    return masked_image


while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    edges = cv2.Canny(blur, 50, 150)

    cropped_edges = region_of_interest(edges)

    lines = cv2.HoughLinesP(
        cropped_edges,
        1,
        np.pi/180,
        50,
        minLineLength=80,
        maxLineGap=50
    )

    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line[0]

            # Filter almost horizontal lines
            if abs(y2 - y1) > 20:
                cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),3)

    cv2.imshow("Lane Detection", frame)

    if cv2.waitKey(25) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()