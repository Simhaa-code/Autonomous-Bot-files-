
import cv2
import torch
import folium
import serial 
import pynmea2
import threading
from flask import Flask, Response, render_template_string, request, redirect
from geopy.distance import geodesic
from math import radians, degrees, sin, cos, atan2
import time

app = Flask(__name__)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

camera_frame = None
gps_lat = 0.0
gps_lon = 0.0
target_lat = None
target_lon = None
obstacle_detected = False

arduino = serial.Serial('/dev/ttyACM0', 9600)

def capture_video():
    global camera_frame, obstacle_detected
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            results = model(frame)
            obstacle_detected = any([res['name'] in ['person', 'car', 'bicycle', 'truck'] for res in results.pandas().xyxy[0].to_dict('records')])
            frame = results.render()[0]
            camera_frame = frame

def read_gps():
    global gps_lat, gps_lon
    try:
        port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
        while True:
            line = port.readline().decode("utf-8", errors="replace")
            if line.startswith('$GPGGA'):
                msg = pynmea2.parse(line)
                if msg.latitude and msg.longitude:
                    gps_lat = msg.latitude
                    gps_lon = msg.longitude
    except Exception as e:
        print("GPS Error:", e)

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).meters

def get_command():
    global gps_lat, gps_lon, target_lat, target_lon, obstacle_detected
    if obstacle_detected:
        return 'S'
    if target_lat is None or target_lon is None:
        return 'S'
    dist = calculate_distance((gps_lat, gps_lon), (target_lat, target_lon))
    if dist < 2:
        return 'S'
    else:
        return 'F'   

def auto_move():
    while True:
        cmd = get_command()
        arduino.write(cmd.encode())
        time.sleep(1)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    global gps_lat, gps_lon, target_lat, target_lon
    if request.method == 'POST':
        target_lat = float(request.form['target_lat'])
        target_lon = float(request.form['target_lon'])
        return redirect('/')
    map_object = folium.Map(location=[gps_lat, gps_lon], zoom_start=16)
    folium.Marker([gps_lat, gps_lon], tooltip="Bot Location").add_to(map_object)
    if target_lat and target_lon:
        folium.Marker([target_lat, target_lon], tooltip="Target Location", icon=folium.Icon(color='red')).add_to(map_object)
    html_map = map_object._repr_html_()
    return render_template_string('''
        <html>
            <head><title>Auto GPS Bot with Obstacle Detection</title></head>
            <body>
                <h1>Live Video Feed</h1>
                <img src="{{ url_for('video_feed') }}" width="640" height="480">
                <h2>Enter Destination GPS Coordinates</h2>
                <form method="POST">
                    Latitude: <input name="target_lat" required><br>
                    Longitude: <input name="target_lon" required><br>
                    <button type="submit">Set Target</button>
                </form>
                <h1>Real-Time GPS Map</h1>
                {{ map_html|safe }}
            </body>
        </html>
    ''', map_html=html_map)

if __name__ == '__main__':
    threading.Thread(target=capture_video, daemon=True).start()
    threading.Thread(target=read_gps, daemon=True).start()
    threading.Thread(target=auto_move, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
