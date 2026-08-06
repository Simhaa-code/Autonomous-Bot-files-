import cv2
import torch
import ipinfo
import folium
import serial
import threading
import numpy as np
from flask import Flask, Response, render_template_string

app = Flask(_name_)

access_token = 'YOUR_IPINFO_ACCESS_TOKEN'
handler = ipinfo.getHandler(access_token)

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

camera_frame = None

def detect_lanes(frame):
    height, width = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    mask = np.zeros_like(edges)
    polygon = np.array([[
        (0, height),
        (width, height),
        (width, int(height * 0.6)),
        (0, int(height * 0.6))
    ]], np.int32)
    cv2.fillPoly(mask, polygon, 255)
    masked_edges = cv2.bitwise_and(edges, mask)
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=150)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
    return frame

def avoid_obstacles(results):
    for *box, conf, cls in results.xyxy[0]:
        if conf > 0.5:
            x1, y1, x2, y2 = map(int, box)
            width = x2 - x1
            height = y2 - y1
            if width * height > 5000:
                ser.write(b'STOP\n')
                return
    ser.write(b'GO\n')

def capture_video():
    global camera_frame
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            frame = detect_lanes(frame)
            results = model(frame)
            avoid_obstacles(results)
            frame = results.render()[0]
            camera_frame = frame

@app.route('/video_feed')
def video_feed():
    def generate():
        global camera_frame
        while True:
            if camera_frame is not None:
                ret, buffer = cv2.imencode('.jpg', camera_frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    details = handler.getDetails()
    location = details.loc.split(',')
    lat, lon = float(location[0]), float(location[1])
    map_object = folium.Map(location=[lat, lon], zoom_start=16)
    folium.Marker([lat, lon], tooltip="Bot Location").add_to(map_object)
    html_map = map_object.repr_html()
    return render_template_string('''
        <html>
            <head><title>Bot Camera & Map</title></head>
            <body>
                <h1>Live Bot Feed</h1>
                <img src="{{ url_for('video_feed') }}" width="640" height="480">
                <h1>Live Map</h1>
                {{ map_html|safe }}
            </body>
        </html>
    ''', map_html=html_map)

if _name_ == '_main_':
    video_thread = threading.Thread(target=capture_video)
    video_thread.daemon = True
    video_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=False)